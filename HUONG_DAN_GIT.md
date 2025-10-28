# 🚀 HƯỚNG DẪN PUSH CODE LÊN GITHUB

## 📋 CHUẨN BỊ

### 1. Đã tạo file `.gitignore` ✅
File này giúp Git BỎ QUA các file không cần thiết như:
- ❌ `.env` (chứa API key - RẤT QUAN TRỌNG!)
- ❌ `venv/` (thư mục virtual environment - dung lượng lớn)
- ❌ `__pycache__/` (file cache Python)
- ❌ `.vscode/`, `.idea/` (settings IDE)

### 2. Kiểm tra Git đã cài chưa
```bash
git --version
```
Nếu chưa có, tải tại: https://git-scm.com/download/win

---

## 🎯 BƯỚC 1: TẠO REPOSITORY TRÊN GITHUB

1. Truy cập: https://github.com/new
2. Điền thông tin:
   - **Repository name**: `my-ai-chatbot` (hoặc tên bạn thích)
   - **Description**: "AI Chatbot using HuggingFace API and Flask"
   - **Public** hoặc **Private** (tùy bạn)
   - ❌ **KHÔNG** chọn "Add README" (vì mình đã có rồi)
   - ❌ **KHÔNG** chọn "Add .gitignore"
3. Click **Create repository**

---

## 🎯 BƯỚC 2: KHỞI TẠO GIT (Chạy lệnh trong terminal)

### Mở terminal tại folder dự án:
```bash
cd c:\KhoaTranVan\Personal\MY_AI_AGENT
```

### Khởi tạo Git repository:
```bash
git init
```

### Cấu hình thông tin của bạn (chỉ làm 1 lần):
```bash
git config --global user.name "Tên của bạn"
git config --global user.email "email@example.com"
```

---

## 🎯 BƯỚC 3: ADD VÀ COMMIT CODE

### Thêm tất cả files (trừ những file trong .gitignore):
```bash
git add .
```

### Kiểm tra xem file nào sẽ được commit:
```bash
git status
```

**⚠️ QUAN TRỌNG: Kiểm tra `.env` KHÔNG có trong danh sách!**

Nếu thấy `.env` trong danh sách, chạy:
```bash
git rm --cached .env
```

### Tạo commit đầu tiên:
```bash
git commit -m "Initial commit: HuggingFace Chatbot with Flask API"
```

---

## 🎯 BƯỚC 4: PUSH LÊN GITHUB

### Thêm remote repository (thay YOUR_USERNAME và REPO_NAME):
```bash
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

**Ví dụ:**
```bash
git remote add origin https://github.com/khoatranvan/my-ai-chatbot.git
```

### Đổi tên branch thành main (nếu cần):
```bash
git branch -M main
```

### Push code lên GitHub:
```bash
git push -u origin main
```

**Lần đầu push sẽ yêu cầu đăng nhập GitHub!**

---

## 🎯 CÁC LỆNH GIT CƠ BẢN (Sau này dùng)

### Xem trạng thái:
```bash
git status
```

### Thêm file mới hoặc file đã sửa:
```bash
git add .                  # Thêm tất cả
git add file_name.py       # Thêm 1 file cụ thể
```

### Commit thay đổi:
```bash
git commit -m "Mô tả thay đổi"
```

### Push lên GitHub:
```bash
git push
```

### Pull code mới nhất từ GitHub:
```bash
git pull
```

### Xem lịch sử commit:
```bash
git log --oneline
```

---

## ⚠️ CỰC KỲ QUAN TRỌNG!

### ❌ KHÔNG BAO GIỜ PUSH FILE `.env` LÊN GITHUB!

File `.env` chứa API key của bạn. Nếu push lên GitHub:
- ❌ Người khác có thể lấy API key của bạn
- ❌ Họ có thể dùng hết quota miễn phí của bạn
- ❌ Có thể bị lạm dụng

### ✅ Kiểm tra trước khi commit:
```bash
git status
```
Đảm bảo `.env` KHÔNG có trong danh sách!

### ⚠️ Nếu đã vô tình push .env:

**1. Xóa file khỏi Git (nhưng giữ lại local):**
```bash
git rm --cached .env
git commit -m "Remove .env from repository"
git push
```

**2. ĐỔI API KEY NGAY LẬP TỨC:**
- Truy cập: https://huggingface.co/settings/tokens
- Xóa token cũ
- Tạo token mới
- Cập nhật file `.env`

---

## 📝 FILE CẤU TRÚC SẼ ĐƯỢC PUSH

```
MY_AI_AGENT/
├── src/
│   ├── chatbot.py          ✅
│   └── app_flask.py        ✅
├── .gitignore              ✅
├── .env.example            ✅ (template, không có key thật)
├── requirements.txt        ✅
├── README.md               ✅
├── HUONG_DAN_DON_GIAN.md  ✅
├── demo.py                 ✅
├── quick_test.py           ✅
├── test_api_simple.py      ✅
├── start_server.bat        ✅
├── test_chat.bat           ✅
└── test_api.bat            ✅
```

### KHÔNG được push:
- ❌ `.env` (chứa API key)
- ❌ `venv/` (virtual environment)
- ❌ `__pycache__/` (cache)
- ❌ `.vscode/`, `.idea/` (IDE settings)

---

## 🎓 HỌC THÊM VỀ GIT

- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [GitHub Docs](https://docs.github.com/)

---

## 🚀 TÓM TẮT NHANH - COPY & PASTE

```bash
# 1. Khởi tạo Git
cd c:\KhoaTranVan\Personal\MY_AI_AGENT
git init

# 2. Config (chỉ làm 1 lần)
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 3. Add và commit
git add .
git status              # Kiểm tra .env KHÔNG có trong list
git commit -m "Initial commit: HuggingFace Chatbot"

# 4. Push lên GitHub (thay YOUR_USERNAME/REPO_NAME)
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git push -u origin main
```

---

## ❓ CÂU HỎI THƯỜNG GẶP

**Q: Làm sao để người khác chạy được code sau khi clone?**

A: Họ cần:
1. Clone repo
2. Tạo virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Cài packages: `pip install -r requirements.txt`
5. Tạo file `.env` và thêm API key của họ
6. Chạy: `start_server.bat`

**Q: Tôi có nên push `app.js` (file Node.js cũ) không?**

A: Không cần nếu bạn không dùng nữa. Hoặc xóa hoặc để đấy cũng được (không hại).

**Q: Public hay Private repository?**

A:
- **Public**: Ai cũng xem được code (nhưng không có API key nên không chạy được)
- **Private**: Chỉ bạn xem được

**Q: Có thể đổi tên file không?**

A: Có! Miễn sao rõ ràng và dễ hiểu.

---

🎉 **Chúc bạn push code thành công!**
