# Product Consultation Chatbot - Tư vấn sản phẩm AI

## 🎯 Tổng quan

Chatbot tư vấn sản phẩm thông minh sử dụng RAG (Retrieval-Augmented Generation) để:
- **Tìm kiếm sản phẩm** theo yêu cầu của khách hàng
- **Tư vấn** sản phẩm phù hợp dựa trên ngữ cảnh
- **So sánh** các sản phẩm
- **Trả lời câu hỏi** về thông tin sản phẩm
- **Gợi ý** sản phẩm tương tự

### Công nghệ

| Component | Technology | Chi phí |
|-----------|-----------|---------|
| Database | MongoDB | FREE |
| Embeddings | sentence-transformers | FREE (local) |
| LLM | HuggingFace API | FREE (1000 req/day) |
| API | Flask + CORS | FREE |
| Search | Semantic Search | FREE |

---

## 🏗️ Kiến trúc

```
┌─────────────┐
│  Frontend   │ (React/Vue/Mobile App)
└──────┬──────┘
       │ REST API
       ↓
┌──────────────────────────────────┐
│  product_chatbot_api.py          │
│  - Chat endpoint                 │
│  - Product management            │
│  - Search & Filter               │
└──────┬───────────────────────────┘
       │
       ↓
┌──────────────────────────────────┐
│  product_chatbot.py (RAG Core)   │
│  ┌────────────────────────────┐  │
│  │ 1. Query Analysis          │  │
│  │ 2. Semantic Search         │  │
│  │ 3. Product Retrieval       │  │
│  │ 4. AI Consultation         │  │
│  └────────────────────────────┘  │
└──────┬───────────────────────────┘
       │
       ↓
┌──────────────────────────────────┐
│  MongoDB - Product Database      │
│  - Products Collection           │
│  - Embeddings                    │
│  - Specifications                │
└──────────────────────────────────┘
```

---

## 📦 Product Schema

```json
{
  "name": "iPhone 15 Pro Max",
  "description": "iPhone 15 Pro Max với chip A17 Pro...",
  "category": "Điện thoại",
  "brand": "Apple",
  "price": 34990000,
  "currency": "VND",
  "stock": 50,
  "specifications": {
    "Screen": "6.7 inch Super Retina XDR",
    "Chipset": "Apple A17 Pro",
    "RAM": "8GB",
    "Storage": "256GB",
    "Camera": "48MP + 12MP + 12MP",
    "Battery": "4422 mAh"
  },
  "images": ["url1.jpg", "url2.jpg"],
  "rating": 4.9,
  "tags": ["flagship", "premium", "5g"],
  "embedding": [0.12, -0.45, ...],  // Vector 384 dimensions
  "created_at": "2025-10-29T...",
  "updated_at": "2025-10-29T..."
}
```

---

## 🚀 Cài đặt

### 1. Cài MongoDB

**Windows:**
```bash
choco install mongodb
mongod --dbpath="C:\data\db"
```

**Mac:**
```bash
brew install mongodb-community
brew services start mongodb-community
```

**Linux:**
```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình .env

File `.env` đã có sẵn config:
```env
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=chatbot_db
HUGGINGFACE_API_KEY=your_key_here
PORT=5000
```

### 4. Seed dữ liệu sản phẩm mẫu

```bash
python seed_products.py
```

Sẽ thêm 15 sản phẩm mẫu:
- 4 Laptops (Dell, ASUS, Apple, HP)
- 4 Điện thoại (iPhone, Samsung, Xiaomi, OPPO)
- 2 Máy tính bảng (iPad, Galaxy Tab)
- 2 Tai nghe (AirPods, Sony)
- 2 Đồng hồ thông minh (Apple Watch, Galaxy Watch)

---

## 💬 Sử dụng

### Option 1: Command Line (CLI)

```bash
python product_chatbot.py
```

**Ví dụ chat:**
```
Bạn: Tìm laptop dưới 20 triệu
Bot: Dựa trên yêu cầu của bạn, tôi gợi ý HP Pavilion 15...

[Tìm thấy 2 sản phẩm phù hợp]
  1. HP Pavilion 15 - 15,990,000đ
  2. MacBook Air M2 - 28,990,000đ
```

```
Bạn: So sánh iPhone 15 với Samsung S24
Bot: Cả hai đều là flagship cao cấp. iPhone 15 Pro Max...
```

### Option 2: API Server

```bash
python product_chatbot_api.py
```

Server chạy tại: `http://localhost:5000`

---

## 🔌 API Documentation

### 1. Chat với Bot tư vấn

```http
POST /api/chat
Content-Type: application/json

{
  "message": "Tìm laptop gaming dưới 30 triệu",
  "session_id": "optional-uuid"
}
```

**Response:**
```json
{
  "response": "Dựa trên yêu cầu laptop gaming dưới 30 triệu...",
  "products": [
    {
      "id": "507f1f77bcf86cd799439011",
      "name": "Laptop ASUS ROG Strix G15",
      "category": "Laptop",
      "brand": "ASUS",
      "price": 35990000,
      "price_formatted": "35,990,000đ",
      "description": "Laptop gaming ASUS ROG...",
      "specifications": {
        "CPU": "AMD Ryzen 9 7945HX",
        "RAM": "32GB DDR5",
        "Graphics": "NVIDIA RTX 4060 8GB"
      },
      "rating": 4.8,
      "stock": 15,
      "in_stock": true,
      "images": ["asus-rog-g15-1.jpg"],
      "similarity": 0.87
    }
  ],
  "found_products": true,
  "session_id": "abc-123",
  "status": "success"
}
```

### 2. Tìm kiếm sản phẩm nâng cao

```http
POST /api/products/search
Content-Type: application/json

{
  "query": "laptop gaming",
  "top_k": 5,
  "filters": {
    "category": "Laptop",
    "brand": "ASUS",
    "min_price": 10000000,
    "max_price": 40000000,
    "in_stock_only": true
  }
}
```

### 3. Thêm sản phẩm mới

```http
POST /api/products/add
Content-Type: application/json

{
  "name": "iPhone 16 Pro",
  "description": "Latest iPhone...",
  "category": "Điện thoại",
  "brand": "Apple",
  "price": 35990000,
  "currency": "VND",
  "stock": 30,
  "specifications": {
    "Screen": "6.7 inch",
    "Chipset": "A18 Pro"
  },
  "images": ["iphone16-1.jpg"],
  "rating": 4.9,
  "tags": ["flagship", "new"]
}
```

### 4. Lấy danh sách sản phẩm

```http
GET /api/products/list?category=Laptop&brand=Dell
```

### 5. Chi tiết sản phẩm

```http
GET /api/products/{product_id}
```

### 6. Danh mục & Thương hiệu

```http
GET /api/products/categories
GET /api/products/brands
```

### 7. Top sản phẩm đánh giá cao

```http
GET /api/products/top-rated?limit=10&category=Laptop
```

### 8. Thống kê

```http
GET /api/statistics
```

**Response:**
```json
{
  "total_products": 15,
  "in_stock": 13,
  "out_of_stock": 2,
  "categories": ["Laptop", "Điện thoại", "Máy tính bảng", ...],
  "brands": ["Apple", "Samsung", "Dell", ...],
  "price_range": {
    "min": 6490000,
    "max": 35990000
  },
  "status": "success"
}
```

---

## 🎨 Frontend Integration

### React Example - Chat Component

```javascript
import { useState } from 'react';
import axios from 'axios';

function ProductChatbot() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    setLoading(true);

    // Add user message to UI
    setMessages(prev => [...prev, {
      role: 'user',
      content: message
    }]);

    try {
      const { data } = await axios.post('http://localhost:5000/api/chat', {
        message: message
      });

      // Add bot response
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.response,
        products: data.products
      }]);

      setMessage('');
    } catch (error) {
      console.error('Chat error:', error);
    }

    setLoading(false);
  };

  return (
    <div className="chatbot-container">
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <p>{msg.content}</p>

            {/* Display products if available */}
            {msg.products && msg.products.length > 0 && (
              <div className="products-grid">
                {msg.products.map(product => (
                  <div key={product.id} className="product-card">
                    <img src={product.images[0]} alt={product.name} />
                    <h4>{product.name}</h4>
                    <p className="brand">{product.brand}</p>
                    <p className="price">{product.price_formatted}</p>
                    <p className="rating">⭐ {product.rating}/5.0</p>
                    <button>Xem chi tiết</button>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      <form onSubmit={sendMessage}>
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Hỏi về sản phẩm..."
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Đang xử lý...' : 'Gửi'}
        </button>
      </form>
    </div>
  );
}

export default ProductChatbot;
```

### Product Search Component

```javascript
function ProductSearch() {
  const [query, setQuery] = useState('');
  const [filters, setFilters] = useState({
    category: '',
    min_price: null,
    max_price: null
  });
  const [products, setProducts] = useState([]);

  const searchProducts = async () => {
    const { data } = await axios.post('http://localhost:5000/api/products/search', {
      query,
      top_k: 10,
      filters
    });

    setProducts(data.products);
  };

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Tìm kiếm sản phẩm..."
      />

      {/* Filters */}
      <select onChange={(e) => setFilters({...filters, category: e.target.value})}>
        <option value="">Tất cả danh mục</option>
        <option value="Laptop">Laptop</option>
        <option value="Điện thoại">Điện thoại</option>
      </select>

      <button onClick={searchProducts}>Tìm kiếm</button>

      {/* Results */}
      <div className="products-grid">
        {products.map(product => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
}
```

---

## 🧠 Cách thức hoạt động

### 1. Natural Language Understanding

Chatbot hiểu ngôn ngữ tự nhiên tiếng Việt:

```
"Tìm laptop dưới 20 triệu"
→ Extract: price < 20,000,000, category: Laptop

"Điện thoại Apple camera đẹp"
→ Extract: brand: Apple, category: Điện thoại, feature: camera

"So sánh iPhone 15 và Samsung S24"
→ Extract: products to compare
```

### 2. Semantic Search Pipeline

```
User Query: "Laptop gaming mạnh"
        ↓
[1] Text Embedding
    "Laptop gaming mạnh" → Vector [0.12, -0.45, 0.67, ...]
        ↓
[2] Filter Products
    - Category: Laptop
    - Price range if specified
    - Stock availability
        ↓
[3] Calculate Similarity
    Query vector vs All product vectors
    → Cosine similarity scores
        ↓
[4] Rank & Return Top-K
    Top 5 most similar products
        ↓
[5] Generate Consultation
    LLM creates personalized recommendation
```

### 3. Price Extraction

Tự động nhận diện giá từ câu hỏi:

```python
"Dưới 20 triệu" → max_price = 20,000,000
"Từ 10 đến 30 triệu" → min_price = 10,000,000, max_price = 30,000,000
"Trên 50 triệu" → min_price = 50,000,000
```

### 4. AI Consultation

```
Context: Top 3 relevant products
Query: "Tìm laptop cho sinh viên"

LLM generates:
"Dựa trên nhu cầu của bạn, tôi gợi ý:

1. HP Pavilion 15 (15,990,000đ)
   - Phù hợp ngân sách sinh viên
   - Hiệu năng ổn định cho học tập
   - Pin tốt, thiết kế nhẹ

2. MacBook Air M2 (28,990,000đ)
   - Nếu ngân sách cao hơn
   - Pin lên đến 18 giờ
   - Lý tưởng cho lập trình, thiết kế

Bạn thường sử dụng laptop để làm gì?"
```

---

## ✨ Tính năng nổi bật

### 1. Smart Filters
- Tự động trích xuất bộ lọc từ câu hỏi
- Hỗ trợ giá, danh mục, thương hiệu
- Kết hợp multiple filters

### 2. Contextual Recommendations
- Gợi ý dựa trên ngữ cảnh
- So sánh ưu nhược điểm
- Phân tích use case

### 3. Vietnamese Language
- Hiểu tiếng Việt tự nhiên
- Format giá theo VNĐ
- Tư vấn bằng tiếng Việt

### 4. Product Comparison
```
User: "So sánh iPhone 15 và Samsung S24"
Bot: Phân tích chi tiết 2 sản phẩm
```

### 5. Real-time Stock
- Hiển thị tình trạng kho
- Filter chỉ sản phẩm còn hàng

---

## 📊 Use Cases

### 1. E-commerce Website
- Chatbot trên website shop
- Tư vấn sản phẩm cho khách
- Giảm tải cho customer service

### 2. Mobile Shopping App
- In-app chatbot
- Voice shopping assistant
- Product discovery

### 3. Social Commerce
- Facebook Messenger bot
- Zalo bot
- Instagram shopping

### 4. Internal Sales Tool
- Công cụ cho nhân viên bán hàng
- Quick product lookup
- Comparison tool

---

## 🔧 Customization

### Thay đổi Embedding Model

```python
# product_chatbot.py
bot = ProductChatbot(
    embedding_model="keepitreal/vietnamese-sbert"  # Vietnamese model
)
```

### Thay đổi LLM

```python
bot = ProductChatbot(
    llm_model="meta-llama/Llama-2-70b-chat-hf"  # Stronger model
)
```

### Custom Product Schema

Thêm fields vào [product_manager.py](product_manager.py:51):

```python
def add_product(self, ..., warranty=None, discount=None):
    product = {
        ...
        "warranty": warranty,
        "discount": discount
    }
```

---

## 🐛 Troubleshooting

### MongoDB Connection Error
```bash
# Check if MongoDB is running
mongod --version

# Start MongoDB
mongod --dbpath="C:\data\db"
```

### No products found
```bash
# Seed sample data
python seed_products.py
```

### Slow embedding generation
```bash
# First time downloads model (~80MB)
# Subsequent runs use cached model
```

### HuggingFace API rate limit
```
# Free tier: 1000 requests/day
# Consider upgrading or using local model
```

---

## 📈 Performance Tips

### 1. Index Optimization
MongoDB tự động tạo indexes cho:
- Text search (name, description)
- Category, Brand
- Price, Rating

### 2. Embedding Cache
- Products embeddings cached in RAM
- Refresh khi add products: `/api/products/refresh`

### 3. Batch Operations
```python
# Add multiple products
for product in products_list:
    bot.add_product(**product)
bot.refresh_cache()  # Refresh once
```

---

## 🔒 Security (Production)

### 1. Authentication
```python
from flask_jwt_extended import jwt_required

@app.route('/api/products/add')
@jwt_required()
def add_product():
    ...
```

### 2. Rate Limiting
```python
from flask_limiter import Limiter

limiter = Limiter(app)

@app.route('/api/chat')
@limiter.limit("10 per minute")
def chat():
    ...
```

### 3. Input Validation
```python
from flask import abort

if not validate_product_data(data):
    abort(400, "Invalid product data")
```

---

## 💰 Chi phí ước tính

### FREE Tier (Current Setup)
- Embeddings: Unlimited (local)
- MongoDB: Unlimited (local)
- HuggingFace API: 1000 requests/day
- **Tổng: $0/tháng**

### Khi scale lên
- 1,000-5,000 requests/day: ~$5/tháng
- 5,000-10,000 requests/day: ~$10/tháng
- MongoDB Atlas: $0-57/tháng (tùy storage)

---

## 📚 Files Structure

```
MY_AI_AGENT/
├── product_manager.py          # MongoDB manager
├── product_chatbot.py          # RAG chatbot core
├── product_chatbot_api.py      # REST API server
├── seed_products.py            # Sample data
├── PRODUCT_CHATBOT_README.md   # This file
├── requirements.txt            # Dependencies
└── .env                        # Configuration
```

---

## 🎓 Learning Resources

- **RAG**: https://www.anthropic.com/research/retrieval-augmented-generation
- **Sentence Transformers**: https://www.sbert.net/
- **MongoDB**: https://docs.mongodb.com/
- **Flask**: https://flask.palletsprojects.com/

---

## 🤝 Support

Nếu gặp vấn đề:
1. Check MongoDB đang chạy
2. Check .env configuration
3. Verify dependencies installed
4. Check HuggingFace API key

---

**Phát triển bởi: Claude Code Assistant**
**Ngày: 2025-10-29**
**Version: 1.0.0**

---

## 📝 License

MIT License - Free for personal and commercial use.
