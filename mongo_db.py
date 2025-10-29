"""
MongoDB Database Manager for RAG Chatbot
Handles connection and operations with MongoDB
"""

import os
from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure, OperationFailure
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class MongoDBManager:
    def __init__(self):
        """Initialize MongoDB connection"""
        self.mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.db_name = os.getenv("MONGODB_DATABASE", "chatbot_db")
        self.client = None
        self.db = None
        self.knowledge_collection = None
        self.conversations_collection = None

    def connect(self):
        """
        Connect to MongoDB

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.admin.command('ping')

            self.db = self.client[self.db_name]
            self.knowledge_collection = self.db['knowledge_base']
            self.conversations_collection = self.db['conversations']

            # Create indexes
            self._create_indexes()

            print(f"✓ Connected to MongoDB: {self.db_name}")
            return True

        except ConnectionFailure as e:
            print(f"✗ Failed to connect to MongoDB: {e}")
            return False
        except Exception as e:
            print(f"✗ Error connecting to MongoDB: {e}")
            return False

    def _create_indexes(self):
        """Create necessary indexes for performance"""
        try:
            # Index for knowledge base
            self.knowledge_collection.create_index([("category", ASCENDING)])
            self.knowledge_collection.create_index([("tags", ASCENDING)])

            # Index for conversations
            self.conversations_collection.create_index([("session_id", ASCENDING)])
            self.conversations_collection.create_index([("timestamp", ASCENDING)])

        except OperationFailure as e:
            print(f"Warning: Could not create indexes: {e}")

    def add_knowledge(self, question, answer, category="general", tags=None, metadata=None):
        """
        Add knowledge to database

        Args:
            question (str): Question or topic
            answer (str): Answer or content
            category (str): Category of knowledge
            tags (list): List of tags
            metadata (dict): Additional metadata

        Returns:
            str: Inserted document ID
        """
        if tags is None:
            tags = []
        if metadata is None:
            metadata = {}

        document = {
            "question": question,
            "answer": answer,
            "category": category,
            "tags": tags,
            "metadata": metadata,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "embedding": None  # Will be filled by RAG system
        }

        result = self.knowledge_collection.insert_one(document)
        return str(result.inserted_id)

    def update_knowledge_embedding(self, doc_id, embedding):
        """
        Update embedding vector for a knowledge document

        Args:
            doc_id (str): Document ID
            embedding (list): Embedding vector
        """
        from bson.objectid import ObjectId

        self.knowledge_collection.update_one(
            {"_id": ObjectId(doc_id)},
            {"$set": {"embedding": embedding, "updated_at": datetime.utcnow()}}
        )

    def get_all_knowledge(self, category=None):
        """
        Get all knowledge documents

        Args:
            category (str): Filter by category (optional)

        Returns:
            list: List of knowledge documents
        """
        query = {}
        if category:
            query["category"] = category

        return list(self.knowledge_collection.find(query))

    def search_knowledge_by_keyword(self, keyword, limit=5):
        """
        Search knowledge by keyword (basic text search)

        Args:
            keyword (str): Search keyword
            limit (int): Maximum results

        Returns:
            list: Matching documents
        """
        query = {
            "$or": [
                {"question": {"$regex": keyword, "$options": "i"}},
                {"answer": {"$regex": keyword, "$options": "i"}},
                {"tags": {"$regex": keyword, "$options": "i"}}
            ]
        }

        return list(self.knowledge_collection.find(query).limit(limit))

    def get_knowledge_with_embeddings(self):
        """
        Get all knowledge documents that have embeddings

        Returns:
            list: Documents with embeddings
        """
        query = {"embedding": {"$ne": None}}
        return list(self.knowledge_collection.find(query))

    def save_conversation(self, session_id, user_message, bot_response, context=None):
        """
        Save conversation to database

        Args:
            session_id (str): Session identifier
            user_message (str): User's message
            bot_response (str): Bot's response
            context (dict): Additional context
        """
        conversation = {
            "session_id": session_id,
            "user_message": user_message,
            "bot_response": bot_response,
            "context": context or {},
            "timestamp": datetime.utcnow()
        }

        self.conversations_collection.insert_one(conversation)

    def get_conversation_history(self, session_id, limit=10):
        """
        Get conversation history for a session

        Args:
            session_id (str): Session identifier
            limit (int): Maximum messages to retrieve

        Returns:
            list: Conversation history
        """
        return list(
            self.conversations_collection
            .find({"session_id": session_id})
            .sort("timestamp", -1)
            .limit(limit)
        )

    def delete_knowledge(self, doc_id):
        """
        Delete a knowledge document

        Args:
            doc_id (str): Document ID
        """
        from bson.objectid import ObjectId
        self.knowledge_collection.delete_one({"_id": ObjectId(doc_id)})

    def get_statistics(self):
        """
        Get database statistics

        Returns:
            dict: Statistics
        """
        return {
            "total_knowledge": self.knowledge_collection.count_documents({}),
            "knowledge_with_embeddings": self.knowledge_collection.count_documents(
                {"embedding": {"$ne": None}}
            ),
            "total_conversations": self.conversations_collection.count_documents({}),
            "categories": self.knowledge_collection.distinct("category")
        }

    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("✓ MongoDB connection closed")


if __name__ == "__main__":
    # Test MongoDB connection
    print("Testing MongoDB connection...\n")

    db = MongoDBManager()

    if db.connect():
        print("\nDatabase connected successfully!")

        # Show statistics
        stats = db.get_statistics()
        print("\nDatabase Statistics:")
        print(f"  Total Knowledge: {stats['total_knowledge']}")
        print(f"  With Embeddings: {stats['knowledge_with_embeddings']}")
        print(f"  Total Conversations: {stats['total_conversations']}")
        print(f"  Categories: {stats['categories']}")

        db.close()
    else:
        print("\nFailed to connect to MongoDB!")
        print("Make sure MongoDB is running and connection string is correct in .env file")
