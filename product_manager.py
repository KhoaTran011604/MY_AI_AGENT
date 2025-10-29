"""
Product Manager for E-commerce Chatbot
Manages product database in MongoDB
"""

import os
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, OperationFailure
from dotenv import load_dotenv
from datetime import datetime
from bson.objectid import ObjectId

load_dotenv()


class ProductManager:
    def __init__(self):
        """Initialize Product Manager"""
        self.mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.db_name = os.getenv("MONGODB_DATABASE", "chatbot_db")
        self.client = None
        self.db = None
        self.products_collection = None

    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')

            self.db = self.client[self.db_name]
            self.products_collection = self.db['products']

            # Create indexes
            self._create_indexes()

            print(f"✓ Connected to MongoDB: {self.db_name}")
            return True

        except ConnectionFailure as e:
            print(f"✗ Failed to connect to MongoDB: {e}")
            return False
        except Exception as e:
            print(f"✗ Error: {e}")
            return False

    def _create_indexes(self):
        """Create indexes for efficient queries"""
        try:
            # Text index for search
            self.products_collection.create_index([
                ("name", "text"),
                ("description", "text"),
                ("category", "text"),
                ("brand", "text")
            ])

            # Regular indexes
            self.products_collection.create_index([("category", ASCENDING)])
            self.products_collection.create_index([("brand", ASCENDING)])
            self.products_collection.create_index([("price", ASCENDING)])
            self.products_collection.create_index([("rating", DESCENDING)])

        except OperationFailure as e:
            print(f"Warning: Could not create indexes: {e}")

    def add_product(self, name, description, category, brand, price,
                   currency="VND", stock=0, specifications=None,
                   images=None, rating=0.0, tags=None):
        """
        Add a new product to database

        Args:
            name (str): Product name
            description (str): Product description
            category (str): Product category
            brand (str): Brand name
            price (float): Product price
            currency (str): Currency code (default: VND)
            stock (int): Available stock
            specifications (dict): Product specs
            images (list): Image URLs
            rating (float): Product rating (0-5)
            tags (list): Product tags

        Returns:
            str: Product ID
        """
        if specifications is None:
            specifications = {}
        if images is None:
            images = []
        if tags is None:
            tags = []

        product = {
            "name": name,
            "description": description,
            "category": category,
            "brand": brand,
            "price": price,
            "currency": currency,
            "stock": stock,
            "specifications": specifications,
            "images": images,
            "rating": rating,
            "tags": tags,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "embedding": None  # Will be filled by RAG system
        }

        result = self.products_collection.insert_one(product)
        return str(result.inserted_id)

    def update_product_embedding(self, product_id, embedding):
        """Update product embedding vector"""
        self.products_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": {"embedding": embedding, "updated_at": datetime.utcnow()}}
        )

    def get_all_products(self, category=None, brand=None):
        """
        Get all products with optional filters

        Args:
            category (str): Filter by category
            brand (str): Filter by brand

        Returns:
            list: List of products
        """
        query = {}
        if category:
            query["category"] = category
        if brand:
            query["brand"] = brand

        return list(self.products_collection.find(query))

    def search_products_by_text(self, search_text, limit=10):
        """
        Full-text search for products

        Args:
            search_text (str): Search query
            limit (int): Max results

        Returns:
            list: Matching products
        """
        query = {"$text": {"$search": search_text}}
        projection = {"score": {"$meta": "textScore"}}

        return list(
            self.products_collection
            .find(query, projection)
            .sort([("score", {"$meta": "textScore"})])
            .limit(limit)
        )

    def search_by_price_range(self, min_price=None, max_price=None, category=None):
        """
        Search products by price range

        Args:
            min_price (float): Minimum price
            max_price (float): Maximum price
            category (str): Optional category filter

        Returns:
            list: Matching products
        """
        query = {}

        if min_price is not None or max_price is not None:
            query["price"] = {}
            if min_price is not None:
                query["price"]["$gte"] = min_price
            if max_price is not None:
                query["price"]["$lte"] = max_price

        if category:
            query["category"] = category

        return list(self.products_collection.find(query).sort("price", ASCENDING))

    def get_product_by_id(self, product_id):
        """Get product by ID"""
        try:
            return self.products_collection.find_one({"_id": ObjectId(product_id)})
        except:
            return None

    def get_products_by_category(self, category, limit=20):
        """Get products in a category"""
        return list(
            self.products_collection
            .find({"category": category})
            .sort("rating", DESCENDING)
            .limit(limit)
        )

    def get_products_by_brand(self, brand, limit=20):
        """Get products by brand"""
        return list(
            self.products_collection
            .find({"brand": brand})
            .sort("rating", DESCENDING)
            .limit(limit)
        )

    def get_top_rated_products(self, limit=10, category=None):
        """Get top-rated products"""
        query = {}
        if category:
            query["category"] = category

        return list(
            self.products_collection
            .find(query)
            .sort("rating", DESCENDING)
            .limit(limit)
        )

    def get_products_in_stock(self, category=None):
        """Get products that are in stock"""
        query = {"stock": {"$gt": 0}}
        if category:
            query["category"] = category

        return list(self.products_collection.find(query))

    def update_product_stock(self, product_id, new_stock):
        """Update product stock"""
        self.products_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": {"stock": new_stock, "updated_at": datetime.utcnow()}}
        )

    def get_categories(self):
        """Get all unique categories"""
        return self.products_collection.distinct("category")

    def get_brands(self):
        """Get all unique brands"""
        return self.products_collection.distinct("brand")

    def get_price_range(self, category=None):
        """Get min and max prices"""
        query = {}
        if category:
            query["category"] = category

        pipeline = [
            {"$match": query},
            {"$group": {
                "_id": None,
                "min_price": {"$min": "$price"},
                "max_price": {"$max": "$price"}
            }}
        ]

        result = list(self.products_collection.aggregate(pipeline))
        if result:
            return {
                "min": result[0]["min_price"],
                "max": result[0]["max_price"]
            }
        return {"min": 0, "max": 0}

    def get_statistics(self):
        """Get product database statistics"""
        return {
            "total_products": self.products_collection.count_documents({}),
            "products_with_embeddings": self.products_collection.count_documents(
                {"embedding": {"$ne": None}}
            ),
            "in_stock": self.products_collection.count_documents({"stock": {"$gt": 0}}),
            "out_of_stock": self.products_collection.count_documents({"stock": {"$lte": 0}}),
            "categories": self.get_categories(),
            "brands": self.get_brands(),
            "price_range": self.get_price_range()
        }

    def delete_product(self, product_id):
        """Delete a product"""
        self.products_collection.delete_one({"_id": ObjectId(product_id)})

    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("✓ MongoDB connection closed")


if __name__ == "__main__":
    # Test Product Manager
    print("\n" + "="*60)
    print("PRODUCT MANAGER TEST")
    print("="*60 + "\n")

    pm = ProductManager()

    if pm.connect():
        print("\n✓ Connected to database!")

        # Show statistics
        stats = pm.get_statistics()
        print("\nProduct Statistics:")
        print(f"  Total Products: {stats['total_products']}")
        print(f"  In Stock: {stats['in_stock']}")
        print(f"  Out of Stock: {stats['out_of_stock']}")
        print(f"  Categories: {', '.join(stats['categories']) if stats['categories'] else 'None'}")
        print(f"  Brands: {', '.join(stats['brands']) if stats['brands'] else 'None'}")
        print(f"  Price Range: {stats['price_range']['min']:,.0f} - {stats['price_range']['max']:,.0f} VND")

        pm.close()
    else:
        print("\n✗ Failed to connect!")
