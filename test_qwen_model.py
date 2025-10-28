import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import HuggingFaceChatbot

# Load environment variables
load_dotenv()

def test_qwen_model():
    print("Testing Qwen/Qwen2.5-72B-Instruct model...")
    print("-" * 50)

    # Check if API key is set
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        print("WARNING: HUGGINGFACE_API_KEY not found in .env file!")
        print("The test will use free tier which may have limitations.\n")
    else:
        print(f"API Key found: {api_key[:10]}...\n")

    # Initialize chatbot with Qwen model
    bot = HuggingFaceChatbot(model_name="Qwen/Qwen2.5-72B-Instruct")

    # Test simple message
    test_message = "Hello! Can you introduce yourself?"
    print(f"Sending test message: {test_message}")
    print("-" * 50)

    response = bot.chat(test_message)
    print(f"\nResponse:\n{response}")
    print("-" * 50)

    # Check if response is an error
    if "Error" in response or "I'm sorry" in response:
        print("\n❌ Model test FAILED!")
        print("\nTroubleshooting:")
        print("1. Check if your HUGGINGFACE_API_KEY is valid")
        print("2. Verify you have access to Qwen/Qwen2.5-72B-Instruct")
        print("3. Try a different model like 'meta-llama/Llama-3.2-3B-Instruct'")
        print("4. Check HuggingFace status: https://status.huggingface.co/")
    else:
        print("\n✅ Model test SUCCESSFUL!")

if __name__ == "__main__":
    test_qwen_model()
