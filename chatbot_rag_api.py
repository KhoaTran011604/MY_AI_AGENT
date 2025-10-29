"""
REST API for RAG Chatbot with MongoDB Knowledge Base
Provides endpoints for chat and knowledge management
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from chatbot_rag import RAGChatbot
import uuid

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize chatbot (singleton)
chatbot = None
chatbot_sessions = {}

def get_chatbot():
    """Get or initialize chatbot instance"""
    global chatbot
    if chatbot is None:
        try:
            chatbot = RAGChatbot()
        except Exception as e:
            print(f"Failed to initialize chatbot: {e}")
            raise
    return chatbot


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        bot = get_chatbot()
        stats = bot.get_statistics()
        return jsonify({
            'status': 'healthy',
            'knowledge_items': stats['total_knowledge'],
            'active_sessions': len(chatbot_sessions)
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat with RAG bot

    Request:
    {
        "message": "user message",
        "session_id": "optional-session-id"
    }

    Response:
    {
        "response": "bot response",
        "relevant_knowledge": [...],
        "used_knowledge_base": true,
        "session_id": "session-id",
        "status": "success"
    }
    """
    try:
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({
                'error': 'Missing required field: message',
                'status': 'error'
            }), 400

        user_message = data['message']
        session_id = data.get('session_id', str(uuid.uuid4()))

        # Get chatbot and generate response
        bot = get_chatbot()
        result = bot.chat(user_message, session_id=session_id)

        # Track session
        if session_id not in chatbot_sessions:
            chatbot_sessions[session_id] = {
                'created_at': str(uuid.uuid1().time),
                'message_count': 0
            }
        chatbot_sessions[session_id]['message_count'] += 1

        return jsonify({
            **result,
            'session_id': session_id,
            'status': 'success'
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/knowledge/add', methods=['POST'])
def add_knowledge():
    """
    Add new knowledge to database

    Request:
    {
        "question": "What is Python?",
        "answer": "Python is a programming language...",
        "category": "programming",
        "tags": ["python", "programming"]
    }

    Response:
    {
        "doc_id": "document-id",
        "status": "success",
        "message": "Knowledge added successfully"
    }
    """
    try:
        data = request.get_json()

        if not data or 'question' not in data or 'answer' not in data:
            return jsonify({
                'error': 'Missing required fields: question, answer',
                'status': 'error'
            }), 400

        question = data['question']
        answer = data['answer']
        category = data.get('category', 'general')
        tags = data.get('tags', [])

        bot = get_chatbot()
        doc_id = bot.add_knowledge(question, answer, category, tags)

        return jsonify({
            'doc_id': doc_id,
            'status': 'success',
            'message': 'Knowledge added successfully'
        }), 201

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/knowledge/search', methods=['POST'])
def search_knowledge():
    """
    Search knowledge by query

    Request:
    {
        "query": "search query",
        "top_k": 5
    }

    Response:
    {
        "results": [...],
        "count": 3,
        "status": "success"
    }
    """
    try:
        data = request.get_json()

        if not data or 'query' not in data:
            return jsonify({
                'error': 'Missing required field: query',
                'status': 'error'
            }), 400

        query = data['query']
        top_k = data.get('top_k', 5)

        bot = get_chatbot()
        results = bot.retrieve_relevant_knowledge(query, top_k=top_k)

        return jsonify({
            'results': [
                {
                    'question': doc['question'],
                    'answer': doc['answer'],
                    'category': doc.get('category', 'general'),
                    'similarity': doc['similarity_score']
                }
                for doc in results
            ],
            'count': len(results),
            'status': 'success'
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/knowledge/list', methods=['GET'])
def list_knowledge():
    """
    List all knowledge in database

    Query params:
    - category: filter by category (optional)

    Response:
    {
        "knowledge": [...],
        "count": 10,
        "status": "success"
    }
    """
    try:
        category = request.args.get('category')

        bot = get_chatbot()
        knowledge_items = bot.db.get_all_knowledge(category=category)

        return jsonify({
            'knowledge': [
                {
                    'id': str(item['_id']),
                    'question': item['question'],
                    'answer': item['answer'],
                    'category': item.get('category', 'general'),
                    'tags': item.get('tags', []),
                    'has_embedding': item.get('embedding') is not None
                }
                for item in knowledge_items
            ],
            'count': len(knowledge_items),
            'status': 'success'
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/knowledge/refresh', methods=['POST'])
def refresh_knowledge():
    """
    Refresh knowledge cache from database

    Response:
    {
        "status": "success",
        "message": "Knowledge cache refreshed",
        "cached_items": 50
    }
    """
    try:
        bot = get_chatbot()
        bot.refresh_knowledge_cache()

        stats = bot.get_statistics()

        return jsonify({
            'status': 'success',
            'message': 'Knowledge cache refreshed',
            'cached_items': stats['cached_knowledge']
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    Get chatbot statistics

    Response:
    {
        "total_knowledge": 50,
        "cached_knowledge": 50,
        "total_conversations": 120,
        "embedding_model": 384,
        "llm_model": "model-name",
        "status": "success"
    }
    """
    try:
        bot = get_chatbot()
        stats = bot.get_statistics()

        return jsonify({
            **stats,
            'active_sessions': len(chatbot_sessions),
            'status': 'success'
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/session/<session_id>/history', methods=['GET'])
def get_session_history(session_id):
    """
    Get conversation history for a session

    Response:
    {
        "history": [...],
        "count": 10,
        "status": "success"
    }
    """
    try:
        limit = request.args.get('limit', 10, type=int)

        bot = get_chatbot()
        history = bot.db.get_conversation_history(session_id, limit=limit)

        return jsonify({
            'history': [
                {
                    'user_message': msg['user_message'],
                    'bot_response': msg['bot_response'],
                    'timestamp': msg['timestamp'].isoformat(),
                    'context': msg.get('context', {})
                }
                for msg in reversed(history)
            ],
            'count': len(history),
            'status': 'success'
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/sessions', methods=['GET'])
def list_sessions():
    """
    List all active sessions

    Response:
    {
        "sessions": [...],
        "count": 5,
        "status": "success"
    }
    """
    try:
        return jsonify({
            'sessions': [
                {
                    'session_id': sid,
                    'message_count': info['message_count']
                }
                for sid, info in chatbot_sessions.items()
            ],
            'count': len(chatbot_sessions),
            'status': 'success'
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error'
    }), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'status': 'error'
    }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'

    print("\n" + "="*60)
    print("RAG CHATBOT API SERVER")
    print("="*60)
    print(f"Port: {port}")
    print(f"Debug mode: {debug_mode}")
    print("\nAvailable endpoints:")
    print("  GET  /health - Health check")
    print("  POST /api/chat - Chat with bot")
    print("  POST /api/knowledge/add - Add knowledge")
    print("  POST /api/knowledge/search - Search knowledge")
    print("  GET  /api/knowledge/list - List all knowledge")
    print("  POST /api/knowledge/refresh - Refresh cache")
    print("  GET  /api/statistics - Get statistics")
    print("  GET  /api/session/<id>/history - Get conversation history")
    print("  GET  /api/sessions - List all sessions")
    print("="*60 + "\n")

    print("Initializing chatbot...")
    try:
        get_chatbot()
        print("✓ Chatbot initialized successfully!\n")
    except Exception as e:
        print(f"✗ Failed to initialize chatbot: {e}\n")
        print("Please check:")
        print("  1. MongoDB is running")
        print("  2. MONGODB_URI in .env is correct")
        print("  3. HUGGINGFACE_API_KEY in .env is set")
        print("\n")
        exit(1)

    app.run(host='0.0.0.0', port=port, debug=debug_mode)
