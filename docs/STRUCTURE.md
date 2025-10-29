# MY_AI_AGENT - Project Structure

## Current Structure

```
MY_AI_AGENT/
├── src/                              # Source code
│   ├── __init__.py
│   ├── config/                       # Configuration
│   │   ├── __init__.py
│   │   └── settings.py              # Centralized settings
│   ├── models/                       # Data models (Pydantic)
│   │   ├── __init__.py
│   │   └── product.py               # Product schema
│   ├── services/                     # Business logic
│   │   ├── __init__.py
│   │   ├── product_service.py       # ProductService
│   │   └── chatbot_service.py       # ChatbotService
│   ├── utils/                        # Utilities
│   │   ├── __init__.py
│   │   └── db_connection.py         # MongoDB connection
│   └── integrations/                 # External integrations
│       └── __init__.py
├── scripts/                          # Scripts
│   ├── seed_products.py
│   └── seed_data.py
├── docs/                             # Documentation
│   ├── README.md
│   ├── PRODUCT_CHATBOT_README.md
│   ├── RAG_CHATBOT_README.md
│   ├── DISCORD_SETUP.md
│   └── REFACTORING_GUIDE.md
├── tests/                            # Tests (future)
│   └── __init__.py
├── main.py                           # 🎯 NEW ENTRY POINT
├── product_manager.py                # Backward compat wrapper
├── product_chatbot.py                # Backward compat wrapper  
├── product_chatbot_api.py            # Old API (still works)
├── requirements.txt
├── .env
└── .gitignore
```

## Quick Start

### Run with NEW structure:
```bash
python main.py
```

### Run with OLD API (backward compatible):
```bash
python product_chatbot_api.py
```

Both work! 🎉

## Key Changes

1. **Organized Source Code**: Everything in `src/`
2. **Centralized Config**: `src/config/settings.py`
3. **Clean Separation**: models, services, utils
4. **Backward Compatible**: Old imports still work
5. **Single Entry Point**: `main.py`

## Documentation

See `docs/REFACTORING_GUIDE.md` for migration guide.
