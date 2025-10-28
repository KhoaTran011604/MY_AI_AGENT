# HuggingFace Chatbot với Python

Dự án chatbot sử dụng HuggingFace API và Python Flask.

## Cài đặt

### 1. Tạo Virtual Environment

```bash
python -m venv venv
```

### 2. Kích hoạt Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

### 4. Cấu hình API Key

1. Copy file `.env.example` thành `.env`:
```bash
copy .env.example .env
```

2. Lấy API key từ HuggingFace:
   - Truy cập: https://huggingface.co/settings/tokens
   - Tạo token mới (read access)
   - Copy token

3. Mở file `.env` và thêm API key:
```
HUGGINGFACE_API_KEY=your_actual_api_key_here
```

## Chạy Demo

### ⚡ CÁCH NHANH NHẤT (Dành cho người mới)

**Chạy server (chỉ cần double-click):**
- Double-click vào file `start_server.bat`
- Server sẽ tự động chạy tại http://localhost:5000

**Test nhanh (chỉ cần double-click):**
- Double-click vào file `test_chat.bat`
- Sẽ test chatbot ngay lập tức

### Hoặc dùng lệnh trong Terminal:

**Chạy Flask API Server:**
```bash
# Cách 1: Dùng file .bat (Windows)
start_server.bat

# Cách 2: Lệnh đầy đủ
cd src
..\venv\Scripts\python.exe app_flask.py

# Cách 3: Nếu đã activate venv
cd src
python app_flask.py
```

Server sẽ chạy tại: http://localhost:5000

**Chạy test nhanh:**
```bash
test_chat.bat
```

**Chạy Console Demo (chat trong terminal):**
```bash
venv\Scripts\python.exe demo.py
```

## Sử dụng API

### 1. Test API với cURL

**Chat endpoint:**
```bash
curl -X POST http://localhost:5000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"Hello, how are you?\"}"
```

**Reset conversation:**
```bash
curl -X POST http://localhost:5000/reset ^
  -H "Content-Type: application/json"
```

### 2. Test API với Python

```python
import requests

# Send message
response = requests.post(
    'http://localhost:5000/chat',
    json={'message': 'Tell me a joke'}
)
print(response.json())

# Reset conversation
response = requests.post('http://localhost:5000/reset')
print(response.json())
```

## Các Model Được Đề Xuất

1. **mistralai/Mistral-7B-Instruct-v0.1** (Recommended)
   - Model mạnh, đa năng
   - Tốt cho hầu hết các tác vụ

2. **HuggingFaceH4/zephyr-7b-beta**
   - Model chat tốt
   - Phản hồi tự nhiên

3. **microsoft/DialoGPT-medium**
   - Nhẹ, nhanh
   - Tốt cho chat đơn giản

4. **tiiuae/falcon-7b-instruct**
   - Instruction following tốt
   - Đa dạng trong câu trả lời

## Cấu trúc Project

```
MY_AI_AGENT/
├── src/
│   ├── chatbot.py         # Core chatbot class
│   └── app_flask.py       # Flask API server
├── demo.py                # Console demo script
├── requirements.txt       # Python dependencies
├── .env                   # API keys (create this)
└── .env.example          # Environment template
```

## Troubleshooting

### Lỗi: "No module named 'dotenv'"
```bash
pip install python-dotenv
```

### Lỗi: "API key not found"
- Kiểm tra file `.env` đã được tạo
- Đảm bảo `HUGGINGFACE_API_KEY` được set đúng

### Lỗi: "Model requires access"
- Một số model cần approval trên HuggingFace
- Truy cập model page và request access
- Hoặc dùng model khác

### Lỗi kết nối API
- Kiểm tra internet connection
- Verify API key còn valid
- Check HuggingFace status: https://status.huggingface.co/

## Mở rộng

### Thay đổi Model

Trong [app_flask.py](src/app_flask.py:17):
```python
chatbot = HuggingFaceChatbot(model_name="your-model-name")
```

Hoặc trong [demo.py](demo.py), bạn có thể nhập tên model khi chạy.

### Thêm tính năng mới

Edit [chatbot.py](src/chatbot.py) để thêm:
- System prompts
- Temperature control
- Max tokens settings
- Conversation memory

## License

ISC
