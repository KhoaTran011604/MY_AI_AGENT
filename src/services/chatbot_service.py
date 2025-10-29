"""
Product Consultation Chatbot with RAG
Helps customers find and compare products from MongoDB
"""

import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from src.services.product_service import ProductService as ProductManager
import re

# Config loaded from settings


class ProductChatbot:
    def __init__(self, embedding_model="all-MiniLM-L6-v2", llm_model="mistralai/Mistral-7B-Instruct-v0.3"):
        """
        Initialize Product Consultation Chatbot

        Args:
            embedding_model (str): Sentence transformer model
            llm_model (str): HuggingFace model for generation
        """
        print("Initializing Product Chatbot...")

        # Initialize Product Manager
        self.product_manager = ProductManager()
        if not self.product_manager.connect():
            raise Exception("Failed to connect to MongoDB")

        # Initialize embedding model (local - FREE)
        print(f"Loading embedding model: {embedding_model}...")
        self.embedding_model = SentenceTransformer(embedding_model)
        print("✓ Embedding model loaded")

        # Initialize HuggingFace client
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        if self.api_key:
            self.llm_client = InferenceClient(token=self.api_key)
        else:
            self.llm_client = InferenceClient()

        self.llm_model = llm_model

        # Cache for product embeddings
        self.products_cache = []
        self.embeddings_cache = []
        self._load_products_cache()

        print("✓ Product Chatbot initialized successfully!")

    def _load_products_cache(self):
        """Load all products with embeddings into cache"""
        print("Loading products into cache...")

        all_products = self.product_manager.get_all_products()

        for product in all_products:
            # Generate embedding if not exists
            if product.get("embedding") is None:
                text = self._product_to_text(product)
                embedding = self.embedding_model.encode(text).tolist()
                self.product_manager.update_product_embedding(
                    str(product['_id']), embedding
                )
                product['embedding'] = embedding

            if product.get("embedding"):
                self.products_cache.append(product)
                self.embeddings_cache.append(product['embedding'])

        print(f"✓ Loaded {len(self.products_cache)} products into cache")

    def _product_to_text(self, product):
        """Convert product to searchable text"""
        text_parts = [
            f"Product: {product['name']}",
            f"Category: {product['category']}",
            f"Brand: {product['brand']}",
            f"Price: {product['price']:,.0f} {product['currency']}",
            f"Description: {product['description']}"
        ]

        # Add specifications
        if product.get('specifications'):
            specs = ", ".join([f"{k}: {v}" for k, v in product['specifications'].items()])
            text_parts.append(f"Specifications: {specs}")

        # Add tags
        if product.get('tags'):
            text_parts.append(f"Tags: {', '.join(product['tags'])}")

        return " | ".join(text_parts)

    def _format_price(self, price, currency="VND"):
        """Format price for display"""
        if currency == "VND":
            return f"{price:,.0f}đ"
        return f"{price:,.2f} {currency}"

    def add_product(self, name, description, category, brand, price,
                   currency="VND", stock=0, specifications=None,
                   images=None, rating=0.0, tags=None):
        """Add new product to database"""
        # Add to database
        product_id = self.product_manager.add_product(
            name, description, category, brand, price,
            currency, stock, specifications, images, rating, tags
        )

        # Generate embedding
        product = self.product_manager.get_product_by_id(product_id)
        text = self._product_to_text(product)
        embedding = self.embedding_model.encode(text).tolist()

        # Update embedding
        self.product_manager.update_product_embedding(product_id, embedding)

        # Update cache
        product['embedding'] = embedding
        self.products_cache.append(product)
        self.embeddings_cache.append(embedding)

        print(f"✓ Added product: {name}")
        return product_id

    def search_products(self, query, top_k=5, filters=None):
        """
        Search products by query with optional filters

        Args:
            query (str): Search query
            top_k (int): Number of results
            filters (dict): Optional filters (category, brand, price_range)

        Returns:
            list: Relevant products with similarity scores
        """
        if not self.products_cache:
            return []

        # Apply filters first
        filtered_products = self.products_cache
        filtered_embeddings = self.embeddings_cache

        if filters:
            filtered_products = []
            filtered_embeddings = []

            for i, product in enumerate(self.products_cache):
                include = True

                # Category filter
                if filters.get('category') and product['category'] != filters['category']:
                    include = False

                # Brand filter
                if filters.get('brand') and product['brand'] != filters['brand']:
                    include = False

                # Price range filter
                if filters.get('min_price') and product['price'] < filters['min_price']:
                    include = False
                if filters.get('max_price') and product['price'] > filters['max_price']:
                    include = False

                # Stock filter
                if filters.get('in_stock_only') and product['stock'] <= 0:
                    include = False

                if include:
                    filtered_products.append(product)
                    filtered_embeddings.append(self.embeddings_cache[i])

        if not filtered_products:
            return []

        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).reshape(1, -1)

        # Calculate similarities
        embeddings_matrix = np.array(filtered_embeddings)
        similarities = cosine_similarity(query_embedding, embeddings_matrix)[0]

        # Get top-k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        # Return results
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.2:  # Relevance threshold
                product = filtered_products[idx].copy()
                product['similarity_score'] = float(similarities[idx])
                results.append(product)

        return results

    def _extract_price_range(self, query):
        """Extract price range from query"""
        query_lower = query.lower()

        # Patterns for price
        patterns = [
            r'dưới\s+(\d+)\s*(triệu|tr|nghìn|k|m)',
            r'trên\s+(\d+)\s*(triệu|tr|nghìn|k|m)',
            r'từ\s+(\d+)\s*(triệu|tr|nghìn|k|m)\s+đến\s+(\d+)\s*(triệu|tr|nghìn|k|m)',
            r'(\d+)\s*(triệu|tr|nghìn|k|m)\s+đến\s+(\d+)\s*(triệu|tr|nghìn|k|m)',
        ]

        min_price = None
        max_price = None

        for pattern in patterns:
            match = re.search(pattern, query_lower)
            if match:
                groups = match.groups()

                if 'dưới' in query_lower:
                    value = float(groups[0])
                    unit = groups[1]
                    max_price = self._convert_to_vnd(value, unit)

                elif 'trên' in query_lower:
                    value = float(groups[0])
                    unit = groups[1]
                    min_price = self._convert_to_vnd(value, unit)

                elif len(groups) >= 4:
                    min_val = float(groups[0])
                    min_unit = groups[1]
                    max_val = float(groups[2])
                    max_unit = groups[3]
                    min_price = self._convert_to_vnd(min_val, min_unit)
                    max_price = self._convert_to_vnd(max_val, max_unit)
                break

        return min_price, max_price

    def _convert_to_vnd(self, value, unit):
        """Convert value with unit to VND"""
        unit = unit.lower()
        if unit in ['triệu', 'tr', 'm']:
            return value * 1000000
        elif unit in ['nghìn', 'k']:
            return value * 1000
        return value

    def chat(self, user_message, session_id=None):
        """
        Main chat function for product consultation

        Args:
            user_message (str): User's message
            session_id (str): Session ID

        Returns:
            dict: Response with products and answer
        """
        # Extract filters from query
        filters = {}

        # Extract price range
        min_price, max_price = self._extract_price_range(user_message)
        if min_price:
            filters['min_price'] = min_price
        if max_price:
            filters['max_price'] = max_price

        # Search for relevant products
        relevant_products = self.search_products(
            user_message,
            top_k=5,
            filters=filters if filters else None
        )

        # Generate response
        response = self._generate_consultation_response(
            user_message,
            relevant_products
        )

        return {
            "response": response,
            "products": [
                {
                    "id": str(product['_id']),
                    "name": product['name'],
                    "category": product['category'],
                    "brand": product['brand'],
                    "price": product['price'],
                    "price_formatted": self._format_price(product['price'], product['currency']),
                    "description": product['description'],
                    "specifications": product.get('specifications', {}),
                    "rating": product.get('rating', 0),
                    "stock": product['stock'],
                    "in_stock": product['stock'] > 0,
                    "images": product.get('images', []),
                    "similarity": product['similarity_score']
                }
                for product in relevant_products
            ],
            "found_products": len(relevant_products) > 0
        }

    def _generate_consultation_response(self, query, products):
        """Generate consultation response using LLM"""
        if not products:
            return "Xin lỗi, tôi không tìm thấy sản phẩm phù hợp với yêu cầu của bạn. Bạn có thể mô tả chi tiết hơn hoặc thay đổi tiêu chí tìm kiếm không?"

        # Build context from products
        context = "Danh sách sản phẩm phù hợp:\n\n"
        for i, product in enumerate(products, 1):
            context += f"{i}. **{product['name']}** ({product['brand']})\n"
            context += f"   - Giá: {self._format_price(product['price'], product['currency'])}\n"
            context += f"   - Danh mục: {product['category']}\n"
            context += f"   - Đánh giá: {product.get('rating', 0):.1f}/5.0\n"
            context += f"   - Tình trạng: {'Còn hàng' if product['stock'] > 0 else 'Hết hàng'}\n"
            context += f"   - Mô tả: {product['description'][:200]}...\n"

            if product.get('specifications'):
                specs = ", ".join([f"{k}: {v}" for k, v in list(product['specifications'].items())[:3]])
                context += f"   - Thông số: {specs}\n"
            context += "\n"

        # Build prompt
        prompt = f"""Bạn là một tư vấn viên bán hàng chuyên nghiệp và thân thiện. Nhiệm vụ của bạn là tư vấn sản phẩm cho khách hàng.

{context}

Câu hỏi của khách hàng: {query}

Hãy trả lời theo phong cách:
- Thân thiện và chuyên nghiệp
- Giới thiệu 2-3 sản phẩm phù hợp nhất
- So sánh ưu điểm của từng sản phẩm
- Đưa ra gợi ý dựa trên nhu cầu
- Kết thúc bằng câu hỏi để hiểu rõ hơn nhu cầu khách hàng

Trả lời bằng tiếng Việt:"""

        try:
            messages = [{"role": "user", "content": prompt}]

            response = self.llm_client.chat_completion(
                messages=messages,
                model=self.llm_model,
                max_tokens=600,
                temperature=0.7
            )

            if hasattr(response, 'choices') and len(response.choices) > 0:
                answer = response.choices[0].message.content
            else:
                answer = str(response)

            return answer.strip()

        except Exception as e:
            # Fallback response
            top_product = products[0]
            return f"""Dựa trên yêu cầu của bạn, tôi gợi ý sản phẩm **{top_product['name']}** của {top_product['brand']}.

Giá: {self._format_price(top_product['price'], top_product['currency'])}
Đánh giá: {top_product.get('rating', 0):.1f}/5.0

{top_product['description'][:300]}...

Tôi có tìm thấy thêm {len(products)-1} sản phẩm tương tự. Bạn có muốn xem chi tiết hơn về sản phẩm nào không?"""

    def get_statistics(self):
        """Get chatbot statistics"""
        return self.product_manager.get_statistics()

    def refresh_cache(self):
        """Reload product cache"""
        self.products_cache = []
        self.embeddings_cache = []
        self._load_products_cache()

    def close(self):
        """Close connections"""
        self.product_manager.close()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("PRODUCT CONSULTATION CHATBOT")
    print("="*60 + "\n")

    try:
        bot = ProductChatbot()

        stats = bot.get_statistics()
        print(f"\nProduct Database:")
        print(f"  Total Products: {stats['total_products']}")
        print(f"  In Stock: {stats['in_stock']}")
        print(f"  Categories: {', '.join(stats['categories']) if stats['categories'] else 'None'}")

        print("\n" + "="*60)
        print("Commands: 'quit' to exit | 'stats' for statistics")
        print("="*60 + "\n")

        while True:
            user_input = input("Bạn: ").strip()

            if user_input.lower() == 'quit':
                print("Cảm ơn bạn đã sử dụng dịch vụ!")
                break

            elif user_input.lower() == 'stats':
                stats = bot.get_statistics()
                print(f"\n{stats}\n")
                continue

            elif not user_input:
                continue

            # Chat
            result = bot.chat(user_input)

            print(f"\nBot: {result['response']}\n")

            if result['products']:
                print(f"[Tìm thấy {len(result['products'])} sản phẩm phù hợp]\n")

    except KeyboardInterrupt:
        print("\n\nĐã dừng!")
    except Exception as e:
        print(f"\n✗ Lỗi: {e}")
    finally:
        if 'bot' in locals():
            bot.close()


# Backward compatibility alias
ProductChatbot = ProductChatbot if 'ProductChatbot' in dir() else type('ProductChatbot', (), {})
