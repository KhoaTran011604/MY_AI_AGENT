# Hướng dẫn Setup Discord Bot

## Bước 1: Tạo Discord Bot

1. Truy cập [Discord Developer Portal](https://discord.com/developers/applications)
2. Đăng nhập bằng tài khoản Discord của bạn
3. Click nút **"New Application"**
4. Đặt tên cho application (ví dụ: "AI Chatbot")
5. Click **"Create"**

## Bước 2: Tạo Bot và Lấy Token

1. Trong application vừa tạo, chọn tab **"Bot"** ở menu bên trái
2. Click **"Add Bot"** và xác nhận
3. Trong phần **Token**, click **"Reset Token"** hoặc **"Copy"** để lấy token
4. **LƯU Ý**: Token này rất quan trọng, giữ bí mật và không chia sẻ với ai!

## Bước 3: Cấu hình Bot Permissions

### Privileged Gateway Intents
Trong tab **"Bot"**, kéo xuống phần **Privileged Gateway Intents** và bật:
- ✅ **MESSAGE CONTENT INTENT** (bắt buộc để đọc nội dung tin nhắn)
- ✅ **SERVER MEMBERS INTENT** (tùy chọn)

### Bot Permissions
Trong tab **"OAuth2"** > **"URL Generator"**:

1. Chọn **SCOPES**:
   - ✅ `bot`
   - ✅ `applications.commands`

2. Chọn **BOT PERMISSIONS**:
   - ✅ Send Messages
   - ✅ Read Messages/View Channels
   - ✅ Read Message History
   - ✅ Add Reactions (optional)
   - ✅ Embed Links
   - ✅ Attach Files (optional)

3. Copy URL được tạo ở cuối trang

## Bước 4: Mời Bot vào Server

1. Paste URL vừa copy vào trình duyệt
2. Chọn server mà bạn muốn thêm bot (bạn cần có quyền "Manage Server")
3. Click **"Authorize"**
4. Hoàn thành captcha nếu được yêu cầu

## Bước 5: Cấu hình Environment Variables

1. Copy file `.env.example` thành `.env`:
   ```bash
   cp .env.example .env
   ```

2. Mở file `.env` và điền thông tin:
   ```
   DISCORD_BOT_TOKEN=your_actual_discord_bot_token_here
   HUGGINGFACE_API_KEY=your_huggingface_api_key_here
   HUGGINGFACE_MODEL=microsoft/DialoGPT-medium
   ```

3. **Lấy HuggingFace API Key** (nếu cần):
   - Truy cập [HuggingFace](https://huggingface.co/)
   - Đăng ký/Đăng nhập
   - Vào Settings > Access Tokens
   - Tạo token mới với quyền "read"

## Bước 6: Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

## Bước 7: Chạy Bot

```bash
python discord_bot.py
```

Nếu thành công, bạn sẽ thấy:
```
[Bot Name] has connected to Discord!
Bot is in X guilds
```

## Cách sử dụng Bot

### Chat với Bot
Mention bot trong bất kỳ channel nào bot có quyền truy cập:
```
@YourBot xin chào!
```

### Commands
- `!ping` - Kiểm tra bot có hoạt động không
- `!reset` - Reset lịch sử hội thoại trong channel hiện tại
- `!help_bot` - Hiển thị thông tin trợ giúp

## Lưu ý quan trọng

1. **Bảo mật Token**: Không bao giờ commit file `.env` lên Git. File `.gitignore` nên có dòng `.env`
2. **Message Content Intent**: Phải được bật để bot có thể đọc nội dung tin nhắn
3. **Rate Limits**: HuggingFace API có giới hạn rate limit, nếu bot không phản hồi có thể do đã vượt quá giới hạn
4. **Conversation History**: Mỗi channel sẽ có lịch sử hội thoại riêng, sử dụng `!reset` để xóa lịch sử

## Troubleshooting

### Bot không phản hồi khi mention
- Kiểm tra **MESSAGE CONTENT INTENT** đã được bật chưa
- Kiểm tra bot có quyền "Read Messages" và "Send Messages" trong channel đó không

### Lỗi "Invalid Token"
- Kiểm tra lại token trong file `.env`
- Token có thể đã bị reset, lấy token mới từ Developer Portal

### Bot bị rate limit
- Đợi một lúc trước khi sử dụng tiếp
- Xem xét nâng cấp HuggingFace plan hoặc sử dụng API key có quota cao hơn

## Mở rộng thêm

Bạn có thể customize bot bằng cách:
- Thêm commands mới trong file [discord_bot.py](discord_bot.py)
- Thay đổi model HuggingFace trong `.env`
- Thêm reaction, embed, hoặc các tính năng Discord khác
