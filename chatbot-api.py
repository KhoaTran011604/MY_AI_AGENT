import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from chatbot import HuggingFaceChatbot
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Store chatbot instances for different sessions
chatbot_sessions = {}

def get_or_create_chatbot(session_id):
    """
    Get existing chatbot session or create a new one

    Args:
        session_id (str): Unique session identifier

    Returns:
        HuggingFaceChatbot: Chatbot instance for this session
    """
    if session_id not in chatbot_sessions:
        chatbot_sessions[session_id] = HuggingFaceChatbot()
    return chatbot_sessions[session_id]

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'active_sessions': len(chatbot_sessions)
    }), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint

    Request body:
    {
        "message": "user message",
        "session_id": "optional-session-id"
    }

    Response:
    {
        "response": "bot response",
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

        # Get or create chatbot for this session
        chatbot = get_or_create_chatbot(session_id)

        # Get bot response
        bot_response = chatbot.chat(user_message)

        return jsonify({
            'response': bot_response,
            'session_id': session_id,
            'status': 'success'
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/session/new', methods=['POST'])
def create_session():
    """
    Create a new chat session

    Response:
    {
        "session_id": "new-session-id",
        "status": "success"
    }
    """
    try:
        session_id = str(uuid.uuid4())
        chatbot_sessions[session_id] = HuggingFaceChatbot()

        return jsonify({
            'session_id': session_id,
            'status': 'success',
            'message': 'New session created'
        }), 201

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/session/<session_id>/reset', methods=['POST'])
def reset_session(session_id):
    """
    Reset conversation history for a session

    Response:
    {
        "status": "success",
        "message": "Conversation history cleared"
    }
    """
    try:
        if session_id not in chatbot_sessions:
            return jsonify({
                'error': 'Session not found',
                'status': 'error'
            }), 404

        chatbot_sessions[session_id].reset_conversation()

        return jsonify({
            'status': 'success',
            'message': 'Conversation history cleared'
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/session/<session_id>/delete', methods=['DELETE'])
def delete_session(session_id):
    """
    Delete a chat session

    Response:
    {
        "status": "success",
        "message": "Session deleted"
    }
    """
    try:
        if session_id not in chatbot_sessions:
            return jsonify({
                'error': 'Session not found',
                'status': 'error'
            }), 404

        del chatbot_sessions[session_id]

        return jsonify({
            'status': 'success',
            'message': 'Session deleted'
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/session/<session_id>/history', methods=['GET'])
def get_history(session_id):
    """
    Get conversation history for a session

    Response:
    {
        "history": [...],
        "status": "success"
    }
    """
    try:
        if session_id not in chatbot_sessions:
            return jsonify({
                'error': 'Session not found',
                'status': 'error'
            }), 404

        chatbot = chatbot_sessions[session_id]

        return jsonify({
            'history': chatbot.conversation_history,
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
        "sessions": ["session-id-1", "session-id-2"],
        "count": 2,
        "status": "success"
    }
    """
    try:
        session_ids = list(chatbot_sessions.keys())

        return jsonify({
            'sessions': session_ids,
            'count': len(session_ids),
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

    print(f"Starting Chatbot API on port {port}...")
    print(f"Debug mode: {debug_mode}")
    print("\nAvailable endpoints:")
    print("  GET  /health - Health check")
    print("  POST /api/chat - Send message")
    print("  POST /api/session/new - Create new session")
    print("  POST /api/session/<id>/reset - Reset session history")
    print("  DELETE /api/session/<id>/delete - Delete session")
    print("  GET  /api/session/<id>/history - Get conversation history")
    print("  GET  /api/sessions - List all sessions")
    print("\n")

    app.run(host='0.0.0.0', port=port, debug=debug_mode)
