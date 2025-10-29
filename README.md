# Discord AI Chatbot

Bot Discord sử dụng HuggingFace API để trò chuyện thông minh với người dùng.

## Setup Nhanh

### 1. Cài đặt Python Dependencies

```bash
# Tạo và kích hoạt virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Cài đặt packages
pip install -r requirements.txt
```

### 2. Cấu hình API Keys

Tạo file `.env` từ template:

```bash
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac
```

Thêm API keys vào file `.env`:

```env
# HuggingFace API Key (bắt buộc)
HUGGINGFACE_API_KEY=hf_your_key_here

# Discord Bot Token (bắt buộc để chạy Discord bot)
DISCORD_BOT_TOKEN=your_discord_token_here

# Model name (tùy chọn)
HUGGINGFACE_MODEL=Qwen/Qwen2.5-72B-Instruct
```

**Lấy API keys:**

- HuggingFace: https://huggingface.co/settings/tokens
- Discord: Xem hướng dẫn chi tiết trong [DISCORD_SETUP.md](DISCORD_SETUP.md)

### 3. Chạy Bot

```bash
# Chạy Discord bot
python discord_bot.py

```

## Các File Chính

- **[discord_bot.py](discord_bot.py)** - Discord bot chính (chạy file này)

## Sử dụng Discord Bot

Sau khi bot đã online:

1. **Chat với bot**: Mention bot và gửi tin nhắn

   ```
   @YourBot Hello, how are you?
   ```

2. **Các lệnh hữu ích**:
   - `!reset` - Xóa lịch sử hội thoại
   - `!ping` - Kiểm tra bot có hoạt động không
   - `!help_bot` - Hiển thị hướng dẫn

## Models Được Hỗ Trợ

Có thể thay đổi model trong file `.env`:

```env
# Qwen (mạnh, đa năng)
HUGGINGFACE_MODEL=Qwen/Qwen2.5-72B-Instruct

# Mistral (cân bằng)
HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.1

# DialoGPT (nhẹ, nhanh)
HUGGINGFACE_MODEL=microsoft/DialoGPT-medium

# Llama (mạnh mẽ)
HUGGINGFACE_MODEL=meta-llama/Llama-3.2-3B-Instruct
```

## Troubleshooting

### Bot không kết nối Discord

- Kiểm tra `DISCORD_BOT_TOKEN` trong `.env`
- Xem hướng dẫn setup Discord bot: [DISCORD_SETUP.md](DISCORD_SETUP.md)

### Lỗi API Key

```
ERROR: HUGGINGFACE_API_KEY not found
```

- Tạo file `.env` và thêm API key từ HuggingFace
- Đảm bảo key có format: `hf_...`

### Model không trả lời

- Kiểm tra model có tồn tại trên HuggingFace
- Một số model cần request access trước khi dùng
- Thử model khác (xem danh sách phía trên)

### Lỗi import module

```bash
pip install -r requirements.txt --upgrade
```

### Lỗi kẹt trong venv

```bash
deactivate
```

## Tài Liệu Khác

- [DISCORD_SETUP.md](DISCORD_SETUP.md) - Hướng dẫn setup Discord bot chi tiết
- [HUONG_DAN_DON_GIAN.md](HUONG_DAN_DON_GIAN.md) - Hướng dẫn đơn giản bằng tiếng Việt
- [HUONG_DAN_GIT.md](HUONG_DAN_GIT.md) - Hướng dẫn sử dụng Git

## Cấu Trúc Project

```
MY_AI_AGENT/
├── discord_bot.py         # Discord bot entry point
├── chatbot.py             # HuggingFace chatbot core
├── demo.py                # Interactive terminal demo
├── quick_test.py          # Quick test script
├── test_qwen_model.py     # Qwen model test
├── requirements.txt       # Python dependencies
├── .env                   # API keys (tạo file này)
├── .env.example           # Template
└── venv/                  # Virtual environment
```

## License

ISC
