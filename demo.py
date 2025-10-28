"""
Demo script to test the HuggingFace Chatbot
Run this after setting up your environment
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import HuggingFaceChatbot

def main():
    print("=" * 50)
    print("HuggingFace Chatbot Demo")
    print("=" * 50)
    print("\nAvailable models you can try:")
    print("1. mistralai/Mistral-7B-Instruct-v0.1 (Recommended)")
    print("2. HuggingFaceH4/zephyr-7b-beta")
    print("3. microsoft/DialoGPT-medium")
    print("4. tiiuae/falcon-7b-instruct")
    print()

    model_name = input("Enter model name (or press Enter for default): ").strip()

    if not model_name:
        model_name = "mistralai/Mistral-7B-Instruct-v0.1"

    print(f"\nInitializing chatbot with model: {model_name}")
    print("This may take a moment...\n")

    try:
        bot = HuggingFaceChatbot(model_name=model_name)
        print("Chatbot ready!")
        print("\nCommands:")
        print("  - Type your message to chat")
        print("  - Type 'reset' to clear conversation history")
        print("  - Type 'quit' or 'exit' to end the session")
        print("=" * 50)
        print()

        while True:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit']:
                print("\nThank you for using the chatbot. Goodbye!")
                break

            if user_input.lower() == 'reset':
                message = bot.reset_conversation()
                print(f"\n{message}\n")
                continue

            print("\nBot: ", end="", flush=True)
            response = bot.chat(user_input)
            print(response)
            print()

    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you have set HUGGINGFACE_API_KEY in your .env file")
        print("2. Get your API key from: https://huggingface.co/settings/tokens")
        print("3. Install required packages: pip install -r requirements.txt")
        print("4. Some models may require access approval on HuggingFace")

if __name__ == "__main__":
    main()
