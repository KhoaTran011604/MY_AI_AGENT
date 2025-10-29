"""
RAG Chatbot with MongoDB Knowledge Base
Uses sentence-transformers for embeddings (FREE)
Uses HuggingFace Inference API for LLM (FREE tier)
"""

import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from mongo_db import MongoDBManager

load_dotenv()


class RAGChatbot:
    def __init__(self, embedding_model="all-MiniLM-L6-v2", llm_model="mistralai/Mistral-7B-Instruct-v0.3"):
        """
        Initialize RAG Chatbot

        Args:
            embedding_model (str): Sentence transformer model for embeddings
            llm_model (str): HuggingFace model for text generation
        """
        print("Initializing RAG Chatbot...")

        # Initialize MongoDB
        self.db = MongoDBManager()
        if not self.db.connect():
            raise Exception("Failed to connect to MongoDB")

        # Initialize embedding model (runs locally - FREE)
        print(f"Loading embedding model: {embedding_model}...")
        self.embedding_model = SentenceTransformer(embedding_model)
        print("✓ Embedding model loaded")

        # Initialize HuggingFace client for LLM
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        if self.api_key:
            self.llm_client = InferenceClient(token=self.api_key)
        else:
            self.llm_client = InferenceClient()

        self.llm_model = llm_model

        # Cache for embeddings
        self.knowledge_cache = []
        self.embeddings_cache = []
        self._load_knowledge_cache()

        print("✓ RAG Chatbot initialized successfully!")

    def _load_knowledge_cache(self):
        """Load all knowledge with embeddings into cache"""
        print("Loading knowledge base into cache...")

        all_knowledge = self.db.get_all_knowledge()

        for doc in all_knowledge:
            # Generate embedding if not exists
            if doc.get("embedding") is None:
                text = f"{doc['question']} {doc['answer']}"
                embedding = self.embedding_model.encode(text).tolist()
                self.db.update_knowledge_embedding(str(doc['_id']), embedding)
                doc['embedding'] = embedding

            if doc.get("embedding"):
                self.knowledge_cache.append(doc)
                self.embeddings_cache.append(doc['embedding'])

        print(f"✓ Loaded {len(self.knowledge_cache)} knowledge items into cache")

    def add_knowledge(self, question, answer, category="general", tags=None):
        """
        Add new knowledge to the database

        Args:
            question (str): Question or topic
            answer (str): Answer or content
            category (str): Category
            tags (list): Tags

        Returns:
            str: Document ID
        """
        # Add to database
        doc_id = self.db.add_knowledge(question, answer, category, tags)

        # Generate embedding
        text = f"{question} {answer}"
        embedding = self.embedding_model.encode(text).tolist()

        # Update embedding in database
        self.db.update_knowledge_embedding(doc_id, embedding)

        # Update cache
        doc = {
            "_id": doc_id,
            "question": question,
            "answer": answer,
            "category": category,
            "tags": tags,
            "embedding": embedding
        }
        self.knowledge_cache.append(doc)
        self.embeddings_cache.append(embedding)

        print(f"✓ Added knowledge: {question[:50]}...")
        return doc_id

    def retrieve_relevant_knowledge(self, query, top_k=3):
        """
        Retrieve most relevant knowledge for a query

        Args:
            query (str): User query
            top_k (int): Number of top results to return

        Returns:
            list: Top-k relevant knowledge documents
        """
        if not self.knowledge_cache:
            return []

        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).reshape(1, -1)

        # Calculate similarities
        embeddings_matrix = np.array(self.embeddings_cache)
        similarities = cosine_similarity(query_embedding, embeddings_matrix)[0]

        # Get top-k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        # Return relevant documents with scores
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.2:  # Threshold for relevance
                doc = self.knowledge_cache[idx].copy()
                doc['similarity_score'] = float(similarities[idx])
                results.append(doc)

        return results

    def generate_response(self, query, context_docs):
        """
        Generate response using LLM with retrieved context

        Args:
            query (str): User query
            context_docs (list): Retrieved relevant documents

        Returns:
            str: Generated response
        """
        # Build context from retrieved documents
        context = ""
        if context_docs:
            context = "Context information:\n"
            for i, doc in enumerate(context_docs, 1):
                context += f"\n{i}. Q: {doc['question']}\n   A: {doc['answer']}\n"

        # Build prompt
        prompt = f"""You are a helpful assistant. Use the provided context to answer the user's question accurately.

{context}

User Question: {query}

Answer: """

        try:
            # Generate response using HuggingFace API
            messages = [{"role": "user", "content": prompt}]

            response = self.llm_client.chat_completion(
                messages=messages,
                model=self.llm_model,
                max_tokens=500,
                temperature=0.7
            )

            # Extract response
            if hasattr(response, 'choices') and len(response.choices) > 0:
                answer = response.choices[0].message.content
            else:
                answer = str(response)

            return answer.strip()

        except Exception as e:
            # Fallback: return context-based answer if API fails
            if context_docs:
                return f"Based on my knowledge: {context_docs[0]['answer']}"
            return f"I apologize, but I encountered an error: {str(e)}"

    def chat(self, user_message, session_id=None, save_to_db=True):
        """
        Main chat function with RAG

        Args:
            user_message (str): User's message
            session_id (str): Session identifier
            save_to_db (bool): Whether to save conversation to database

        Returns:
            dict: Response with answer and context
        """
        # Step 1: Retrieve relevant knowledge
        relevant_docs = self.retrieve_relevant_knowledge(user_message, top_k=3)

        # Step 2: Generate response
        response = self.generate_response(user_message, relevant_docs)

        # Step 3: Save conversation
        if save_to_db and session_id:
            context = {
                "retrieved_docs": len(relevant_docs),
                "top_similarity": relevant_docs[0]['similarity_score'] if relevant_docs else 0
            }
            self.db.save_conversation(session_id, user_message, response, context)

        return {
            "response": response,
            "relevant_knowledge": [
                {
                    "question": doc['question'],
                    "answer": doc['answer'],
                    "similarity": doc['similarity_score']
                }
                for doc in relevant_docs
            ],
            "used_knowledge_base": len(relevant_docs) > 0
        }

    def refresh_knowledge_cache(self):
        """Reload knowledge cache from database"""
        self.knowledge_cache = []
        self.embeddings_cache = []
        self._load_knowledge_cache()

    def get_statistics(self):
        """Get chatbot statistics"""
        db_stats = self.db.get_statistics()
        return {
            **db_stats,
            "cached_knowledge": len(self.knowledge_cache),
            "embedding_model": self.embedding_model.get_sentence_embedding_dimension(),
            "llm_model": self.llm_model
        }

    def close(self):
        """Close database connection"""
        self.db.close()


if __name__ == "__main__":
    # Test RAG Chatbot
    print("\n" + "="*60)
    print("RAG CHATBOT TEST")
    print("="*60 + "\n")

    try:
        # Initialize chatbot
        bot = RAGChatbot()

        # Show statistics
        stats = bot.get_statistics()
        print(f"\nChatbot Statistics:")
        print(f"  Knowledge Base: {stats['total_knowledge']} items")
        print(f"  Cached: {stats['cached_knowledge']} items")
        print(f"  Embedding Dimension: {stats['embedding_model']}")

        # Test chat
        print("\n" + "="*60)
        print("Type 'quit' to exit, 'add' to add knowledge, 'stats' for statistics")
        print("="*60 + "\n")

        while True:
            user_input = input("You: ").strip()

            if user_input.lower() == 'quit':
                print("Goodbye!")
                break

            elif user_input.lower() == 'stats':
                stats = bot.get_statistics()
                print(f"\nStatistics: {stats}\n")
                continue

            elif user_input.lower() == 'add':
                print("\nAdding new knowledge:")
                question = input("Question: ")
                answer = input("Answer: ")
                category = input("Category (default: general): ") or "general"
                bot.add_knowledge(question, answer, category)
                print("✓ Knowledge added!\n")
                continue

            elif not user_input:
                continue

            # Chat
            result = bot.chat(user_input, session_id="test-session")

            print(f"\nBot: {result['response']}")

            if result['relevant_knowledge']:
                print(f"\n[Used {len(result['relevant_knowledge'])} knowledge item(s)]")
                for i, doc in enumerate(result['relevant_knowledge'], 1):
                    print(f"  {i}. {doc['question']} (similarity: {doc['similarity']:.2f})")

            print()

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n✗ Error: {e}")
    finally:
        if 'bot' in locals():
            bot.close()