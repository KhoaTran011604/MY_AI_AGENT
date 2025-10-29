"""
Seed sample data to MongoDB for RAG Chatbot
Run this script to populate your knowledge base with sample data
"""

from chatbot_rag import RAGChatbot


def seed_sample_data():
    """Add sample knowledge to the database"""

    print("\n" + "="*60)
    print("SEEDING SAMPLE DATA TO MONGODB")
    print("="*60 + "\n")

    try:
        # Initialize chatbot
        print("Initializing chatbot...")
        bot = RAGChatbot()

        # Sample knowledge data
        sample_knowledge = [
            # Programming
            {
                "question": "What is Python?",
                "answer": "Python is a high-level, interpreted programming language known for its simplicity and readability. It supports multiple programming paradigms including procedural, object-oriented, and functional programming. Python is widely used in web development, data science, machine learning, automation, and more.",
                "category": "programming",
                "tags": ["python", "programming", "language"]
            },
            {
                "question": "What is JavaScript?",
                "answer": "JavaScript is a versatile programming language primarily used for web development. It enables interactive web pages and runs in web browsers. With Node.js, JavaScript can also be used for server-side development. It's a key technology alongside HTML and CSS for creating modern web applications.",
                "category": "programming",
                "tags": ["javascript", "web", "programming"]
            },
            {
                "question": "What is an API?",
                "answer": "API stands for Application Programming Interface. It's a set of rules and protocols that allows different software applications to communicate with each other. APIs define the methods and data formats that applications can use to request and exchange information. RESTful APIs are commonly used for web services.",
                "category": "programming",
                "tags": ["api", "rest", "web-services"]
            },
            {
                "question": "What is Git?",
                "answer": "Git is a distributed version control system used to track changes in source code during software development. It allows multiple developers to work together on the same project, maintaining a history of changes and enabling easy collaboration. GitHub, GitLab, and Bitbucket are popular platforms that host Git repositories.",
                "category": "programming",
                "tags": ["git", "version-control", "development"]
            },
            {
                "question": "What is Docker?",
                "answer": "Docker is a platform that uses containerization technology to package applications and their dependencies into portable containers. These containers can run consistently across different computing environments. Docker simplifies deployment, scaling, and ensures that applications run the same way in development, testing, and production.",
                "category": "devops",
                "tags": ["docker", "containers", "devops"]
            },

            # Database
            {
                "question": "What is MongoDB?",
                "answer": "MongoDB is a popular NoSQL document database that stores data in flexible, JSON-like documents. Unlike traditional relational databases, MongoDB doesn't require a fixed schema, making it ideal for handling unstructured or semi-structured data. It's designed for scalability and high performance, supporting horizontal scaling through sharding.",
                "category": "database",
                "tags": ["mongodb", "nosql", "database"]
            },
            {
                "question": "What is SQL?",
                "answer": "SQL (Structured Query Language) is a standard programming language for managing and manipulating relational databases. It's used to create, read, update, and delete data (CRUD operations). SQL databases like MySQL, PostgreSQL, and SQL Server organize data in tables with predefined relationships between them.",
                "category": "database",
                "tags": ["sql", "database", "query"]
            },

            # Machine Learning
            {
                "question": "What is Machine Learning?",
                "answer": "Machine Learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It uses algorithms to analyze data, identify patterns, and make decisions. Common types include supervised learning, unsupervised learning, and reinforcement learning.",
                "category": "machine-learning",
                "tags": ["ml", "ai", "data-science"]
            },
            {
                "question": "What is RAG in AI?",
                "answer": "RAG (Retrieval-Augmented Generation) is a technique that enhances Large Language Models by retrieving relevant information from a knowledge base before generating responses. It combines information retrieval with text generation, allowing the model to provide more accurate and contextual answers based on specific domain knowledge.",
                "category": "machine-learning",
                "tags": ["rag", "llm", "ai", "nlp"]
            },
            {
                "question": "What are embeddings?",
                "answer": "Embeddings are numerical representations of data (text, images, etc.) in a continuous vector space. In NLP, word embeddings capture semantic meaning where similar words have similar vector representations. Models like Word2Vec, GloVe, and sentence transformers create these embeddings, enabling machines to understand and process human language.",
                "category": "machine-learning",
                "tags": ["embeddings", "nlp", "vectors"]
            },

            # Web Development
            {
                "question": "What is React?",
                "answer": "React is a popular JavaScript library for building user interfaces, maintained by Meta (Facebook). It uses a component-based architecture where UI is broken down into reusable components. React uses a virtual DOM for efficient updates and supports modern features like hooks for state management and side effects.",
                "category": "web-development",
                "tags": ["react", "javascript", "frontend"]
            },
            {
                "question": "What is Flask?",
                "answer": "Flask is a lightweight Python web framework that's easy to learn and use. It's considered a micro-framework because it doesn't require particular tools or libraries. Flask is great for building APIs, small to medium web applications, and prototypes. It gives developers flexibility in choosing components and tools.",
                "category": "web-development",
                "tags": ["flask", "python", "backend", "api"]
            },
            {
                "question": "What is REST API?",
                "answer": "REST (Representational State Transfer) API is an architectural style for designing networked applications. It uses HTTP methods (GET, POST, PUT, DELETE) to perform operations on resources identified by URLs. REST APIs are stateless, scalable, and widely used for web services. They typically return data in JSON or XML format.",
                "category": "web-development",
                "tags": ["rest", "api", "http", "web-services"]
            },

            # General Tech
            {
                "question": "What is Cloud Computing?",
                "answer": "Cloud Computing is the delivery of computing services (servers, storage, databases, networking, software) over the internet. It offers flexibility, scalability, and cost-efficiency. Major providers include AWS, Google Cloud, and Microsoft Azure. Cloud services are typically categorized as IaaS, PaaS, or SaaS.",
                "category": "general",
                "tags": ["cloud", "aws", "azure", "infrastructure"]
            },
            {
                "question": "What is CI/CD?",
                "answer": "CI/CD stands for Continuous Integration and Continuous Deployment/Delivery. It's a DevOps practice that automates the software development lifecycle. CI involves automatically testing code changes, while CD automates deployment to production. This approach enables faster, more reliable software releases with reduced manual errors.",
                "category": "devops",
                "tags": ["cicd", "devops", "automation"]
            }
        ]

        # Add knowledge to database
        print(f"Adding {len(sample_knowledge)} knowledge items...\n")

        for i, item in enumerate(sample_knowledge, 1):
            doc_id = bot.add_knowledge(
                question=item['question'],
                answer=item['answer'],
                category=item['category'],
                tags=item['tags']
            )
            print(f"  [{i}/{len(sample_knowledge)}] Added: {item['question']}")

        print("\n" + "="*60)
        print("SEEDING COMPLETED")
        print("="*60)

        # Show statistics
        stats = bot.get_statistics()
        print(f"\nDatabase Statistics:")
        print(f"  Total Knowledge: {stats['total_knowledge']}")
        print(f"  Cached Items: {stats['cached_knowledge']}")
        print(f"  Categories: {', '.join(stats['categories'])}")

        print("\n✓ Sample data seeded successfully!")
        print("\nYou can now:")
        print("  1. Run: python chatbot_rag.py (for CLI chat)")
        print("  2. Run: python chatbot_rag_api.py (for API server)")

        bot.close()

    except Exception as e:
        print(f"\n✗ Error seeding data: {e}")
        print("\nPlease check:")
        print("  1. MongoDB is running")
        print("  2. MONGODB_URI in .env is correct")
        print("  3. All dependencies are installed")


if __name__ == "__main__":
    seed_sample_data()
