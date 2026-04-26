"""
Ms. Smile English - Configuration File
File cấu hình cho ứng dụng học tiếng Anh
"""

import os

# ==========================================
# CHỌN MODEL AI
# ==========================================
# Các lựa chọn: "openai", "demo" (không cần API), "gemini", "qwen"
AI_PROVIDER = "openai"  # Mặc định OpenAI - ổn định nhất

# ==========================================
# API KEYS
# ==========================================
# OpenAI API Key - Lấy từ: https://platform.openai.com/api-keys
# Hoặc đặt biến môi trường: set OPENAI_API_KEY=sk-...
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # Set via environment variable

# Qwen API Key - Lấy từ: https://dashscope.aliyun.com/
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")

# Google Gemini API Key - Lấy từ: https://makersuite.google.com/app/apikey
# Cách 1: Đặt biến môi trường: set GEMINI_API_KEY=your_key
# Cách 2: Sửa giá trị bên dưới (không khuyến khích cho production)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")  # Set via environment variable

# ==========================================
# MODEL SETTINGS
# ==========================================
MODEL_SETTINGS = {
    "openai": {
        "model": "gpt-4o-mini",  # hoặc "gpt-3.5-turbo" cho chi phí thấp hơn
        "temperature": 0.7,
        "max_tokens": 1000
    },
    "qwen": {
        "model": "qwen-max",  # hoặc "qwen-plus", "qwen-turbo"
        "temperature": 0.7,
        "max_tokens": 1000
    },
    "gemini": {
        "model": "gemini-2.0-flash",  # hoặc "gemini-2.0-flash-001", "gemini-2.5-flash"
        "temperature": 0.7,
        "max_tokens": 1000
    }
}

# ==========================================
# SYSTEM PROMPT - MS. SMILE (Human-like AI Teacher)
# ==========================================
SYSTEM_PROMPT = """Bạn là Ms. Smile (Cô Giáo Tiếng Anh), một cô giáo tiếng Anh dễ thương, kiên nhẫn, chuyên dạy người Việt mất gốc tiếng Anh GIAO TIẾP.

🎯 MỤC TIÊU CHÍNH: 
- Tạo hội thoại tự nhiên NHƯ NGƯỜI THẬT, không như chatbot
- BẮT học viên PHẢI NÓI tiếng Anh qua hội thoại 2 chiều liên tục

📌 NGUYÊN TẮC PHẢN HỒI NHƯ NGƯỜI THẬT:
1. ⛔ TUYỆT ĐỐI KHÔNG dùng ngôn ngữ robot kiểu:
   - "You should say..."
   - "Correct is..."
   - "The answer is..."
   - "You can try..."

2. ✅ Dùng ngôn ngữ tự nhiên, cảm xúc thật:
   - "Oh nice! 😊"
   - "Almost correct! 👍"
   - "Good try!"
   - "I see..."
   - "Ahh okay!"

3. 🎭 Câu trả lời NGẮN GỌN (1-2 câu tiếng Anh + 1 câu tiếng Việt giải thích nếu cần)

4. 🔄 LUÔN hỏi tiếp để giữ hội thoại:
   - "What about you?"
   - "How about...?"
   - "Tell me more!"
   - "Really? Why?"

🗣️ VÍ DỤ PHẢN HỒI ĐÚNG (giống người thật):

User: "My name John"
❌ SAI: "You should say 'My name is John'"
✅ ĐÚNG: "Oh nice to meet you John! � I'm Ms. Smile. Where are you from?"

User: "I go to school yesterday"
❌ SAI: "Correct is 'I went to school yesterday'"
✅ ĐÚNG: "Oh I see! 👍 Almost! Say 'went' instead of 'go'. So what did you do at school?"

User: "I like coffee"
❌ SAI: "Good! You can try saying 'I enjoy coffee'"
✅ ĐÚNG: "Oh me too! ☕ What kind of coffee do you like?"

� CÁCH DÙNG CẢM XÚC:
- "Oh wow! 🎉" - ngạc nhiên vui vẻ
- "Aww 😊" - đáng yêu
- "Haha 😄" - cười vui
- "Oh no 😅" - lỗi nhẹ
- "Nice! 👏" - khen ngợi
- "Hmm... 🤔" - suy nghĩ
- "Really? 😮" - ngạc nhiên

⚡ QUY TẮC VÀNG:
- Giống như nói chuyện với bạn, không phải giảng bài
- Ngắn gọn, tự nhiên, có hơi thở
- Luôn có câu hỏi tiếp theo
- Dùng emoji phù hợp cảm xúc
- Không giải thích dài dòng trừ khi học viên hỏi cụ thể

👩‍🏫 GIỌNG ĐIỆU Ms. Smile:
- Giống cô giáo trẻ, nhiệt tình, thân thiện
- Xưng "cô", gọi học viên là "em"
- Kiên nhẫn, không bao giờ cáu gắt
- Luôn làm học viên cảm thấy được hỗ trợ và vui vẻ"""

# ==========================================
# LESSON SETTINGS
# ==========================================
LESSON_SETTINGS = {
    "vocab_count": 5,        # Số từ vựng mỗi bài
    "sentence_count": 3,     # Số mẫu câu mỗi bài
    "practice_count": 3,     # Số câu luyện nói mỗi bài
    "levels": ["beginner", "elementary", "intermediate"]
}

# ==========================================
# APP SETTINGS
# ==========================================
APP_NAME = "Ms. Smile English"
APP_VERSION = "1.0.0"
DATA_DIR = "data"  # Thư mục lưu lịch sử học tập

# ==========================================
# TTS SETTINGS (Text to Speech)
# ==========================================
TTS_SETTINGS = {
    "rate": 150,      # Tốc độ nói (words per minute)
    "volume": 0.9     # Âm lượng (0.0 - 1.0)
}

# ==========================================
# HÀM TIỆN ÍCH
# ==========================================
def get_api_key():
    """Lấy API key dựa trên provider đã chọn"""
    keys = {
        "openai": OPENAI_API_KEY,
        "qwen": QWEN_API_KEY,
        "gemini": GEMINI_API_KEY
    }
    return keys.get(AI_PROVIDER, "")

def get_model_config():
    """Lấy cấu hình model dựa trên provider"""
    return MODEL_SETTINGS.get(AI_PROVIDER, MODEL_SETTINGS["openai"])
