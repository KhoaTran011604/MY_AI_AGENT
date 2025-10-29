"""
MY_AI_AGENT - Main Entry Point
E-commerce Product Consultation Chatbot API
"""

import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

from src.config import settings
from src.services import ProductService, ChatbotService

# Create Flask app
app = Flask(__name__)
CORS(app)

# Global instances
chatbot = None
product_service = None


def get_chatbot():
    """Get or initialize chatbot"""
    global chatbot
    if chatbot is None:
        try:
            chatbot = ChatbotService()
        except Exception as e:
            print(f"Failed to initialize chatbot: {e}")
            raise
    return chatbot


def get_product_service():
    """Get product service instance"""
    global product_service
    if product_service is None:
        product_service = ProductService()
        product_service.connect()
    return product_service


# ============================================================================
# API ROUTES
# ============================================================================

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
    """Chat with product consultation bot"""
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
    """Add new product"""
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
    """Search products"""
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
    """List all products with filters"""
    try:
        category = request.args.get('category')
        brand = request.args.get('brand')

        pm = get_product_service()
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
    """Get product details by ID"""
    try:
        pm = get_product_service()
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
    """Get all product categories"""
    try:
        pm = get_product_service()
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
    """Get all brands"""
    try:
        pm = get_product_service()
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
    """Get top-rated products"""
    try:
        limit = request.args.get('limit', 10, type=int)
        category = request.args.get('category')

        pm = get_product_service()
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
    """Get database statistics"""
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
    """Refresh product cache"""
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


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point"""
    # Display settings
    settings.display_settings()

    # Display endpoints
    print("API Endpoints:")
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
    print(f"{'='*60}\n")

    # Initialize chatbot
    print("Initializing chatbot...")
    try:
        get_chatbot()
        print("✓ Chatbot ready!\n")
    except Exception as e:
        print(f"✗ Failed: {e}\n")
        sys.exit(1)

    # Start server
    app.run(
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG
    )


if __name__ == '__main__':
    main()
