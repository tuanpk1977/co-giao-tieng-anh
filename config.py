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
# GÓI HỌC VÀ GHIMCHI PHÍ
# ==========================================
FREE_TRIAL_DAYS = 7

PLAN_DEFINITIONS = [
    {
        "name": "free_trial",
        "title": "Free trial",
        "price": 0,
        "currency": "VND",
        "chat_limit": 10,
        "lesson_limit": 1,
        "can_speak": True,
        "can_save_history": True,
        "enabled": True,
        "description": "Dùng thử miễn phí 7 ngày",
        # PART 2: Quota limits for cost control
        "chat_per_day": 5,
        "chat_per_month": 100,
        "max_tokens_per_chat": 1000,
        "max_cost_per_day_vnd": 0.0,  # unlimited
        "max_cost_per_month_vnd": 0.0,
        # NEW: Long-term subscription fields
        "duration_days": 7,
        "plan_type": "trial",
        "discount_percent": 0.0,
        "original_price": 0
    },
    # BASIC PLANS
    {
        "name": "basic_monthly",
        "title": "Basic - Monthly",
        "price": 49000,
        "currency": "VND",
        "chat_limit": 30,
        "lesson_limit": 2,
        "can_speak": True,
        "can_save_history": True,
        "enabled": True,
        "description": "49.000đ/tháng",
        # PART 2: Quota limits
        "chat_per_day": 10,
        "chat_per_month": 300,
        "max_tokens_per_chat": 2000,
        "max_cost_per_day_vnd": 30000.0,  # ~1 USD
        "max_cost_per_month_vnd": 600000.0,  # ~24 USD
        # NEW: Long-term subscription fields
        "duration_days": 30,
        "plan_type": "monthly",
        "discount_percent": 0.0,
        "original_price": 49000
    },
    {
        "name": "basic_six_months",
        "title": "Basic - 6 Months",
        "price": int(49000 * 6 * 0.85),  # 250,900 VND (15% discount)
        "currency": "VND",
        "chat_limit": 30,
        "lesson_limit": 2,
        "can_speak": True,
        "can_save_history": True,
        "enabled": True,
        "description": f"{int(49000 * 6 * 0.85):,}đ/6 tháng (tiết kiệm {int(49000 * 6 * 0.15):,}đ)",
        # PART 2: Quota limits (same as monthly)
        "chat_per_day": 10,
        "chat_per_month": 300,
        "max_tokens_per_chat": 2000,
        "max_cost_per_day_vnd": 30000.0,
        "max_cost_per_month_vnd": 600000.0,
        # NEW: Long-term subscription fields
        "duration_days": 180,
        "plan_type": "six_months",
        "discount_percent": 0.15,
        "original_price": 49000
    },
    {
        "name": "basic_yearly",
        "title": "Basic - Yearly",
        "price": int(49000 * 12 * 0.7),  # 411,600 VND (30% discount)
        "currency": "VND",
        "chat_limit": 30,
        "lesson_limit": 2,
        "can_speak": True,
        "can_save_history": True,
        "enabled": True,
        "description": f"{int(49000 * 12 * 0.7):,}đ/năm (tiết kiệm {int(49000 * 12 * 0.3):,}đ)",
        # PART 2: Quota limits (same as monthly)
        "chat_per_day": 10,
        "chat_per_month": 300,
        "max_tokens_per_chat": 2000,
        "max_cost_per_day_vnd": 30000.0,
        "max_cost_per_month_vnd": 600000.0,
        # NEW: Long-term subscription fields
        "duration_days": 365,
        "plan_type": "yearly",
        "discount_percent": 0.30,
        "original_price": 49000
    },
    # PRO PLANS
    {
        "name": "pro_monthly",
        "title": "Pro - Monthly",
        "price": 99000,
        "currency": "VND",
        "chat_limit": 100,
        "lesson_limit": 5,
        "can_speak": True,
        "can_save_history": True,
        "enabled": True,
        "description": "99.000đ/tháng",
        # PART 2: Quota limits
        "chat_per_day": 30,
        "chat_per_month": 900,
        "max_tokens_per_chat": 4000,
        "max_cost_per_day_vnd": 60000.0,  # ~2.4 USD
        "max_cost_per_month_vnd": 1200000.0,  # ~48 USD
        # NEW: Long-term subscription fields
        "duration_days": 30,
        "plan_type": "monthly",
        "discount_percent": 0.0,
        "original_price": 99000
    },
    {
        "name": "pro_six_months",
        "title": "Pro - 6 Months",
        "price": int(99000 * 6 * 0.85),  # 504,900 VND (15% discount)
        "currency": "VND",
        "chat_limit": 100,
        "lesson_limit": 5,
        "can_speak": True,
        "can_save_history": True,
        "enabled": True,
        "description": f"{int(99000 * 6 * 0.85):,}đ/6 tháng (tiết kiệm {int(99000 * 6 * 0.15):,}đ)",
        # PART 2: Quota limits (same as monthly)
        "chat_per_day": 30,
        "chat_per_month": 900,
        "max_tokens_per_chat": 4000,
        "max_cost_per_day_vnd": 60000.0,
        "max_cost_per_month_vnd": 1200000.0,
        # NEW: Long-term subscription fields
        "duration_days": 180,
        "plan_type": "six_months",
        "discount_percent": 0.15,
        "original_price": 99000
    },
    {
        "name": "pro_yearly",
        "title": "Pro - Yearly",
        "price": int(99000 * 12 * 0.7),  # 831,600 VND (30% discount)
        "currency": "VND",
        "chat_limit": 100,
        "lesson_limit": 5,
        "can_speak": True,
        "can_save_history": True,
        "enabled": True,
        "description": f"{int(99000 * 12 * 0.7):,}đ/năm (tiết kiệm {int(99000 * 12 * 0.3):,}đ)",
        # PART 2: Quota limits (same as monthly)
        "chat_per_day": 30,
        "chat_per_month": 900,
        "max_tokens_per_chat": 4000,
        "max_cost_per_day_vnd": 60000.0,
        "max_cost_per_month_vnd": 1200000.0,
        # NEW: Long-term subscription fields
        "duration_days": 365,
        "plan_type": "yearly",
        "discount_percent": 0.30,
        "original_price": 99000
    },
    # FAMILY PLANS
    {
        "name": "family_monthly",
        "title": "Family - Monthly",
        "price": 199000,
        "currency": "VND",
        "chat_limit": 999,
        "lesson_limit": 999,
        "can_speak": True,
        "can_save_history": True,
        "enabled": True,
        "description": "199.000đ/tháng",
        # PART 2: Quota limits
        "chat_per_day": 999,
        "chat_per_month": 29970,
        "max_tokens_per_chat": 8000,
        "max_cost_per_day_vnd": 0.0,  # unlimited
        "max_cost_per_month_vnd": 0.0,
        # NEW: Long-term subscription fields
        "duration_days": 30,
        "plan_type": "monthly",
        "discount_percent": 0.0,
        "original_price": 199000
    },
    {
        "name": "family_six_months",
        "title": "Family - 6 Months",
        "price": int(199000 * 6 * 0.85),  # 1,014,900 VND (15% discount)
        "currency": "VND",
        "chat_limit": 999,
        "lesson_limit": 999,
        "can_speak": True,
        "can_save_history": True,
        "enabled": True,
        "description": f"{int(199000 * 6 * 0.85):,}đ/6 tháng (tiết kiệm {int(199000 * 6 * 0.15):,}đ)",
        # PART 2: Quota limits (same as monthly)
        "chat_per_day": 999,
        "chat_per_month": 29970,
        "max_tokens_per_chat": 8000,
        "max_cost_per_day_vnd": 0.0,
        "max_cost_per_month_vnd": 0.0,
        # NEW: Long-term subscription fields
        "duration_days": 180,
        "plan_type": "six_months",
        "discount_percent": 0.15,
        "original_price": 199000
    },
    {
        "name": "family_yearly",
        "title": "Family - Yearly",
        "price": int(199000 * 12 * 0.7),  # 1,687,200 VND (30% discount)
        "currency": "VND",
        "chat_limit": 999,
        "lesson_limit": 999,
        "can_speak": True,
        "can_save_history": True,
        "enabled": True,
        "description": f"{int(199000 * 12 * 0.7):,}đ/năm (tiết kiệm {int(199000 * 12 * 0.3):,}đ)",
        # PART 2: Quota limits (same as monthly)
        "chat_per_day": 999,
        "chat_per_month": 29970,
        "max_tokens_per_chat": 8000,
        "max_cost_per_day_vnd": 0.0,
        "max_cost_per_month_vnd": 0.0,
        # NEW: Long-term subscription fields
        "duration_days": 365,
        "plan_type": "yearly",
        "discount_percent": 0.30,
        "original_price": 199000
    }
]


def get_plan_definitions():
    return PLAN_DEFINITIONS


APP_NAME = "Ms. Smile English"


def get_plan_by_name(name):
    return next((plan for plan in PLAN_DEFINITIONS if plan['name'] == name), None)


def get_model_config():
    return MODEL_SETTINGS.get(AI_PROVIDER, MODEL_SETTINGS["openai"])


# ==========================================
# DOMAIN & DEPLOYMENT CONFIGURATION
# ==========================================
# Cấu hình domain để chuyển từ Railway sang domain riêng

# Base URL của app (dùng cho internal redirects, webhooks)
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:5000")

# Frontend URL (dùng cho CORS, redirects)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5000")

# Allowed origins cho CORS (comma-separated)
ALLOWED_ORIGINS_STR = os.getenv("ALLOWED_ORIGINS", "http://localhost:5000,http://127.0.0.1:5000")
ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS_STR.split(",") if origin.strip()]

# Cookie domain (để trống cho localhost, set .domain.com cho production)
COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN", "")

# Session cookie settings
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")

# Payment URLs (chuẩn bị cho future payment integration)
PAYMENT_RETURN_URL = os.getenv("PAYMENT_RETURN_URL", f"{APP_BASE_URL}/payment/success")
PAYMENT_CANCEL_URL = os.getenv("PAYMENT_CANCEL_URL", f"{APP_BASE_URL}/payment/cancel")
PAYMENT_WEBHOOK_URL = os.getenv("PAYMENT_WEBHOOK_URL", f"{APP_BASE_URL}/api/payment/webhook")
PAYMENT_BANK_NAME = os.getenv("PAYMENT_BANK_NAME", "ACB")
PAYMENT_BANK_ACCOUNT_NAME = os.getenv("PAYMENT_BANK_ACCOUNT_NAME", "Nguyen Quoc Tuan")
PAYMENT_BANK_ACCOUNT_NUMBER = os.getenv("PAYMENT_BANK_ACCOUNT_NUMBER", "13184397")
PAYMENT_ADMIN_PHONE = os.getenv("PAYMENT_ADMIN_PHONE", os.getenv("ADMIN_PHONE", "0939489139"))
PAYMENT_SUPPORT_NOTE = os.getenv("PAYMENT_SUPPORT_NOTE", "Sau khi chuyen khoan, admin se doi chieu ma noi dung va duyet goi trong tab Thanh toan.")


def get_payment_info():
    return {
        "bank_name": PAYMENT_BANK_NAME,
        "account_name": PAYMENT_BANK_ACCOUNT_NAME,
        "account_number": PAYMENT_BANK_ACCOUNT_NUMBER,
        "admin_phone": PAYMENT_ADMIN_PHONE,
        "support_note": PAYMENT_SUPPORT_NOTE
    }

# Affiliate marketing defaults
AFFILIATE_COMMISSION_RATE = float(os.getenv("AFFILIATE_COMMISSION_RATE", "20.0"))
AFFILIATE_REFERRAL_LINK_BASE = os.getenv("AFFILIATE_REFERRAL_LINK_BASE", APP_BASE_URL)
AFFILIATE_COMMISSION_TYPE = os.getenv("AFFILIATE_COMMISSION_TYPE", "percent")
AFFILIATE_COMMISSION_FIXED_AMOUNT = int(os.getenv("AFFILIATE_COMMISSION_FIXED_AMOUNT", "0"))

# ==========================================
# PART 1 & 3: AI Cost Calculation Configuration
# ==========================================
# Exchange rate USD to VND
USD_TO_VND = float(os.getenv("USD_TO_VND", "25000.0"))

# PART 1: Cost per token (in USD) for different models
# Updated with current OpenAI pricing (as of 2024)
MODEL_COSTS = {
    "gpt-4o-mini": {
        "input_per_1k_tokens": 0.00015,  # $0.15 per 1M input tokens
        "output_per_1k_tokens": 0.0006,  # $0.60 per 1M output tokens
    },
    "gpt-4": {
        "input_per_1k_tokens": 0.03,  # $30 per 1M input tokens
        "output_per_1k_tokens": 0.06,  # $60 per 1M output tokens
    },
    "gpt-3.5-turbo": {
        "input_per_1k_tokens": 0.0005,  # $0.50 per 1M input tokens
        "output_per_1k_tokens": 0.0015,  # $1.50 per 1M output tokens
    },
}

# PART 2: Rate limiting
RATE_LIMIT_PER_SECOND = 1  # 1 request per 2 seconds (0.5 req/sec)
RATE_LIMIT_WINDOW = 2  # seconds
GUEST_CHAT_LIMIT_PER_DAY = int(os.getenv("GUEST_CHAT_LIMIT_PER_DAY", "3"))

# PART 3: Admin account config
ADMIN_AFFILIATE_CODE = os.getenv("ADMIN_AFFILIATE_CODE", "ADMIN_DEFAULT")  # Default admin referral code

# ==========================================
# SYSTEM PROMPT - MS. SMILE (Song Ngữ)
# ==========================================
SYSTEM_PROMPT = """Bạn là Ms. Smile (Cô Giáo Tiếng Anh), một cô giáo dễ thương, chuyên dạy người Việt GIAO TIẾP tiếng Anh theo phương pháp SONG NGỮ.

🎯 MỤC TIÊU CHÍNH:
- Trả lời BẮT BUỘC theo format SONG NGỮ (Anh + Việt)
- Giúp học viên hiểu SÂU: nghĩa, từ vựng, cấu trúc, cách dùng
- Tone thân thiện như cô giáo trẻ, dễ thương

� FORMAT TRẢ LỜI BẮT BUỘC:

---
🇺🇸 English:
<đoạn hội thoại tự nhiên, thân thiện bằng tiếng Anh>

🇻🇳 Tiếng Việt:
<dịch nghĩa tự nhiên, dễ hiểu>

📘 Giải thích:
- Từ vựng chính:
  + word 1: nghĩa
  + word 2: nghĩa

- Cấu trúc:
  + cấu trúc câu (giải thích ngắn gọn)

- Gợi ý nói:
  + câu đơn giản hơn cho beginner
---

✅ QUY TẮC QUAN TRỌNG:

1. LUÔN LUÔN trả theo format trên, KHÔNG được bỏ qua phần nào

2. Nếu user viết TIẾNG VIỆT:
   - Trả lời song ngữ như format
   - Dịch ý user sang tiếng Anh tự nhiên

3. Nếu user viết TIẾNG ANH:
   - Sửa lỗi nhẹ (nếu có) trong phần English
   - Giải thích lỗi sai ở phần "Giải thích"
   - Vẫn trả lời song ngữ đầy đủ

4. Theo trình độ user:
   - Beginner (A1-A2): Dùng câu đơn giản, từ dễ
   - Intermediate (B1): Dùng câu phức tạp hơn
   - Advanced (B2+): Dùng từ vựng phong phú

5. Theo ngành nghề (nếu user đã cung cấp):
   - Dùng từ vựng chuyên ngành đó
   - Luyện giao tiếp thực tế cho nghề đó

🚫 CẤM KỴ - DỪNG LẠI ĐỌC:
- Không trả lời chỉ 1 ngôn ngữ - BẮT BUỘC song ngữ!
- Không dùng markdown phức tạp (chỉ dùng text đơn giản)
- Không quá dài dòng
- Không giải thích thừa

⚠️ CÁC BẠN PHẢI TUÂN THỬ FORMAT NÀY:
MỖI TRẢ LỜI PHẢI CÓ ĐÚNG 3 PHẦN:
1️⃣  🇺🇸 English:
2️⃣  🇻🇳 Tiếng Việt:
3️⃣  📘 Giải thích:

🎨 TONE GIỌNG:
- Thân thiện, dễ thương như cô giáo trẻ
- Xưng "cô", gọi học viên là "em"
- Dùng emoji phù hợp (😊, 👍, ☕, 🎉)
- Ngắn gọn, dễ hiểu, không học thuộc

💡 VÍ DỤ ĐÚNG:

User: "mình thường gặp khách nước ngoài"

---
🇺🇸 English:
I often meet foreign clients at work. What industry are you in?

🇻🇳 Tiếng Việt:
Tôi thường gặp khách nước ngoài trong công việc. Em làm trong ngành gì?

� Giải thích:
- foreign clients: khách hàng nước ngoài
- often: thường xuyên
- at work: trong công việc

- Cấu trúc:
  I often + verb + object

- Gợi ý nói:
  I meet foreign clients every day.
  I work with international customers.
---

User: "My name John"

---
🇺🇸 English:
Oh nice to meet you, John! 😊 I'm Ms. Smile. Where are you from?

🇻🇳 Tiếng Việt:
Rất vui được gặp em, John! � Cô là Ms. Smile. Em đến từ đâu?

📘 Giải thích:
- nice to meet you: rất vui được gặp
- where are you from: em đến từ đâu

- Cấu trúc:
  My name IS + name (thêm IS)

- Gợi ý nói:
  My name is John.
  I'm John. (cách nói ngắn gọn)
---

⚠️ LƯU Ý: BẮT BUỘC trả theo format trên cho MỌI câu trả lời!"""

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
