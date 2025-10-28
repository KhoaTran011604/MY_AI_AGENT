from flask import Flask, request, jsonify
from chatbot import HuggingFaceChatbot
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize chatbot (you can change the model here)
# Popular models:
# - "microsoft/DialoGPT-medium" - conversational AI (fast, reliable)
# - "Qwen/Qwen2.5-72B-Instruct" - very good instruction following (free tier)
# - "mistralai/Mistral-7B-Instruct-v0.2" - instruction following (may need approval)
# - "meta-llama/Llama-3.2-3B-Instruct" - chat model (free tier)
# Using Qwen2.5 which is known to work well on free tier
chatbot = HuggingFaceChatbot(model_name="Qwen/Qwen2.5-72B-Instruct")

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to HuggingFace Chatbot API",
        "endpoints": {
            "/chat": "POST - Send a message to the chatbot",
            "/reset": "POST - Reset conversation history"
        }
    })

@app.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint to chat with the bot
    Expected JSON: {"message": "your message here"}
    """
    try:
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400

        user_message = data['message']
        response = chatbot.chat(user_message)

        return jsonify({
            "user_message": user_message,
            "bot_response": response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset():
    """Reset the conversation history"""
    try:
        message = chatbot.reset_conversation()
        return jsonify({"message": message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    print(f"Using model: {chatbot.model_name}")
    app.run(host='0.0.0.0', port=5000, debug=True)
