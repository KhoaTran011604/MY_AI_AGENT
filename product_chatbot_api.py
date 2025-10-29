"""
REST API for Product Consultation Chatbot
E-commerce chatbot API for frontend integration
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from product_chatbot import ProductChatbot
from product_manager import ProductManager
import uuid

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize chatbot
chatbot = None
product_manager = None


def get_chatbot():
    """Get or initialize chatbot"""
    global chatbot
    if chatbot is None:
        try:
            chatbot = ProductChatbot()
        except Exception as e:
            print(f"Failed to initialize chatbot: {e}")
            raise
    return chatbot


def get_product_manager():
    """Get product manager instance"""
    global product_manager
    if product_manager is None:
        product_manager = ProductManager()
        product_manager.connect()
    return product_manager


@app.route('/health', methods=['GET'])
def health_check():
    """Health check"""
    try:
        bot = get_chatbot()
        stats = bot.get_statistics()
        return jsonify({
            'status': 'healthy',
            'total_products': stats['total_products'],
            'in_stock': stats['in_stock']
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat with product consultation bot

    Request:
    {
        "message": "Tìm laptop dưới 20 triệu",
        "session_id": "optional"
    }

    Response:
    {
        "response": "bot response",
        "products": [...],
        "found_products": true,
        "session_id": "session-id",
        "status": "success"
    }
    """
    try:
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({
                'error': 'Missing required field: message',
                'status': 'error'
            }), 400

        user_message = data['message']
        session_id = data.get('session_id', str(uuid.uuid4()))

        bot = get_chatbot()
        result = bot.chat(user_message, session_id=session_id)

        return jsonify({
            **result,
            'session_id': session_id,
            'status': 'success'
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/products/add', methods=['POST'])
def add_product():
    """
    Add new product

    Request:
    {
        "name": "iPhone 15 Pro",
        "description": "...",
        "category": "Điện thoại",
        "brand": "Apple",
        "price": 28990000,
        "currency": "VND",
        "stock": 50,
        "specifications": {...},
        "images": [...],
        "rating": 4.8,
        "tags": [...]
    }

    Response:
    {
        "product_id": "id",
        "status": "success"
    }
    """
    try:
        data = request.get_json()

        required_fields = ['name', 'description', 'category', 'brand', 'price']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}',
                    'status': 'error'
                }), 400

        bot = get_chatbot()
        product_id = bot.add_product(
            name=data['name'],
            description=data['description'],
            category=data['category'],
            brand=data['brand'],
            price=data['price'],
            currency=data.get('currency', 'VND'),
            stock=data.get('stock', 0),
            specifications=data.get('specifications'),
            images=data.get('images'),
            rating=data.get('rating', 0.0),
            tags=data.get('tags')
        )

        return jsonify({
            'product_id': product_id,
            'status': 'success',
            'message': 'Product added successfully'
        }), 201

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/products/search', methods=['POST'])
def search_products():
    """
    Search products

    Request:
    {
        "query": "laptop gaming",
        "top_k": 5,
        "filters": {
            "category": "Laptop",
            "brand": "ASUS",
            "min_price": 10000000,
            "max_price": 30000000,
            "in_stock_only": true
        }
    }

    Response:
    {
        "products": [...],
        "count": 5,
        "status": "success"
    }
    """
    try:
        data = request.get_json()

        if not data or 'query' not in data:
            return jsonify({
                'error': 'Missing required field: query',
                'status': 'error'
            }), 400

        query = data['query']
        top_k = data.get('top_k', 5)
        filters = data.get('filters')

        bot = get_chatbot()
        products = bot.search_products(query, top_k=top_k, filters=filters)

        return jsonify({
            'products': [
                {
                    'id': str(p['_id']),
                    'name': p['name'],
                    'category': p['category'],
                    'brand': p['brand'],
                    'price': p['price'],
                    'price_formatted': bot._format_price(p['price'], p['currency']),
                    'description': p['description'],
                    'specifications': p.get('specifications', {}),
                    'rating': p.get('rating', 0),
                    'stock': p['stock'],
                    'in_stock': p['stock'] > 0,
                    'images': p.get('images', []),
                    'similarity': p['similarity_score']
                }
                for p in products
            ],
            'count': len(products),
            'status': 'success'
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/products/list', methods=['GET'])
def list_products():
    """
    List all products with filters

    Query params:
    - category: filter by category
    - brand: filter by brand

    Response:
    {
        "products": [...],
        "count": 50,
        "status": "success"
    }
    """
    try:
        category = request.args.get('category')
        brand = request.args.get('brand')

        pm = get_product_manager()
        products = pm.get_all_products(category=category, brand=brand)

        return jsonify({
            'products': [
                {
                    'id': str(p['_id']),
                    'name': p['name'],
                    'category': p['category'],
                    'brand': p['brand'],
                    'price': p['price'],
                    'currency': p['currency'],
                    'description': p['description'],
                    'specifications': p.get('specifications', {}),
                    'rating': p.get('rating', 0),
                    'stock': p['stock'],
                    'in_stock': p['stock'] > 0,
                    'images': p.get('images', []),
                    'tags': p.get('tags', [])
                }
                for p in products
            ],
            'count': len(products),
            'status': 'success'
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """
    Get product details by ID

    Response:
    {
        "product": {...},
        "status": "success"
    }
    """
    try:
        pm = get_product_manager()
        product = pm.get_product_by_id(product_id)

        if not product:
            return jsonify({
                'error': 'Product not found',
                'status': 'error'
            }), 404

        return jsonify({
            'product': {
                'id': str(product['_id']),
                'name': product['name'],
                'category': product['category'],
                'brand': product['brand'],
                'price': product['price'],
                'currency': product['currency'],
                'description': product['description'],
                'specifications': product.get('specifications', {}),
                'rating': product.get('rating', 0),
                'stock': product['stock'],
                'in_stock': product['stock'] > 0,
                'images': product.get('images', []),
                'tags': product.get('tags', [])
            },
            'status': 'success'
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/products/categories', methods=['GET'])
def get_categories():
    """
    Get all product categories

    Response:
    {
        "categories": ["Laptop", "Điện thoại", ...],
        "count": 5,
        "status": "success"
    }
    """
    try:
        pm = get_product_manager()
        categories = pm.get_categories()

        return jsonify({
            'categories': categories,
            'count': len(categories),
            'status': 'success'
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/products/brands', methods=['GET'])
def get_brands():
    """
    Get all brands

    Response:
    {
        "brands": ["Apple", "Samsung", ...],
        "count": 10,
        "status": "success"
    }
    """
    try:
        pm = get_product_manager()
        brands = pm.get_brands()

        return jsonify({
            'brands': brands,
            'count': len(brands),
            'status': 'success'
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/products/top-rated', methods=['GET'])
def get_top_rated():
    """
    Get top-rated products

    Query params:
    - limit: number of products (default: 10)
    - category: filter by category

    Response:
    {
        "products": [...],
        "count": 10,
        "status": "success"
    }
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        category = request.args.get('category')

        pm = get_product_manager()
        products = pm.get_top_rated_products(limit=limit, category=category)

        return jsonify({
            'products': [
                {
                    'id': str(p['_id']),
                    'name': p['name'],
                    'category': p['category'],
                    'brand': p['brand'],
                    'price': p['price'],
                    'rating': p.get('rating', 0),
                    'stock': p['stock'],
                    'images': p.get('images', [])
                }
                for p in products
            ],
            'count': len(products),
            'status': 'success'
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    Get database statistics

    Response:
    {
        "total_products": 100,
        "in_stock": 85,
        "out_of_stock": 15,
        "categories": [...],
        "brands": [...],
        "price_range": {...},
        "status": "success"
    }
    """
    try:
        bot = get_chatbot()
        stats = bot.get_statistics()

        return jsonify({
            **stats,
            'status': 'success'
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/products/refresh', methods=['POST'])
def refresh_cache():
    """
    Refresh product cache

    Response:
    {
        "status": "success",
        "message": "Cache refreshed"
    }
    """
    try:
        bot = get_chatbot()
        bot.refresh_cache()

        return jsonify({
            'status': 'success',
            'message': 'Product cache refreshed successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error'
    }), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        'error': 'Internal server error',
        'status': 'error'
    }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'

    print("\n" + "="*60)
    print("PRODUCT CONSULTATION CHATBOT API")
    print("="*60)
    print(f"Port: {port}")
    print(f"Debug: {debug_mode}")
    print("\nEndpoints:")
    print("  GET  /health")
    print("  POST /api/chat - Chat với bot tư vấn")
    print("  POST /api/products/add - Thêm sản phẩm")
    print("  POST /api/products/search - Tìm kiếm sản phẩm")
    print("  GET  /api/products/list - Danh sách sản phẩm")
    print("  GET  /api/products/<id> - Chi tiết sản phẩm")
    print("  GET  /api/products/categories - Danh mục")
    print("  GET  /api/products/brands - Thương hiệu")
    print("  GET  /api/products/top-rated - Top sản phẩm")
    print("  GET  /api/statistics - Thống kê")
    print("  POST /api/products/refresh - Refresh cache")
    print("="*60 + "\n")

    print("Initializing chatbot...")
    try:
        get_chatbot()
        print("✓ Chatbot ready!\n")
    except Exception as e:
        print(f"✗ Failed: {e}\n")
        exit(1)

    app.run(host='0.0.0.0', port=port, debug=debug_mode)
