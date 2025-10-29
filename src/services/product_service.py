"""
Product Service
Business logic for product management
"""

from pymongo import ASCENDING, DESCENDING
from pymongo.errors import OperationFailure
from datetime import datetime
from bson.objectid import ObjectId
from pydantic import ValidationError

from src.config import settings
from src.models import create_product_document
from src.utils import MongoDBConnection


class ProductService:
    """
    Product Service - Handles all product-related operations
    """

    def __init__(self):
        """Initialize Product Service"""
        self.db_connection = MongoDBConnection()
        self.products_collection = None

    def connect(self):
        """
        Connect to MongoDB and initialize products collection

        Returns:
            bool: True if connected successfully
        """
        client, db = self.db_connection.connect()
        if db is not None:
            self.products_collection = db['products']
            self._create_indexes()
            return True
        return False

    def _create_indexes(self):
        """Create indexes for efficient queries"""
        if self.products_collection is None:
            return

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
        Add a new product to database with Pydantic validation

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

        Raises:
            ValueError: If validation fails
        """
        try:
            # Use Pydantic validation
            product = create_product_document(
                name=name,
                description=description,
                category=category,
                brand=brand,
                price=price,
                currency=currency,
                stock=stock,
                specifications=specifications,
                images=images,
                rating=rating,
                tags=tags
            )

            result = self.products_collection.insert_one(product)
            return str(result.inserted_id)

        except ValidationError as e:
            raise ValueError(f"Product validation failed: {e}")

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
        self.db_connection.close()


# Backward compatibility alias
ProductManager = ProductService
