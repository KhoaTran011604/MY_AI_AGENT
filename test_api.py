"""
Test script to check HuggingFace API connection
"""

import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

api_key = os.getenv("HUGGINGFACE_API_KEY")

print("=" * 60)
print("HuggingFace API Connection Test")
print("=" * 60)
print(f"\nAPI Key loaded: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"API Key prefix: {api_key[:10]}...")

print("\nTesting connection to HuggingFace API...")
print("-" * 60)

try:
    client = InferenceClient(token=api_key)

    # Test with a simple model first
    model = "mistralai/Mistral-7B-Instruct-v0.1"
    print(f"Using model: {model}")

    messages = [
        {"role": "user", "content": "Say hello in one sentence."}
    ]

    print("\nSending test message...")
    response = client.chat_completion(
        messages=messages,
        model=model,
        max_tokens=100,
        temperature=0.7
    )

    print("\n[SUCCESS]")
    print("Response received:")
    print("-" * 60)
    print(response.choices[0].message.content)
    print("-" * 60)
    print("\n[OK] API is working correctly!")
    print("\nYou can now use the Flask API at http://127.0.0.1:5000/chat")

except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {str(e)}")
    print("\nPossible issues:")
    print("1. Invalid or expired API key")
    print("2. Model requires access approval")
    print("3. Rate limit exceeded (free tier)")
    print("4. Network connection issue")
    print("\nSuggestions:")
    print("- Try a different model (e.g., microsoft/DialoGPT-medium)")
    print("- Check your API key at: https://huggingface.co/settings/tokens")
    print("- Wait a few minutes if rate limited")
    print("- Request access to the model on HuggingFace")
