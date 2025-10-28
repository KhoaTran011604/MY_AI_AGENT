"""
Quick test script - No interactive input needed
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import HuggingFaceChatbot

def main():
    print("=" * 60)
    print("HuggingFace Chatbot Quick Test")
    print("=" * 60)

    # Use a simple model for testing
    model_name = "mistralai/Mistral-7B-Instruct-v0.1"

    print(f"\nInitializing chatbot with model: {model_name}")
    print("This may take a moment...\n")

    try:
        bot = HuggingFaceChatbot(model_name=model_name)
        print("[OK] Chatbot initialized successfully!")
        print("=" * 60)

        # Test with a simple question
        test_messages = [
            "Hello! What is Python?",
            "Can you tell me a fun fact about AI?",
        ]

        for i, message in enumerate(test_messages, 1):
            print(f"\n[Test {i}]")
            print(f"User: {message}")
            print("Bot: ", end="", flush=True)

            response = bot.chat(message)
            print(response)
            print("-" * 60)

        print("\n[OK] All tests completed successfully!")
        print("\nNext steps:")
        print("1. Add your HuggingFace API key to .env file")
        print("2. Get API key from: https://huggingface.co/settings/tokens")
        print("3. Edit .env and replace 'your_huggingface_api_key_here' with your actual key")
        print("\nThen you can:")
        print("- Run: python demo.py (for interactive chat)")
        print("- Run: cd src && python app_flask.py (for API server)")

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        print("\nTroubleshooting:")
        print("=" * 60)
        print("1. Make sure you have set HUGGINGFACE_API_KEY in .env file")
        print("2. Get your API key from: https://huggingface.co/settings/tokens")
        print("3. Edit .env file and add your key:")
        print("   HUGGINGFACE_API_KEY=hf_your_actual_key_here")
        print("\n4. Some models may require access approval on HuggingFace")
        print("5. Free tier has rate limits - try again in a few moments")
        print("=" * 60)

if __name__ == "__main__":
    main()
