# Refactoring Guide

## New Project Structure

```
MY_AI_AGENT/
├── src/
│   ├── config/              # Configuration
│   │   ├── __init__.py
│   │   └── settings.py      # Centralized settings
│   ├── models/              # Data models (Pydantic schemas)
│   │   ├── __init__.py
│   │   └── product.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── product_service.py    # ProductService (was ProductManager)
│   │   └── chatbot_service.py    # ChatbotService (was ProductChatbot)
│   ├── routes/              # API routes (future)
│   │   └── __init__.py
│   ├── utils/               # Utilities
│   │   ├── __init__.py
│   │   └── db_connection.py
│   └── integrations/        # External integrations
│       ├── __init__.py
│       └── discord_bot.py
├── scripts/                 # Scripts
│   ├── seed_products.py
│   └── seed_data.py
├── tests/                   # Tests
│   └── __init__.py
├── docs/                    # Documentation
│   ├── PRODUCT_CHATBOT_README.md
│   ├── RAG_CHATBOT_README.md
│   ├── DISCORD_SETUP.md
│   └── REFACTORING_GUIDE.md
├── main.py                  # Main entry point
├── requirements.txt
└── .env
```

## Migration Guide

### Old Code → New Code

#### 1. ProductManager → ProductService

**Old:**
```python
from product_manager import ProductManager

pm = ProductManager()
pm.connect()
```

**New:**
```python
from src.services import ProductService

service = ProductService()
service.connect()
```

**Backward Compatible (still works):**
```python
from product_manager import ProductManager  # Still works but deprecated

pm = ProductManager()
pm.connect()
```

#### 2. ProductChatbot → ChatbotService

**Old:**
```python
from product_chatbot import ProductChatbot

bot = ProductChatbot()
```

**New:**
```python
from src.services import ChatbotService

bot = ChatbotService()
```

**Backward Compatible:**
```python
from product_chatbot import ProductChatbot  # Still works

bot = ProductChatbot()
```

#### 3. Schemas

**Old:**
```python
from schemas.product_schema import ProductSchema
```

**New:**
```python
from src.models import ProductSchema
```

#### 4. Configuration

**Old:**
```python
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
```

**New:**
```python
from src.config import settings

mongodb_uri = settings.MONGODB_URI
```

## Running the Application

### Option 1: Using new main.py (Recommended)

```bash
python main.py
```

### Option 2: Using old API file (Still works)

```bash
python product_chatbot_api.py
```

## Benefits of New Structure

1. **Better Organization**: Clear separation of concerns
   - `models/`: Data schemas
   - `services/`: Business logic
   - `config/`: Configuration
   - `utils/`: Helper functions

2. **Easier Testing**: Each component can be tested independently

3. **Scalability**: Easy to add new features
   - Add new models in `models/`
   - Add new services in `services/`
   - Add new routes in `routes/`

4. **Maintainability**: Code is easier to find and modify

5. **Backward Compatibility**: Old code still works while you migrate

## Next Steps

1. **Test the new structure**:
   ```bash
   python main.py
   ```

2. **Migrate your code gradually**:
   - Start using `from src.services import ProductService`
   - Update imports one file at a time
   - Old imports will still work

3. **Add tests**:
   - Create tests in `tests/` directory
   - Test each service independently

4. **Add new features**:
   - Use the new structure for all new code
   - Follow the established patterns

## Common Issues

### Import Errors

If you get import errors, make sure:
1. You're in the root directory (`MY_AI_AGENT/`)
2. Python can find the `src/` package
3. All `__init__.py` files exist

### Database Connection

The new `MongoDBConnection` utility uses singleton pattern.
All services share the same connection.

## Questions?

Check the documentation in `docs/` or refer to the original README files.
