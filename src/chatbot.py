import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

class HuggingFaceChatbot:
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        """
        Initialize the chatbot with a HuggingFace model

        Args:
            model_name (str): The HuggingFace model to use for chat
        """
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.model_name = model_name

        if self.api_key:
            self.client = InferenceClient(token=self.api_key)
        else:
            self.client = InferenceClient()

        self.conversation_history = []

    def chat(self, user_message):
        """
        Send a message and get a response from the chatbot

        Args:
            user_message (str): The user's message

        Returns:
            str: The chatbot's response
        """
        try:
            # Add user message to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })

            # Generate response using HuggingFace Inference API
            response = self.client.chat_completion(
                messages=self.conversation_history,
                model=self.model_name,
                max_tokens=500,
                temperature=0.7
            )

            # Extract the assistant's reply - handle both response types
            if hasattr(response, 'choices') and len(response.choices) > 0:
                assistant_message = response.choices[0].message.content
            else:
                # Fallback if response structure is different
                assistant_message = str(response)

            # Add assistant's response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message

        except StopIteration:
            # Handle empty response from API
            return "I'm sorry, I couldn't generate a response. The model might be unavailable or rate limited. Please try again later."
        except Exception as e:
            return f"Error ({type(e).__name__}): {str(e)}"

    def reset_conversation(self):
        """Clear the conversation history"""
        self.conversation_history = []
        return "Conversation history cleared."

if __name__ == "__main__":
    # Simple test
    bot = HuggingFaceChatbot()
    print("Chatbot initialized!")
    print("Type 'quit' to exit or 'reset' to clear conversation history\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'quit':
            print("Goodbye!")
            break

        if user_input.lower() == 'reset':
            print(bot.reset_conversation())
            continue

        response = bot.chat(user_input)
        print(f"Bot: {response}\n")
