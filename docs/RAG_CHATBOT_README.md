# RAG Chatbot with MongoDB - Complete Guide

## Tổng quan

RAG (Retrieval-Augmented Generation) Chatbot là chatbot thông minh có khả năng:
- **Training**: Học từ dữ liệu trong MongoDB
- **Retrieval**: Tìm kiếm thông tin liên quan từ knowledge base
- **Generation**: Tạo câu trả lời dựa trên context

### Công nghệ sử dụng (Option B - Hybrid FREE)

| Component | Technology | Chi phí | Mô tả |
|-----------|-----------|---------|-------|
| **Database** | MongoDB | FREE | Lưu trữ knowledge base |
| **Embeddings** | sentence-transformers | FREE | Chuyển text thành vectors (local) |
| **LLM** | HuggingFace API | FREE* | Text generation (1000 req/day miễn phí) |
| **API Server** | Flask | FREE | REST API cho frontend |
| **Search** | Cosine Similarity | FREE | Tìm kiếm semantic |

*FREE tier: 1000 requests/ngày, sau đó ~$5-10/tháng

---

## Kiến trúc hệ thống

```
┌─────────────┐
│  Frontend   │
│   (React)   │
└──────┬──────┘
       │ HTTP Requests
       ↓
┌─────────────────────────────────────┐
│     Flask API (chatbot_rag_api.py)  │
└──────┬──────────────────────────────┘
       │
       ↓
┌─────────────────────────────────────┐
│   RAG Chatbot (chatbot_rag.py)      │
│   ┌─────────────────────────────┐   │
│   │  1. Query Embedding         │   │
│   │  2. Similarity Search       │   │
│   │  3. Context Retrieval       │   │
│   │  4. LLM Generation          │   │
│   └─────────────────────────────┘   │
└──────┬────────────────────┬─────────┘
       │                    │
       ↓                    ↓
┌─────────────┐    ┌─────────────────┐
│   MongoDB   │    │ HuggingFace API │
│ Knowledge   │    │      (LLM)      │
│    Base     │    └─────────────────┘
└─────────────┘
```

---

## Cài đặt

### 1. Cài đặt MongoDB

**Windows:**
```bash
# Download từ: https://www.mongodb.com/try/download/community
# Hoặc dùng Chocolatey:
choco install mongodb

# Start MongoDB
mongod --dbpath="C:\data\db"
```

**Mac:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Linux:**
```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
```

### 2. Cài đặt Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình .env

Tạo file `.env` với nội dung:

```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=chatbot_db

# HuggingFace API Key
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# API Server Configuration
PORT=5000
DEBUG=False
```

**Lấy HuggingFace API Key:**
1. Đăng ký tại: https://huggingface.co/
2. Vào Settings → Access Tokens
3. Tạo token mới và copy vào .env

### 4. Seed dữ liệu mẫu

```bash
python seed_data.py
```

---

## Sử dụng

### Option 1: Command Line Interface (CLI)

Chạy chatbot trực tiếp từ terminal:

```bash
python chatbot_rag.py
```

**Commands:**
- Gõ câu hỏi để chat
- `add` - Thêm knowledge mới
- `stats` - Xem thống kê
- `quit` - Thoát

**Ví dụ:**
```
You: What is Python?
Bot: Python is a high-level, interpreted programming language...

[Used 1 knowledge item(s)]
  1. What is Python? (similarity: 0.89)
```

### Option 2: API Server

Chạy REST API server:

```bash
python chatbot_rag_api.py
```

Server sẽ chạy tại: `http://localhost:5000`

---

## API Documentation

### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "knowledge_items": 15,
  "active_sessions": 3
}
```

---

### 2. Chat với Bot
```http
POST /api/chat
Content-Type: application/json

{
  "message": "What is RAG in AI?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "RAG (Retrieval-Augmented Generation) is...",
  "relevant_knowledge": [
    {
      "question": "What is RAG in AI?",
      "answer": "RAG is a technique...",
      "similarity": 0.95
    }
  ],
  "used_knowledge_base": true,
  "session_id": "abc-123",
  "status": "success"
}
```

---

### 3. Thêm Knowledge
```http
POST /api/knowledge/add
Content-Type: application/json

{
  "question": "What is Vue.js?",
  "answer": "Vue.js is a progressive JavaScript framework...",
  "category": "web-development",
  "tags": ["vue", "javascript", "frontend"]
}
```

**Response:**
```json
{
  "doc_id": "507f1f77bcf86cd799439011",
  "status": "success",
  "message": "Knowledge added successfully"
}
```

---

### 4. Tìm kiếm Knowledge
```http
POST /api/knowledge/search
Content-Type: application/json

{
  "query": "python programming",
  "top_k": 5
}
```

**Response:**
```json
{
  "results": [
    {
      "question": "What is Python?",
      "answer": "Python is...",
      "category": "programming",
      "similarity": 0.87
    }
  ],
  "count": 5,
  "status": "success"
}
```

---

### 5. Danh sách Knowledge
```http
GET /api/knowledge/list?category=programming
```

**Response:**
```json
{
  "knowledge": [
    {
      "id": "507f1f77bcf86cd799439011",
      "question": "What is Python?",
      "answer": "Python is...",
      "category": "programming",
      "tags": ["python", "language"],
      "has_embedding": true
    }
  ],
  "count": 10,
  "status": "success"
}
```

---

### 6. Refresh Cache
```http
POST /api/knowledge/refresh
```

Reload knowledge từ database vào cache.

---

### 7. Xem Statistics
```http
GET /api/statistics
```

**Response:**
```json
{
  "total_knowledge": 15,
  "cached_knowledge": 15,
  "total_conversations": 50,
  "embedding_model": 384,
  "llm_model": "mistralai/Mistral-7B-Instruct-v0.3",
  "active_sessions": 5,
  "status": "success"
}
```

---

### 8. Lịch sử Chat
```http
GET /api/session/{session_id}/history?limit=10
```

**Response:**
```json
{
  "history": [
    {
      "user_message": "What is Python?",
      "bot_response": "Python is...",
      "timestamp": "2025-10-29T10:30:00",
      "context": {
        "retrieved_docs": 3,
        "top_similarity": 0.89
      }
    }
  ],
  "count": 10,
  "status": "success"
}
```

---

## Frontend Integration

### React Example

```javascript
import { useState, useEffect } from 'react';
import axios from 'axios';

function RAGChatbot() {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const API_URL = 'http://localhost:5000';

  // Initialize session
  useEffect(() => {
    const savedSession = localStorage.getItem('chat_session_id');
    if (savedSession) {
      setSessionId(savedSession);
    }
  }, []);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setLoading(true);
    try {
      const { data } = await axios.post(`${API_URL}/api/chat`, {
        message: input,
        session_id: sessionId
      });

      // Save session ID
      if (!sessionId) {
        setSessionId(data.session_id);
        localStorage.setItem('chat_session_id', data.session_id);
      }

      // Update messages
      setMessages(prev => [
        ...prev,
        { role: 'user', content: input },
        {
          role: 'assistant',
          content: data.response,
          knowledge: data.relevant_knowledge
        }
      ]);

      setInput('');
    } catch (error) {
      console.error('Chat error:', error);
    }
    setLoading(false);
  };

  return (
    <div className="chatbot">
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <p>{msg.content}</p>
            {msg.knowledge && msg.knowledge.length > 0 && (
              <div className="knowledge-used">
                <small>
                  Used {msg.knowledge.length} knowledge item(s)
                </small>
              </div>
            )}
          </div>
        ))}
      </div>

      <form onSubmit={sendMessage}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me anything..."
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Thinking...' : 'Send'}
        </button>
      </form>
    </div>
  );
}

export default RAGChatbot;
```

---

## Cách thức hoạt động

### 1. Thêm Knowledge (Training)

```python
# Khi thêm knowledge mới:
bot.add_knowledge(
    question="What is FastAPI?",
    answer="FastAPI is a modern Python web framework...",
    category="web-development",
    tags=["python", "api"]
)

# Hệ thống sẽ:
# 1. Lưu vào MongoDB
# 2. Tạo embedding vector (sentence-transformers)
# 3. Cập nhật cache
```

### 2. Chat Process (RAG Pipeline)

```
User Query: "Tell me about Python"
        ↓
[1] Encode Query → Vector [0.12, -0.45, 0.67, ...]
        ↓
[2] Search MongoDB → Find similar vectors (cosine similarity)
        ↓
[3] Retrieve Top-K Documents
    - "What is Python?" (similarity: 0.89)
    - "Python features" (similarity: 0.75)
        ↓
[4] Build Context + Prompt
        ↓
[5] Send to LLM (HuggingFace API)
        ↓
[6] Generate Response
        ↓
[7] Save to MongoDB + Return to User
```

### 3. Embeddings & Similarity

```python
# Text → Vector
"What is Python?" → [0.12, -0.45, 0.67, 0.23, ...]
"Python programming" → [0.15, -0.42, 0.69, 0.25, ...]

# Cosine Similarity
similarity = cosine(vector1, vector2)
# High similarity (0.8-1.0) = Very related
# Low similarity (0.0-0.3) = Not related
```

---

## Best Practices

### 1. Knowledge Base Design

**Good:**
```json
{
  "question": "What is Docker?",
  "answer": "Docker is a containerization platform...",
  "category": "devops",
  "tags": ["docker", "containers"]
}
```

**Bad:**
```json
{
  "question": "Docker",
  "answer": "Container thing",
  "category": "",
  "tags": []
}
```

### 2. Optimal Knowledge Size
- **Question**: 10-100 words
- **Answer**: 50-300 words
- Quá ngắn → Thiếu context
- Quá dài → Embedding kém hiệu quả

### 3. Categories & Tags
- Dùng categories để tổ chức
- Tags giúp tìm kiếm tốt hơn
- Consistent naming convention

### 4. Updating Knowledge
```python
# Sau khi update knowledge
await axios.post('/api/knowledge/refresh')
```

---

## Troubleshooting

### MongoDB Connection Error
```
✗ Failed to connect to MongoDB
```

**Giải pháp:**
1. Kiểm tra MongoDB đang chạy: `mongod --version`
2. Check connection string trong `.env`
3. Thử: `mongodb://localhost:27017/` hoặc `mongodb://127.0.0.1:27017/`

### HuggingFace API Error
```
Error: 429 Too Many Requests
```

**Giải pháp:**
- Free tier: 1000 requests/day
- Chờ 24h hoặc upgrade plan
- Hoặc dùng local model (Option A)

### Embedding Model Download Slow
```
Downloading sentence-transformers model...
```

**Giải pháp:**
- Lần đầu download ~80MB
- Lần sau dùng cache
- Dùng WiFi nhanh cho lần đầu

### Low Similarity Scores
```
No relevant knowledge found
```

**Giải pháp:**
- Thêm nhiều knowledge hơn
- Cải thiện câu hỏi trong database
- Giảm threshold (0.2 → 0.1)

---

## Performance Tips

### 1. Cache Management
- Cache tự động load vào RAM
- Refresh khi add nhiều knowledge: `/api/knowledge/refresh`

### 2. Batch Insert
```python
# Thêm nhiều knowledge cùng lúc
for item in knowledge_list:
    bot.add_knowledge(**item)
bot.refresh_knowledge_cache()
```

### 3. Index MongoDB
```python
# Tự động tạo indexes cho:
# - category
# - tags
# - session_id
```

---

## Mở rộng

### 1. Thêm Authentication
```python
from flask_jwt_extended import JWTManager

jwt = JWTManager(app)
```

### 2. Rate Limiting
```python
from flask_limiter import Limiter

limiter = Limiter(app)
```

### 3. Caching với Redis
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})
```

### 4. Monitoring
```python
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app)
```

---

## Files Structure

```
MY_AI_AGENT/
├── chatbot_rag.py          # RAG chatbot core
├── chatbot_rag_api.py      # REST API server
├── mongo_db.py             # MongoDB manager
├── seed_data.py            # Sample data seeder
├── requirements.txt        # Dependencies
├── .env                    # Configuration
└── RAG_CHATBOT_README.md   # This file
```

---

## Chi phí & Giới hạn

### FREE Tier (Current)
- **Embeddings**: Unlimited (local)
- **MongoDB**: Unlimited (local)
- **HuggingFace API**: 1000 requests/day
- **Tổng**: $0/tháng

### Khi vượt FREE Tier
- **1000-5000 req/day**: ~$5/tháng
- **5000-10000 req/day**: ~$10/tháng
- **10000+ req/day**: Consider Option A (fully local)

---

## Support & Resources

- **HuggingFace Models**: https://huggingface.co/models
- **Sentence Transformers**: https://www.sbert.net/
- **MongoDB Docs**: https://docs.mongodb.com/
- **Flask Docs**: https://flask.palletsprojects.com/

---

## License

MIT License - Free to use for personal and commercial projects.

---

**Tạo bởi: Claude Code Assistant**
**Ngày: 2025-10-29**
