"""
Test API đơn giản - Gửi tin nhắn đến chatbot
Chạy: python test_api_simple.py
"""

import requests
import json

API_URL = "http://localhost:5000"

def test_chat(message):
    """Gửi tin nhắn và nhận phản hồi"""
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={"message": message},
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            return data.get("bot_response", "Không có phản hồi")
        else:
            return f"Lỗi: {response.status_code}"

    except requests.exceptions.ConnectionError:
        return "❌ Không thể kết nối! Server có đang chạy không?\n   Chạy: start_server.bat"
    except Exception as e:
        return f"❌ Lỗi: {str(e)}"

def reset_chat():
    """Reset lịch sử chat"""
    try:
        response = requests.post(f"{API_URL}/reset", timeout=10)
        return response.json().get("message", "OK")
    except Exception as e:
        return f"Lỗi: {str(e)}"

def main():
    print("=" * 60)
    print("🤖 TEST CHATBOT API")
    print("=" * 60)
    print(f"API URL: {API_URL}")
    print()

    # Kiểm tra server
    print("[1] Kiểm tra server đang chạy...")
    try:
        response = requests.get(API_URL, timeout=5)
        print("✅ Server đang hoạt động!")
        print()
    except:
        print("❌ Server không chạy! Hãy chạy: start_server.bat")
        print()
        return

    # Test với các câu hỏi
    questions = [
        "Xin chào! Bạn là ai?",
        "Cho tôi biết về Python?",
        "Viết code hello world bằng Python"
    ]

    for i, question in enumerate(questions, 1):
        print(f"[{i}] Câu hỏi: {question}")
        print("-" * 60)

        response = test_chat(question)
        print(f"🤖 Bot: {response}")
        print()

    # Reset chat
    print("[Reset] Xóa lịch sử chat...")
    result = reset_chat()
    print(f"✅ {result}")
    print()

    print("=" * 60)
    print("✅ Hoàn thành test!")
    print()
    print("💡 Để chat tự do, chạy:")
    print("   venv\\Scripts\\python.exe demo.py")

if __name__ == "__main__":
    main()
