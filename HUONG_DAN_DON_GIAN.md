# 🚀 HƯỚNG DẪN ĐỐN GIẢN - DÀNH CHO NGƯỜI MỚI

## ✅ Bạn đã setup xong! Giờ chỉ cần chạy thôi!

---

## 🎯 CÁCH CHẠY NHANH NHẤT (3 GIÂY)

### 1️⃣ Chạy Server Chatbot

**Cách 1: Double-click (KHUYẾN NGHỊ)**
```
👆 Double-click vào file: start_server.bat
```
- Server sẽ tự động chạy
- Địa chỉ: http://localhost:5000
- Để tắt: Bấm Ctrl+C hoặc đóng cửa sổ

**Cách 2: Gõ lệnh ngắn trong terminal**
```bash
start_server.bat
```

---

### 2️⃣ Test Chatbot Nhanh

**Cách 1: Double-click**
```
👆 Double-click vào file: test_chat.bat
```
- Sẽ test chatbot với câu hỏi mẫu
- Xem kết quả ngay lập tức

**Cách 2: Gõ lệnh**
```bash
test_chat.bat
```

---

## 📝 GỬI TIN NHẮN ĐẾN CHATBOT

### Cách 1: Dùng curl (trong terminal)

```bash
curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d "{\"message\": \"Xin chào!\"}"
```

### Cách 2: Dùng PowerShell (Windows)

```powershell
# Gửi tin nhắn
$body = @{message="Xin chào!"} | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:5000/chat -Method Post -Body $body -ContentType "application/json"
```

### Cách 3: Dùng Postman (giao diện đẹp)

1. Tải Postman: https://www.postman.com/
2. Tạo request mới:
   - Method: POST
   - URL: http://localhost:5000/chat
   - Headers: Content-Type = application/json
   - Body (raw JSON):
   ```json
   {
     "message": "Hello!"
   }
   ```

---

## 🌟 CÁC FILE QUAN TRỌNG

| File | Công dụng | Cách dùng |
|------|-----------|-----------|
| `start_server.bat` | Chạy server | Double-click |
| `test_chat.bat` | Test nhanh | Double-click |
| `demo.py` | Chat trong terminal | `venv\Scripts\python demo.py` |
| `.env` | Chứa API key | Đã setup rồi, không cần động |
| `src/app_flask.py` | Code server | Có thể đổi model ở đây |

---

## 🔧 CÁC LỆNH HỮU ÍCH

### Activate virtual environment (nếu cần)
```bash
venv\Scripts\activate
```
Sau khi activate, prompt sẽ hiện `(venv)` ở đầu

### Deactivate virtual environment
```bash
deactivate
```

### Cài thêm package
```bash
venv\Scripts\pip install ten_package
```

### Xem các package đã cài
```bash
venv\Scripts\pip list
```

---

## 🎨 ĐỔI MODEL CHATBOT

Mở file `src/app_flask.py`, tìm dòng:

```python
chatbot = HuggingFaceChatbot(model_name="Qwen/Qwen2.5-72B-Instruct")
```

Đổi thành model khác:

```python
# Model mạnh, thông minh (đang dùng)
model_name="Qwen/Qwen2.5-72B-Instruct"

# Model nhỏ gọn, nhanh
model_name="microsoft/DialoGPT-medium"

# Model khác
model_name="meta-llama/Llama-3.2-3B-Instruct"
```

Sau đó restart server (tắt rồi chạy lại `start_server.bat`)

---

## ❓ GẶP VẤN ĐỀ?

### Lỗi: "Port 5000 đã được dùng"
```bash
# Tìm process đang dùng port 5000
netstat -ano | findstr :5000

# Kill process (thay PID bằng số process)
taskkill /PID <số_PID> /F
```

### Lỗi: "Module not found"
```bash
# Cài lại packages
venv\Scripts\pip install -r requirements.txt
```

### Lỗi: "API key invalid"
- Kiểm tra file `.env`
- Lấy key mới tại: https://huggingface.co/settings/tokens

### Server không phản hồi
- Đợi 10-15 giây sau khi start
- Check xem server có đang chạy không
- Thử restart server

---

## 🎓 HỌC THÊM

- [README.md](README.md) - Hướng dẫn chi tiết
- [HuggingFace Models](https://huggingface.co/models) - Tìm model khác
- [Flask Documentation](https://flask.palletsprojects.com/) - Học Flask
- [Python Docs](https://docs.python.org/) - Học Python

---

## 📞 TÓM TẮT NHANH

```
✅ Chạy server     → Double-click start_server.bat
✅ Test chatbot    → Double-click test_chat.bat
✅ Gửi tin nhắn    → POST http://localhost:5000/chat
✅ Reset chat      → POST http://localhost:5000/reset
✅ Tắt server      → Ctrl+C hoặc đóng cửa sổ
```

---

🎉 **Chúc bạn code vui vẻ!**
