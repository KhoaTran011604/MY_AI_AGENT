"""
Services Package
Business logic layer
"""

from .product_service import ProductService
from .chatbot_service import ProductChatbot

# Aliases
ChatbotService = ProductChatbot

__all__ = [
    'ProductService',
    'ProductChatbot',
    'ChatbotService'
]
