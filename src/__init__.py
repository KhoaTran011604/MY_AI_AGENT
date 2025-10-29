"""
MY_AI_AGENT - AI-powered E-commerce Chatbot
Main package initialization
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from . import config
from . import models
from . import services
from . import routes
from . import utils
from . import integrations

__all__ = [
    'config',
    'models',
    'services',
    'routes',
    'utils',
    'integrations'
]
