# Chatbot API Documentation

REST API để tương tác với HuggingFace Chatbot từ Frontend.

## Cài đặt

```bash
pip install -r requirements.txt
```

## Chạy Server

```bash
python chatbot-api.py
```

Server sẽ chạy tại: `http://localhost:5000`

## Cấu hình (.env)

```env
HUGGINGFACE_API_KEY=your_api_key_here
PORT=5000
DEBUG=False
```

---

## API Endpoints

### 1. Health Check
**GET** `/health`

Kiểm tra trạng thái server.

**Response:**
```json
{
  "status": "healthy",
  "active_sessions": 3
}
```

---

### 2. Chat với Bot
**POST** `/api/chat`

Gửi tin nhắn và nhận phản hồi từ bot.

**Request Body:**
```json
{
  "message": "Hello, how are you?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "I'm doing great! How can I help you today?",
  "session_id": "abc-123-def-456",
  "status": "success"
}
```

**Lưu ý:**
- Nếu không có `session_id`, hệ thống tự tạo session mới
- Lưu `session_id` để duy trì cuộc hội thoại

---

### 3. Tạo Session Mới
**POST** `/api/session/new`

Tạo session mới để bắt đầu cuộc hội thoại.

**Response:**
```json
{
  "session_id": "new-uuid-here",
  "status": "success",
  "message": "New session created"
}
```

---

### 4. Reset Lịch Sử Chat
**POST** `/api/session/<session_id>/reset`

Xóa lịch sử hội thoại nhưng giữ session.

**Response:**
```json
{
  "status": "success",
  "message": "Conversation history cleared"
}
```

---

### 5. Xóa Session
**DELETE** `/api/session/<session_id>/delete`

Xóa hoàn toàn session.

**Response:**
```json
{
  "status": "success",
  "message": "Session deleted"
}
```

---

### 6. Lấy Lịch Sử Chat
**GET** `/api/session/<session_id>/history`

Lấy toàn bộ lịch sử hội thoại.

**Response:**
```json
{
  "history": [
    {
      "role": "user",
      "content": "Hello"
    },
    {
      "role": "assistant",
      "content": "Hi there!"
    }
  ],
  "status": "success"
}
```

---

### 7. Danh Sách Sessions
**GET** `/api/sessions`

Lấy danh sách tất cả sessions đang hoạt động.

**Response:**
```json
{
  "sessions": ["session-1", "session-2", "session-3"],
  "count": 3,
  "status": "success"
}
```

---

## Error Responses

Tất cả lỗi trả về format:

```json
{
  "error": "Error message here",
  "status": "error"
}
```

**HTTP Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad Request (thiếu tham số)
- `404` - Not Found (session không tồn tại)
- `500` - Internal Server Error

---

## Ví Dụ Sử Dụng với JavaScript

### Fetch API
```javascript
// Gửi tin nhắn
async function sendMessage(message, sessionId = null) {
  const response = await fetch('http://localhost:5000/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: message,
      session_id: sessionId
    })
  });

  const data = await response.json();
  return data;
}

// Sử dụng
const result = await sendMessage("Hello bot!");
console.log(result.response);
console.log(result.session_id); // Lưu lại để dùng cho lần sau
```

### Axios
```javascript
import axios from 'axios';

const API_URL = 'http://localhost:5000';

// Tạo session mới
const createSession = async () => {
  const { data } = await axios.post(`${API_URL}/api/session/new`);
  return data.session_id;
};

// Chat
const chat = async (message, sessionId) => {
  const { data } = await axios.post(`${API_URL}/api/chat`, {
    message,
    session_id: sessionId
  });
  return data.response;
};

// Sử dụng
const sessionId = await createSession();
const response = await chat("Hello!", sessionId);
console.log(response);
```

### React Hook Example
```javascript
import { useState, useEffect } from 'react';
import axios from 'axios';

function useChatbot() {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Tạo session khi component mount
    const initSession = async () => {
      const { data } = await axios.post('http://localhost:5000/api/session/new');
      setSessionId(data.session_id);
    };
    initSession();
  }, []);

  const sendMessage = async (message) => {
    if (!sessionId) return;

    setLoading(true);
    try {
      const { data } = await axios.post('http://localhost:5000/api/chat', {
        message,
        session_id: sessionId
      });

      setMessages(prev => [
        ...prev,
        { role: 'user', content: message },
        { role: 'assistant', content: data.response }
      ]);
    } catch (error) {
      console.error('Chat error:', error);
    }
    setLoading(false);
  };

  const resetChat = async () => {
    if (!sessionId) return;
    await axios.post(`http://localhost:5000/api/session/${sessionId}/reset`);
    setMessages([]);
  };

  return { messages, sendMessage, resetChat, loading };
}
```

---

## CORS Configuration

API đã enable CORS, cho phép frontend từ bất kỳ origin nào gọi API.

Nếu muốn giới hạn origins:

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "https://yourdomain.com"]
    }
})
```

---

## Testing với cURL

```bash
# Health check
curl http://localhost:5000/health

# Tạo session
curl -X POST http://localhost:5000/api/session/new

# Chat
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello bot!", "session_id": "your-session-id"}'

# Lấy lịch sử
curl http://localhost:5000/api/session/your-session-id/history

# Reset session
curl -X POST http://localhost:5000/api/session/your-session-id/reset

# Xóa session
curl -X DELETE http://localhost:5000/api/session/your-session-id/delete
```

---

## Tips & Best Practices

1. **Session Management:**
   - Lưu `session_id` trong localStorage hoặc cookies
   - Tạo session mới khi user clear data hoặc đóng tab

2. **Error Handling:**
   - Luôn check `status` field trong response
   - Hiển thị error message cho user khi có lỗi

3. **Loading States:**
   - Show loading indicator khi đang chờ response
   - Disable input khi đang xử lý

4. **Rate Limiting:**
   - HuggingFace API có rate limit
   - Implement debounce cho input nếu cần

5. **Security:**
   - Không expose HUGGINGFACE_API_KEY ra frontend
   - Implement authentication nếu deploy production
