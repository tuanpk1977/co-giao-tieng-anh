"""
Ms. Smile English - Main Flask Application
Backend API cho ứng dụng học tiếng Anh
"""

# VERSION - để track deploy
APP_VERSION = "hybrid-roadmap-021"

from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import json

# Import services
from services.ai_service import get_ai_service
from services.roleplay_service import get_roleplay_service, ROLES, SITUATIONS
from services.situation_advisor import get_situation_advisor
from services.user_service import get_user_service
from services.cost_service import get_cost_service  # PART 1 & 3: Cost tracking
from services.quota_service import get_quota_service  # PART 2: Quota enforcement
from services.roadmap_service import get_roadmap_service
from services.ai_usage_service import get_ai_usage_service
from utils.history import get_history_manager
from utils.user_profile import (
    load_profile, save_profile, update_profile, is_onboarded,
    get_profile_for_prompt, reset_profile, normalize_user_profile
)

app = Flask(__name__, 
    template_folder='templates',
    static_folder='static'
)

# Import config after app creation to avoid circular import
import config as app_config

# CORS configuration
CORS(app, origins=app_config.ALLOWED_ORIGINS, supports_credentials=True)

# Session configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SESSION_COOKIE_DOMAIN'] = app_config.COOKIE_DOMAIN if app_config.COOKIE_DOMAIN else None
app.config['SESSION_COOKIE_SECURE'] = app_config.SESSION_COOKIE_SECURE
app.config['SESSION_COOKIE_SAMESITE'] = app_config.SESSION_COOKIE_SAMESITE
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=180)

# Database configuration
database_url = os.getenv('DATABASE_URL')
if not database_url:
    volume_path = os.getenv('RAILWAY_VOLUME_MOUNT_PATH') or os.getenv('VOLUME_MOUNT_PATH')
    if volume_path:
        os.makedirs(volume_path, exist_ok=True)
        database_url = f"sqlite:///{os.path.join(volume_path, 'ms_smile.db')}"
    else:
        database_url = 'sqlite:///ms_smile.db'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
from models import init_db, db
init_db(app)

# Global instances
ai_service = None
history_manager = None
_roleplay_service = None

@app.route('/')
def index():
    """Trang chủ - Render giao diện chính"""
    return render_template('index.html')

@app.route('/api/version')
def api_version():
    return jsonify({
        "version": APP_VERSION,
        "file": "app.py",
        "ok": True
    })

@app.route('/api/health', methods=['GET'])
def api_health():
    return jsonify({
        "ok": True,
        "status": "healthy",
        "version": APP_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/health/domain', methods=['GET'])
def health_domain():
    """Endpoint kiểm tra cấu hình domain production"""
    return jsonify({
        "success": True,
        "app": "Ms. Smile English",
        "app_base_url": app_config.APP_BASE_URL,
        "frontend_url": app_config.FRONTEND_URL,
        "allowed_origins": app_config.ALLOWED_ORIGINS,
        "cookie_domain": app_config.COOKIE_DOMAIN,
        "session_secure": app_config.SESSION_COOKIE_SECURE,
        "session_samesite": app_config.SESSION_COOKIE_SAMESITE,
        "version": "domain-ready-v1"
    })

@app.route('/version')
def version():
    """Trả về version hiện tại - BILINGUAL V5"""
    return jsonify({
        "app": "Ms Smile English",
        "version": "bilingual-v5",
        "bilingual": True,
        "status": "running",
        "features": ["bilingual", "vn_en_explain", "song_ngu"],
        "deployed_at": "2026-04-27",
        "railway": "active"
    })

@app.route('/api/test-bilingual', methods=['GET'])
def test_bilingual():
    """Test endpoint trả về response song ngữ mẫu"""
    test_reply = """US English:
I am from Vietnam.

VN Tiếng Việt:
Tôi đến từ Việt Nam.

📘 Giải thích:
- from: đến từ
- Vietnam viết liền, không viết VietNam
- Cấu trúc: I am from + country
- Gợi ý: Tôi đến từ + tên quốc gia"""
    return jsonify({
        "success": True,
        "reply": test_reply,
        "response": test_reply,
        "test": True,
        "version": APP_VERSION
    })

@app.route('/api/profile', methods=['GET', 'POST'])
def profile():
    """
    API endpoint để quản lý user profile
    
    GET: Lấy profile hiện tại
    POST: Cập nhật profile { field: value, ... }
    """
    try:
        if request.method == 'GET':
            profile = load_profile()
            return jsonify({
                "success": True,
                "profile": profile,
                "onboarded": is_onboarded()
            })
        else:
            data = request.json or {}
            profile = update_profile(data)
            return jsonify({
                "success": True,
                "profile": profile,
                "message": "Profile updated successfully"
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/profile/onboarded', methods=['GET'])
def check_onboarded():
    """Kiểm tra xem user đã hoàn thành onboarding chưa"""
    return jsonify({
        "success": True,
        "onboarded": is_onboarded()
    })


@app.route('/api/profile/reset', methods=['POST'])
def reset_user_profile():
    """Reset profile về mặc định"""
    try:
        reset_profile()
        return jsonify({
            "success": True,
            "message": "Profile reset successfully"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    API endpoint để chat với Ms. Smile (đã cá nhân hóa)
    
    Request body:
    {
        "message": "Tin nhắn của người dùng",
        "user_id": 1,  // optional - để cá nhân hóa theo user
        "history": [  // optional
            {"role": "user", "content": "..."},
            {"role": "assistant", "content": "..."}
        ]
    }
    
    Response:
    {
        "success": true,
        "response": "Phản hồi từ AI",
        "timestamp": "2024-01-01T00:00:00"
    }
    """
    try:
        print(f"\n[CHAT API v{APP_VERSION}] Received request")
        
        data = request.json
        user_message = data.get('message', '').strip()
        user_id = data.get('user_id')
        conversation_history = data.get('history', [])
        
        print(f"[CHAT] User message: {user_message[:50]}...")
        print(f"[CHAT] User ID: {user_id}")
        
        if not user_message:
            return jsonify({
                "success": False,
                "error": "Vui lòng nhập tin nhắn"
            }), 400
        
        # PART 2: Check quota before calling AI
        user_service = get_user_service()
        quota_service = get_quota_service()
        cost_service = get_cost_service()
        
        user = None
        plan_name = "free_trial"
        limit_message = """US English:
You have reached today's free limit. Please upgrade your plan to continue.

VN Tiếng Việt:
Em đã dùng hết lượt miễn phí hôm nay. Vui lòng nâng cấp gói để tiếp tục học.

📘 Giải thích:
Giới hạn dùng thử giúp hệ thống kiểm soát chi phí AI."""
        
        if user_id:
            user = user_service.get_user(user_id)
            if user:
                plan_name = user.plan_name or "free_trial"
                
                # Check if user is locked or expired
                if user.is_locked or user.status == 'banned':
                    return jsonify({
                        'success': False,
                        'error': 'Tài khoản đã bị khóa. Liên hệ admin để mở lại.',
                        'message': 'Tài khoản đã bị khóa. Liên hệ admin để mở lại.'
                    }), 403
        else:
            today_key = datetime.utcnow().date().isoformat()
            if session.get('guest_chat_date') != today_key:
                session['guest_chat_date'] = today_key
                session['guest_chat_count'] = 0
            if session.get('guest_chat_count', 0) >= app_config.GUEST_CHAT_LIMIT_PER_DAY:
                return jsonify({
                    'success': False,
                    'error': limit_message,
                    'message': limit_message,
                    'limits': {
                        'daily_chats': app_config.GUEST_CHAT_LIMIT_PER_DAY,
                        'chats_remaining_today': 0
                    }
                }), 429

        # PART 2: Check daily chat quota
        quota_check = quota_service.check_can_chat(user_id, plan_name)
        if not quota_check['allowed']:
            return jsonify({
                'success': False,
                'error': limit_message,
                'message': limit_message,
                'limits': quota_check['limits']
            }), 429  # 429 = Too Many Requests
        
        # Lấy AI service
        service = get_ai_service()
        
        # DEBUG LOG
        import config as app_config
        print(f"[CHAT DEBUG] Provider: {app_config.AI_PROVIDER}")
        print(f"[CHAT DEBUG] Bilingual format: ENABLED")
        
        try:
            # Build user profile cho AI context
            user_profile = None
            if user_id:
                if user:
                    if user.status == 'expired':
                        return jsonify({
                            'success': False,
                            'error': 'Tài khoản đã hết hạn. Vui lòng gia hạn để tiếp tục.',
                            'message': 'Tài khoản đã hết hạn. Vui lòng gia hạn để tiếp tục.'
                        }), 403
                    profile = user.get_profile_for_ai()
                    user_profile = {
                        'level': profile['level'],
                        'occupation': profile['job'],
                        'goal': profile['goal'],
                        'meet_foreigners': profile['meet_foreigners']
                    }

            if not user_profile:
                # Fallback to local profile
                local_profile = get_profile_for_prompt()
                # ✅ Normalize local_profile - FIX cho lỗi 'str' object has no attribute 'get'
                local_profile = normalize_user_profile(local_profile)
                if local_profile:
                    user_profile = {
                        'level': local_profile.get('level', 'beginner'),
                        'occupation': local_profile.get('job', ''),
                        'goal': local_profile.get('goal', ''),
                        'meet_foreigners': local_profile.get('meet_foreigners', False)
                    }
            
            # ✅ Normalize user_profile trước khi gọi AI
            user_profile = normalize_user_profile(user_profile)
            
            # Gọi AI với user profile để cá nhân hóa
            ai_response = service.chat(user_message, conversation_history, user_profile=user_profile)
            
        except Exception as e:
            print(f"[CHAT ERROR] Exception caught: {str(e)}")
            import traceback
            print(traceback.format_exc())
            # ✅ Exception format SONG NGỮ đúng chuẩn
            ai_response = f"""🇺🇸 English:
❌ System error: {str(e)}

🇻🇳 Tiếng Việt:
Hệ thống gặp lỗi khi xử lý. Vui lòng thử lại sau.

📘 Giải thích:
Lỗi kỹ thuật: {str(e)}"""
        
        # Log response chi tiết
        print(f"[CHAT DEBUG] === RESPONSE ===")
        print(f"[CHAT DEBUG] response_preview: {ai_response[:200]}")
        has_english = '🇺🇸 English:' in ai_response
        has_vietnamese = '🇻🇳 Tiếng Việt:' in ai_response
        has_explanation = '📘 Giải thích:' in ai_response
        print(f"[CHAT DEBUG] Format check - English: {has_english}, Vietnamese: {has_vietnamese}, Explanation: {has_explanation}")
        
        if not (has_english and has_vietnamese and has_explanation):
            print(f"[CHAT DEBUG] ❌ WRONG FORMAT - Missing bilingual sections!")
        else:
            print(f"[CHAT DEBUG] ✅ CORRECT FORMAT - Bilingual OK")
        
        # Lưu vào lịch sử
        try:
            hm = get_history_manager()
            hm.add_chat_interaction(user_message, ai_response)
        except Exception as e:
            print(f"Lỗi lưu lịch sử: {e}")
        
        # PART 1 & 3: Log AI usage and cost
        try:
            if user_id:
                # Estimate tokens from messages
                input_tokens = len(user_message) // 4 or 1
                output_tokens = len(ai_response) // 4 or 1
                
                # Log usage
                cost_service.log_usage(
                    user_id=user_id,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    model=app_config.get_model_config().get("model", "gpt-4o-mini"),
                    message_count=1,
                    ai_provider=app_config.AI_PROVIDER
                )
                
                # Update cost analytics for admin dashboard
                cost_service.update_cost_analytics(user_id)
                get_ai_usage_service().log_usage(
                    user_id=user_id,
                    feature_type="chat",
                    token_used=input_tokens + output_tokens,
                    estimated_cost=0.0,
                    plan_type=plan_name
                )
                
                print(f"[COST LOG] Logged {input_tokens + output_tokens} tokens for user {user_id}")
        except Exception as e:
            print(f"[COST LOG] Failed to log cost: {e}")

        # Log JSON response trước khi return
        if not user_id:
            session['guest_chat_count'] = session.get('guest_chat_count', 0) + 1

        response_data = {
            "success": True,
            "reply": ai_response,
            "response": ai_response,
            "message": ai_response,  # ✅ Thêm message field
            "timestamp": get_timestamp(),
            "version": APP_VERSION
        }
        print(f"[API CHAT RESPONSE JSON] {response_data}")
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Lỗi: {str(e)}"
        }), 500

@app.route('/api/lesson', methods=['GET', 'POST'])
def get_lesson():
    """
    API endpoint để lấy bài học mới
    
    Query params (GET) hoặc body (POST):
    - level: beginner | elementary | intermediate (default: beginner)
    
    Response: JSON chứa nội dung bài học
    """
    try:
        # Lấy level từ query params hoặc body
        profile = {}
        if request.method == 'POST':
            data = request.json or {}
            level = data.get('level', 'beginner')
            roadmap_level = data.get('roadmap_level') or data.get('level_id')
            user_id = data.get('user_id') or session.get('user_id')
        else:
            level = request.args.get('level', 'beginner')
            roadmap_level = request.args.get('roadmap_level') or request.args.get('level_id')
            user_id = request.args.get('user_id', type=int) or session.get('user_id')
        if user_id:
            try:
                from models import User
                user = User.query.get(user_id)
                if user:
                    profile = user.get_profile_for_ai()
                    level = profile.get('level') or level
            except Exception as e:
                print(f"Could not load lesson profile: {e}")
        
        # Validate level
        roadmap_level_id = normalize_daily_lesson_level(roadmap_level or level)
        
        # Lấy AI service và tạo bài học
        lesson = get_daily_lesson_from_roadmap(roadmap_level_id, user_id)
        
        # Lưu vào lịch sử
        try:
            hm = get_history_manager()
            hm.add_lesson(lesson)
        except Exception as e:
            print(f"Lỗi lưu bài học: {e}")
        
        return jsonify({
            "success": True,
            "level": roadmap_level_id,
            "lesson": lesson,
            "timestamp": get_timestamp()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Lỗi tạo bài học: {str(e)}"
        }), 500

@app.route('/api/evaluate', methods=['POST'])
def evaluate_speech():
    """
    API endpoint để đánh giá câu nói của học viên
    
    Request body:
    {
        "spoken": "Câu người học nói",
        "expected": "Câu mẫu đúng"
    }
    
    Response: JSON chứa đánh giá
    """
    try:
        data = request.json
        spoken_text = data.get('spoken', '').strip()
        expected_text = data.get('expected', '').strip()
        
        if not spoken_text or not expected_text:
            return jsonify({
                "success": False,
                "error": "Vui lòng cung cấp cả câu nói và câu mẫu"
            }), 400
        
        # Lấy AI service và đánh giá
        service = get_ai_service()
        evaluation = service.evaluate_speech(spoken_text, expected_text)
        try:
            user_id = session.get('user_id') or data.get('user_id')
            get_ai_usage_service().log_usage(
                user_id=user_id,
                feature_type="speaking_correction",
                token_used=(len(spoken_text) + len(expected_text)) // 4 or 1,
                estimated_cost=0.0
            )
        except Exception as e:
            print(f"[AI USAGE LOG] Failed to log evaluate usage: {e}")
        
        # Lưu vào lịch sử
        try:
            hm = get_history_manager()
            hm.add_speaking_practice(spoken_text, expected_text, evaluation)
        except Exception as e:
            print(f"Lỗi lưu lịch sử luyện nói: {e}")
        
        return jsonify({
            "success": True,
            "evaluation": evaluation,
            "timestamp": get_timestamp()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Lỗi đánh giá: {str(e)}"
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """
    API endpoint để lấy lịch sử học tập
    
    Query params:
    - type: all | lesson | chat | speaking (default: all)
    - limit: Số bản ghi tối đa (default: 50)
    """
    try:
        history_type = request.args.get('type', 'all')
        limit = request.args.get('limit', 50, type=int)
        
        hm = get_history_manager()
        history = hm.get_recent_history(limit)
        
        # Filter theo type nếu cần
        if history_type != 'all':
            history = [h for h in history if h.get('type') == history_type]
        
        return jsonify({
            "success": True,
            "history": history,
            "count": len(history)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Lỗi lấy lịch sử: {str(e)}"
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """API endpoint để lấy thống kê học tập"""
    try:
        hm = get_history_manager()
        stats = hm.get_stats()
        
        return jsonify({
            "success": True,
            "stats": stats
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Lỗi lấy thống kê: {str(e)}"
        }), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    """API endpoint để lấy thông tin cấu hình (không bao gồm API keys)"""
    try:
        import config as app_config
        
        return jsonify({
            "success": True,
            "app_name": app_config.APP_NAME,
            "ai_provider": app_config.AI_PROVIDER,
            "available_providers": ["openai", "qwen", "gemini"],
            "model": app_config.get_model_config()["model"]
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

def get_timestamp():
    """Lấy timestamp hiện tại"""
    from datetime import datetime
    return datetime.now().isoformat()


def normalize_daily_lesson_level(level):
    value = (level or "starter").strip().lower()
    mapping = {
        "beginner": "starter",
        "pre-a1": "starter",
        "pre_a1": "starter",
        "starter": "starter",
        "elementary": "flyer",
        "a1": "flyer",
        "a2": "flyer",
        "flyer": "flyer",
        "intermediate": "ket",
        "ket": "ket",
        "pet": "pet",
        "ielts": "ielts_foundation",
        "ielts_foundation": "ielts_foundation",
        "ielts_50": "ielts_50",
        "ielts_65": "ielts_65",
        "business": "business",
        "sales": "sales",
        "cafe": "cafe",
        "factory": "factory",
    }
    return mapping.get(value, "starter")


def roadmap_lesson_to_daily_lesson(lesson):
    content = lesson.get("content") or {}
    vocab = content.get("vocabulary") or content.get("words") or []
    sentences = []
    for pattern in content.get("sentencePatterns") or content.get("examples") or []:
        sentences.append({
            "english": pattern,
            "vietnamese": "",
            "situation": lesson.get("topic") or lesson.get("title") or "Daily practice",
        })
    dialogue = []
    for line in content.get("dialogue") or []:
        dialogue.append({
            "speaker": line.get("speaker", "A") if isinstance(line, dict) else "A",
            "text": line.get("text", "") if isinstance(line, dict) else str(line),
            "translation": line.get("translation", "") if isinstance(line, dict) else "",
        })
    practice = []
    for item in content.get("speaking") or content.get("practice") or []:
        practice.append(item.get("text", "") if isinstance(item, dict) else str(item))
    quiz = content.get("quiz") or content.get("questions") or []
    exercise = None
    if quiz:
        first = quiz[0]
        exercise = {
            "type": "multiple_choice",
            "question": first.get("question", "Choose the best answer."),
            "options": first.get("options", []),
            "correct": first.get("answer") or first.get("correct") or "",
        }
    return {
        "id": lesson.get("id"),
        "source": "roadmap",
        "levelId": lesson.get("levelId"),
        "title": lesson.get("title"),
        "topic": lesson.get("topic") or lesson.get("title"),
        "vocabulary": vocab,
        "sentences": sentences,
        "dialogue": dialogue,
        "practice": [item for item in practice if item],
        "exercise": exercise,
    }


def fallback_daily_lesson_for_level(level_id):
    lessons = {
        "ket": {
            "title": "KET Daily Life Messages",
            "vocabulary": [
                {"word": "message", "ipa": "", "meaning": "tin nhan", "example": "I sent a short message."},
                {"word": "appointment", "ipa": "", "meaning": "cuoc hen", "example": "I have an appointment at ten."},
                {"word": "platform", "ipa": "", "meaning": "san ga", "example": "The train leaves from platform two."},
            ],
            "sentences": [
                {"english": "Could you call me later?", "vietnamese": "Ban goi lai cho toi sau duoc khong?", "situation": "Short message"},
                {"english": "The train leaves at nine thirty.", "vietnamese": "Tau roi luc 9:30.", "situation": "Travel"},
            ],
            "practice": ["Could you call me later?", "The train leaves at nine thirty.", "I have an appointment today."],
        },
        "pet": {
            "title": "PET Opinions and Plans",
            "vocabulary": [
                {"word": "opinion", "ipa": "", "meaning": "y kien", "example": "In my opinion, it is useful."},
                {"word": "although", "ipa": "", "meaning": "mac du", "example": "Although it rained, we went out."},
                {"word": "recommend", "ipa": "", "meaning": "de xuat", "example": "I recommend this book."},
            ],
            "sentences": [
                {"english": "In my opinion, learning English is important.", "vietnamese": "Theo toi, hoc tieng Anh rat quan trong.", "situation": "Giving opinions"},
                {"english": "I would recommend this place because it is quiet.", "vietnamese": "Toi de xuat noi nay vi no yen tinh.", "situation": "Recommendation"},
            ],
            "practice": ["In my opinion, learning English is important.", "I would recommend this place.", "Although it is hard, I can try."],
        },
        "business": {
            "title": "Business Meeting Basics",
            "vocabulary": [
                {"word": "meeting", "ipa": "", "meaning": "cuoc hop", "example": "We have a meeting at 3 p.m."},
                {"word": "deadline", "ipa": "", "meaning": "han chot", "example": "The deadline is Friday."},
                {"word": "proposal", "ipa": "", "meaning": "de xuat", "example": "Please read my proposal."},
            ],
            "sentences": [
                {"english": "Could we move the meeting to Friday?", "vietnamese": "Minh doi cuoc hop sang thu Sau duoc khong?", "situation": "Scheduling"},
                {"english": "I will send the proposal today.", "vietnamese": "Toi se gui de xuat hom nay.", "situation": "Work update"},
            ],
            "practice": ["Could we move the meeting to Friday?", "I will send the proposal today.", "The deadline is Friday."],
        },
        "sales": {
            "title": "Sales Customer Needs",
            "vocabulary": [
                {"word": "customer", "ipa": "", "meaning": "khach hang", "example": "The customer needs help."},
                {"word": "discount", "ipa": "", "meaning": "giam gia", "example": "We have a ten percent discount."},
                {"word": "recommend", "ipa": "", "meaning": "gioi thieu", "example": "I recommend this product."},
            ],
            "sentences": [
                {"english": "What are you looking for today?", "vietnamese": "Hom nay anh chi dang tim san pham gi?", "situation": "Sales opening"},
                {"english": "I recommend this one because it is easy to use.", "vietnamese": "Toi goi y cai nay vi no de dung.", "situation": "Product pitch"},
            ],
            "practice": ["What are you looking for today?", "I recommend this one.", "We have a ten percent discount."],
        },
        "cafe": {
            "title": "Cafe Staff Orders",
            "vocabulary": [
                {"word": "order", "ipa": "", "meaning": "goi mon", "example": "May I take your order?"},
                {"word": "receipt", "ipa": "", "meaning": "hoa don", "example": "Here is your receipt."},
                {"word": "recommend", "ipa": "", "meaning": "gioi thieu", "example": "I recommend iced coffee."},
            ],
            "sentences": [
                {"english": "May I take your order?", "vietnamese": "Toi co the nhan order cua anh chi khong?", "situation": "Taking orders"},
                {"english": "Would you like it hot or iced?", "vietnamese": "Anh chi muon nong hay da?", "situation": "Cafe choice"},
            ],
            "practice": ["May I take your order?", "Would you like it hot or iced?", "Here is your receipt."],
        },
        "factory": {
            "title": "Factory Safety English",
            "vocabulary": [
                {"word": "helmet", "ipa": "", "meaning": "mu bao ho", "example": "Please wear your helmet."},
                {"word": "shift", "ipa": "", "meaning": "ca lam", "example": "My shift starts at seven."},
                {"word": "machine", "ipa": "", "meaning": "may moc", "example": "The machine is not working."},
            ],
            "sentences": [
                {"english": "Please wear your safety helmet.", "vietnamese": "Vui long doi mu bao ho.", "situation": "Safety"},
                {"english": "The machine is not working.", "vietnamese": "May dang khong hoat dong.", "situation": "Reporting problems"},
            ],
            "practice": ["Please wear your safety helmet.", "My shift starts at seven.", "The machine is not working."],
        },
    }
    lesson = dict(lessons.get(level_id, lessons["ket"]))
    lesson.setdefault("dialogue", [
        {"speaker": "A", "text": lesson["practice"][0], "translation": ""},
        {"speaker": "B", "text": "Yes, I understand.", "translation": ""},
    ])
    lesson.setdefault("exercise", {
        "type": "multiple_choice",
        "question": "Choose the best sentence.",
        "options": [lesson["practice"][0], "I no understand.", "Yesterday go."],
        "correct": lesson["practice"][0],
    })
    lesson["source"] = "level_fallback"
    lesson["levelId"] = level_id
    return lesson


def get_daily_lesson_from_roadmap(level_id, user_id=None):
    service = get_roadmap_service()
    user = get_user_service().get_user(user_id) if user_id else None
    progress = service.get_progress_map(user_id) if user_id else {}
    candidates = []
    for unit in service.units_by_level.get(level_id, []):
        candidates.extend(unit.get("lessons", []))
    candidates.sort(key=lambda item: (item.get("unitId", ""), item.get("order", 0)))
    for lesson in candidates:
        content = lesson.get("content") or {}
        if service.get_lesson_status(lesson, user, progress) == "locked":
            continue
        if content.get("vocabulary") or content.get("words"):
            return roadmap_lesson_to_daily_lesson(lesson)
    for lesson in candidates:
        content = lesson.get("content") or {}
        if content.get("vocabulary") or content.get("words"):
            return roadmap_lesson_to_daily_lesson(lesson)
    return fallback_daily_lesson_for_level(level_id)


def is_admin_user(user_id):
    if not user_id:
        return False
    user = get_user_service().get_user(user_id)
    return user is not None and user.role == 'admin'


def require_admin(request):
    admin_id = session.get('user_id') or request.args.get('admin_id', type=int)
    if request.method in ['POST', 'PATCH', 'DELETE']:
        data = request.get_json(silent=True) or {}
        admin_id = session.get('user_id') or data.get('admin_id', admin_id)
    if not is_admin_user(admin_id):
        return None, jsonify({"success": False, "error": "Unauthorized"}), 403
    return admin_id, None, None


# ==========================================
# Hybrid Learning Roadmap API
# ==========================================
@app.route('/api/roadmap/levels', methods=['GET'])
def roadmap_levels():
    user_id = request.args.get('user_id', type=int) or session.get('user_id')
    service = get_roadmap_service()
    return jsonify({"success": True, "levels": service.get_levels(user_id)})


@app.route('/api/roadmap/levels/<level_id>', methods=['GET'])
def roadmap_level_detail(level_id):
    user_id = request.args.get('user_id', type=int) or session.get('user_id')
    service = get_roadmap_service()
    detail = service.get_level_detail(level_id, user_id)
    if not detail:
        return jsonify({"success": False, "error": "Level not found"}), 404
    return jsonify({"success": True, "level": detail})


@app.route('/api/roadmap/lessons/<lesson_id>', methods=['GET'])
def roadmap_lesson_detail(lesson_id):
    user_id = request.args.get('user_id', type=int) or session.get('user_id')
    service = get_roadmap_service()
    lesson = service.get_lesson(lesson_id)
    if not lesson:
        return jsonify({"success": False, "error": "Lesson not found"}), 404
    progress = service.get_progress_map(user_id) if user_id else {}
    user = get_user_service().get_user(user_id) if user_id else None
    status = service.get_lesson_status(lesson, user, progress)
    if status == "locked":
        return jsonify({"success": False, "error": "Lesson is locked", "status": status}), 403
    return jsonify({"success": True, "lesson": {**lesson, "status": status}})


@app.route('/api/roadmap/progress', methods=['POST'])
def roadmap_save_progress():
    data = request.get_json() or {}
    user_id = data.get('user_id') or session.get('user_id')
    lesson_id = data.get('lesson_id')
    if not user_id or not lesson_id:
        return jsonify({"success": False, "error": "user_id and lesson_id are required"}), 400
    row = get_roadmap_service().save_progress(
        user_id=user_id,
        lesson_id=lesson_id,
        status=data.get('status', 'completed'),
        score=data.get('score', 0),
    )
    if not row:
        return jsonify({"success": False, "error": "Lesson not found or locked"}), 403
    dashboard = get_roadmap_service().get_dashboard(user_id)
    return jsonify({"success": True, "progress": row.to_dict(), "dashboard": dashboard})


@app.route('/api/roadmap/dashboard', methods=['GET'])
def roadmap_dashboard():
    user_id = request.args.get('user_id', type=int) or session.get('user_id')
    return jsonify({"success": True, "dashboard": get_roadmap_service().get_dashboard(user_id)})


@app.route('/api/roadmap/continue', methods=['GET'])
def roadmap_continue():
    user_id = request.args.get('user_id', type=int) or session.get('user_id')
    lesson = get_roadmap_service().get_continue_lesson(user_id)
    return jsonify({"success": True, "lesson": lesson})


@app.route('/api/roadmap/selection', methods=['POST'])
def roadmap_selection():
    data = request.get_json() or {}
    user_id = data.get('user_id') or session.get('user_id')
    level_id = data.get('level_id')
    if not user_id or not level_id:
        return jsonify({"success": False, "error": "user_id and level_id are required"}), 400
    success, result = get_roadmap_service().set_selected_level(user_id, level_id)
    if success:
        user = get_user_service().get_user(user_id)
        return jsonify({"success": True, **result, "user": user.to_dict() if user else None})
    return jsonify({"success": False, **result}), 400


@app.route('/api/family/members', methods=['GET'])
def family_members():
    user_id = request.args.get('user_id', type=int) or session.get('user_id')
    success, result = get_user_service().get_family_members(user_id)
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


@app.route('/api/family/members', methods=['POST'])
def family_invite_member():
    data = request.get_json() or {}
    user_id = data.get('user_id') or session.get('user_id')
    success, result = get_user_service().invite_family_member(user_id, data)
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


@app.route('/api/family/members/<int:member_id>', methods=['DELETE'])
def family_remove_member(member_id):
    data = request.get_json(silent=True) or {}
    user_id = data.get('user_id') or request.args.get('user_id', type=int) or session.get('user_id')
    success, result = get_user_service().remove_family_member(user_id, member_id)
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


@app.route('/api/placement-test', methods=['GET'])
def placement_test():
    return jsonify({"success": True, "questions": get_roadmap_service().get_placement_questions()})


@app.route('/api/placement-test/submit', methods=['POST'])
def placement_test_submit():
    data = request.get_json() or {}
    result = get_roadmap_service().score_placement(data.get('answers') or {})
    return jsonify({"success": True, "result": result})


@app.route('/api/ai/usage/log', methods=['POST'])
def ai_usage_log():
    data = request.get_json() or {}
    user_id = data.get('userId') or data.get('user_id') or session.get('user_id')
    feature_type = data.get('featureType') or data.get('feature_type') or 'unknown'
    limit = get_roadmap_service().get_ai_limit_status(user_id, feature_type)
    if user_id and not limit["allowed"]:
        return jsonify({"success": False, "error": "AI daily limit reached", "limit": limit}), 429
    log = get_ai_usage_service().log_usage(
        user_id=user_id,
        feature_type=feature_type,
        token_used=data.get('tokenUsed') or data.get('token_used') or 0,
        estimated_cost=data.get('estimatedCost') or data.get('estimated_cost') or 0,
        plan_type=limit.get('planType')
    )
    return jsonify({"success": True, "log": log.to_dict(), "limit": limit})


@app.route('/api/roadmap/ai/explain', methods=['POST'])
def roadmap_ai_explain():
    data = request.get_json() or {}
    user_id = data.get('user_id') or session.get('user_id')
    lesson_id = data.get('lesson_id')
    feature_type = data.get('feature_type') or 'explain'
    lesson = get_roadmap_service().get_lesson(lesson_id)
    if not lesson:
        return jsonify({"success": False, "error": "Lesson not found"}), 404
    limit = get_roadmap_service().get_ai_limit_status(user_id, feature_type)
    if user_id and not limit["allowed"]:
        return jsonify({"success": False, "error": "AI daily limit reached", "limit": limit}), 429
    prompt = f"""Explain this fixed English lesson in Vietnamese for the learner.
Keep it short, practical, and personalized. Do not create a new lesson.

Lesson title: {lesson.get('title')}
Lesson type: {lesson.get('type')}
Content: {lesson.get('content')}
Feature: {feature_type}
"""
    explanation = get_ai_service().chat(prompt)
    token_used = (len(prompt) + len(explanation)) // 4 or 1
    log = get_ai_usage_service().log_usage(
        user_id=user_id,
        feature_type=feature_type,
        token_used=token_used,
        estimated_cost=0.0,
        plan_type=limit.get('planType')
    )
    return jsonify({
        "success": True,
        "explanation": explanation,
        "limit": {**limit, "used": limit["used"] + 1},
        "log": log.to_dict()
    })


@app.route('/api/roadmap/ai/speaking-correction', methods=['POST'])
def roadmap_ai_speaking_correction():
    data = request.get_json() or {}
    user_id = data.get('user_id') or session.get('user_id')
    lesson_id = data.get('lesson_id')
    expected = (data.get('expected') or '').strip()
    transcript = (data.get('transcript') or '').strip()
    if not expected or not transcript:
        return jsonify({"success": False, "error": "expected and transcript are required"}), 400

    feature_type = 'speaking_correction'
    limit = get_roadmap_service().get_ai_limit_status(user_id, feature_type)
    if user_id and not limit["allowed"]:
        return jsonify({"success": False, "error": "AI daily limit reached", "limit": limit}), 429

    prompt = f"""You are a friendly English pronunciation coach for Vietnamese learners.
Return ONLY compact valid JSON. No markdown. Keep feedback under 45 Vietnamese words.
Keys: overall_score, pronunciation_score, grammar_score, short_feedback, suggested_sentence.
Mention practical issues like missing article, unclear final sound, grammar, or naturalness.

Expected sentence: {expected}
Learner transcript: {transcript}
"""
    raw = get_ai_service().chat(prompt)
    fallback = {
        "overall_score": 70,
        "pronunciation_score": 70,
        "grammar_score": 70,
        "short_feedback": raw[:500],
        "suggested_sentence": expected,
    }
    try:
        start = raw.find('{')
        end = raw.rfind('}')
        correction = json.loads(raw[start:end + 1]) if start >= 0 and end >= start else fallback
    except Exception:
        correction = fallback

    token_used = (len(prompt) + len(raw)) // 4 or 1
    log = get_ai_usage_service().log_usage(
        user_id=user_id,
        feature_type=feature_type,
        token_used=token_used,
        estimated_cost=0.0,
        plan_type=limit.get('planType')
    )
    if user_id:
        get_roadmap_service().record_speaking_attempt(
            user_id=user_id,
            lesson_id=lesson_id,
            score=correction.get("overall_score") or 0
        )
    return jsonify({
        "success": True,
        "correction": correction,
        "limit": {**limit, "used": limit["used"] + 1},
        "log": log.to_dict()
    })


@app.route('/api/admin/roadmap/ai-usage', methods=['GET'])
def admin_roadmap_ai_usage():
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    return jsonify({"success": True, "summary": get_ai_usage_service().today_summary()})


@app.route('/api/admin/roadmap/learning-analytics', methods=['GET'])
def admin_roadmap_learning_analytics():
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    return jsonify({"success": True, "analytics": get_roadmap_service().admin_learning_analytics()})


@app.route('/api/admin/roadmap/content', methods=['GET'])
def admin_roadmap_content_index():
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    level_id = request.args.get('level_id')
    service = get_roadmap_service()
    levels = service.get_levels()
    if level_id:
        detail = service.get_level_detail(level_id)
        return jsonify({"success": True, "level": detail})
    return jsonify({"success": True, "levels": levels})


@app.route('/api/admin/roadmap/content/drafts', methods=['POST'])
def admin_roadmap_content_draft_upsert():
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    data = request.get_json() or {}
    lesson_id = data.get('lesson_id')
    lesson = get_roadmap_service().get_lesson(lesson_id)
    if not lesson:
        return jsonify({"success": False, "error": "Lesson not found"}), 404
    from models import RoadmapContentDraft
    draft = RoadmapContentDraft.query.filter_by(lesson_id=lesson_id).first()
    if not draft:
        draft = RoadmapContentDraft(
            level_id=lesson.get('levelId'),
            unit_id=lesson.get('unitId'),
            lesson_id=lesson_id,
            title=data.get('title') or lesson.get('title'),
            updated_by=admin_id,
        )
        db.session.add(draft)
    draft.title = data.get('title') or draft.title
    draft.content_json = json.dumps(data.get('content') or lesson.get('content') or {})
    draft.audio_manifest_json = json.dumps(data.get('audio_manifest') or lesson.get('audio') or {})
    draft.status = data.get('status') or draft.status
    draft.updated_by = admin_id
    db.session.commit()
    return jsonify({"success": True, "draft": draft.to_dict()})


@app.route('/api/plans', methods=['GET'])
def get_plans():
    """Get available subscription plans"""
    try:
        from services.user_service import get_user_service
        user_service = get_user_service()
        plans = [plan.to_dict() for plan in user_service.get_all_plans()]
        return jsonify({
            "success": True,
            "plans": plans,
            "payment_info": user_service.get_payment_info()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/payment/info', methods=['GET'])
def get_payment_info():
    """Return manual payment instructions shown to users before checkout."""
    user_service = get_user_service()
    return jsonify({
        "success": True,
        "payment_info": user_service.get_payment_info()
    })


@app.route('/api/payment/request', methods=['POST'])
def create_payment_request():
    """Create a new payment request for a plan"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        plan_name = data.get('plan_name')
        if not user_id or not plan_name:
            return jsonify({"success": False, "error": "user_id và plan_name là bắt buộc"}), 400
        user_service = get_user_service()
        success, result = user_service.create_payment_request(user_id, plan_name)
        if success:
            return jsonify({"success": True, **result})
        return jsonify({"success": False, **result}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/payment/request/<int:payment_id>/confirm-paid', methods=['POST'])
def confirm_payment_paid(payment_id):
    """User confirms they have transferred money for a payment request."""
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id') or session.get('user_id')
        if not user_id:
            return jsonify({"success": False, "error": "user_id is required"}), 400
        success, result = get_user_service().confirm_payment_paid(
            payment_id=payment_id,
            user_id=user_id,
            note=data.get('note') or ''
        )
        if success:
            return jsonify({"success": True, **result})
        return jsonify({"success": False, **result}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/admin/summary', methods=['GET'])
def admin_summary():
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    user_service = get_user_service()
    return jsonify({"success": True, "summary": user_service.get_admin_summary()})


@app.route('/api/admin/users', methods=['GET'])
def admin_users():
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    search = request.args.get('search')
    user_service = get_user_service()
    users = [u.to_dict() for u in user_service.search_users(search)]
    return jsonify({"success": True, "users": users})


@app.route('/api/admin/users/<int:user_id>/status', methods=['PATCH'])
def admin_update_user_status(user_id):
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    data = request.get_json() or {}
    status = data.get('status')
    user_service = get_user_service()
    success, result = user_service.update_user_status(user_id, status)
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


@app.route('/api/admin/users/<int:user_id>/extend-trial', methods=['PATCH'])
def admin_extend_trial(user_id):
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    data = request.get_json() or {}
    days = data.get('days', 7)
    user_service = get_user_service()
    success, result = user_service.extend_trial(user_id, int(days))
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


@app.route('/api/admin/users/<int:user_id>/plan', methods=['PATCH'])
def admin_change_user_plan(user_id):
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    data = request.get_json() or {}
    plan_name = data.get('plan_name')
    user_service = get_user_service()
    success, result = user_service.change_user_plan(user_id, plan_name)
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
def admin_delete_user(user_id):
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    user_service = get_user_service()
    success, result = user_service.delete_user(user_id)
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


@app.route('/api/admin/plans', methods=['GET'])
def admin_get_plans():
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    user_service = get_user_service()
    plans = [plan.to_dict() for plan in user_service.get_all_plans()]
    return jsonify({"success": True, "plans": plans})


@app.route('/api/admin/plans', methods=['POST'])
def admin_create_plan():
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    data = request.get_json() or {}
    user_service = get_user_service()
    success, result = user_service.create_plan(data)
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


@app.route('/api/admin/plans/<int:plan_id>', methods=['PATCH'])
def admin_update_plan(plan_id):
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    data = request.get_json() or {}
    user_service = get_user_service()
    success, result = user_service.update_plan(plan_id, data)
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


@app.route('/api/admin/plans/<int:plan_id>', methods=['DELETE'])
def admin_delete_plan(plan_id):
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    user_service = get_user_service()
    success, result = user_service.delete_plan(plan_id)
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


@app.route('/api/admin/payments', methods=['GET'])
def admin_payments():
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    status = request.args.get('status', 'actionable')
    user_service = get_user_service()
    payments = [p.to_dict() for p in user_service.get_payment_requests(status=status)]
    return jsonify({"success": True, "payments": payments})


@app.route('/api/admin/payments/<int:payment_id>/approve', methods=['PATCH'])
def admin_approve_payment(payment_id):
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    user_service = get_user_service()
    success, result = user_service.approve_payment(payment_id)
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


@app.route('/api/admin/payments/<int:payment_id>/reject', methods=['PATCH'])
def admin_reject_payment(payment_id):
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    user_service = get_user_service()
    success, result = user_service.reject_payment(payment_id)
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


@app.route('/api/admin/affiliate/summary', methods=['GET'])
def admin_affiliate_summary():
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    user_service = get_user_service()
    return jsonify({"success": True, "summary": user_service.get_affiliate_summary()})


@app.route('/api/admin/affiliate/profiles', methods=['GET'])
def admin_affiliate_profiles():
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    user_service = get_user_service()
    profiles = [p.to_dict() for p in user_service.get_affiliate_profiles()]
    return jsonify({"success": True, "profiles": profiles})


@app.route('/api/admin/affiliate/commissions', methods=['GET'])
def admin_affiliate_commissions():
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    status = request.args.get('status')
    user_service = get_user_service()
    commissions = [c.to_dict() for c in user_service.get_affiliate_commissions(status=status)]
    return jsonify({"success": True, "commissions": commissions})


@app.route('/api/admin/affiliate/commissions/<int:commission_id>/approve', methods=['PATCH'])
def admin_affiliate_commission_approve(commission_id):
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    user_service = get_user_service()
    success, result = user_service.update_affiliate_commission_status(commission_id, 'approved')
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


@app.route('/api/admin/affiliate/commissions/<int:commission_id>/paid', methods=['PATCH'])
def admin_affiliate_commission_paid(commission_id):
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    user_service = get_user_service()
    success, result = user_service.update_affiliate_commission_status(commission_id, 'paid')
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


@app.route('/api/admin/affiliate/commissions/<int:commission_id>/cancel', methods=['PATCH'])
def admin_affiliate_commission_cancel(commission_id):
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    user_service = get_user_service()
    success, result = user_service.update_affiliate_commission_status(commission_id, 'cancelled')
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


# ==========================================
# AGENT / AFFILIATE MANAGEMENT (BenNha style)
# ==========================================

@app.route('/api/admin/agents', methods=['GET'])
def admin_get_agents():
    """Get all agents with stats"""
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    
    status = request.args.get('status')  # pending, approved, suspended
    user_service = get_user_service()
    agents = user_service.get_all_agents(status=status)
    
    return jsonify({"success": True, "agents": agents})


@app.route('/api/admin/agents/<int:user_id>/grant', methods=['POST'])
def admin_grant_agent(user_id):
    """Grant agent status to a user"""
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    
    user_service = get_user_service()
    success, result = user_service.grant_agent_status(user_id)
    
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


@app.route('/api/admin/agents/<int:user_id>/approve', methods=['POST'])
def admin_approve_agent(user_id):
    """Approve agent status"""
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    
    user_service = get_user_service()
    success, result = user_service.approve_agent(user_id)
    
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


@app.route('/api/admin/agents/<int:user_id>/suspend', methods=['POST'])
def admin_suspend_agent(user_id):
    """Suspend agent status"""
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    
    user_service = get_user_service()
    success, result = user_service.suspend_agent(user_id)
    
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


@app.route('/api/admin/agents/<int:user_id>/revoke', methods=['DELETE'])
def admin_revoke_agent(user_id):
    """Revoke agent status"""
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    
    user_service = get_user_service()
    success, result = user_service.revoke_agent_status(user_id)
    
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


@app.route('/api/admin/agents/<int:user_id>/stats', methods=['GET'])
def admin_agent_stats(user_id):
    """Get agent statistics"""
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    
    user_service = get_user_service()
    stats = user_service.get_agent_stats(user_id)
    
    if not stats:
        return jsonify({"success": False, "error": "Agent not found"}), 404
    
    return jsonify({"success": True, "stats": stats})


@app.route('/api/admin/agents/<int:user_id>/referrals', methods=['GET'])
def admin_agent_referrals(user_id):
    """Get agent's referral history"""
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    
    user_service = get_user_service()
    agent = user_service.get_user(user_id)
    if not agent or agent.role != 'agent':
        return jsonify({"success": False, "error": "User is not an agent"}), 400
    
    referrals = user_service.get_referral_history(user_id)
    
    return jsonify({"success": True, "referrals": referrals})


@app.route('/api/admin/users/search', methods=['GET'])
def admin_search_users():
    """Search users by name, email, phone, user_code, or referral_code"""
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    
    query = request.args.get('q', '')
    user_service = get_user_service()
    users = user_service.search_users_advanced(query)
    
    return jsonify({
        "success": True,
        "users": [u.to_dict() for u in users],
        "total": len(users)
    })


@app.route('/api/admin/users/<int:user_id>/lock', methods=['PATCH'])
def admin_lock_user(user_id):
    """Lock/ban user account"""
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    
    user_service = get_user_service()
    success, result = user_service.lock_user(user_id)
    
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


@app.route('/api/admin/users/<int:user_id>/unlock', methods=['PATCH'])
def admin_unlock_user(user_id):
    """Unlock user account"""
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    
    user_service = get_user_service()
    success, result = user_service.unlock_user(user_id)
    
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


@app.route('/api/admin/users/<int:user_id>/reset-quota', methods=['PATCH'])
def admin_reset_quota(user_id):
    """Reset user quota"""
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    
    user_service = get_user_service()
    success, result = user_service.reset_user_quota(user_id)
    
    if success:
        return jsonify({"success": True, **result})
    return jsonify({"success": False, **result}), 400


# ==========================================
# PART 3: ADMIN COST & PROFITABILITY DASHBOARD
# ==========================================
@app.route('/api/admin/analytics/summary', methods=['GET'])
def admin_analytics_summary():
    """
    PART 3: Get overall cost and profitability summary for admin dashboard
    
    Returns:
    {
        "total_users": int,
        "trial_users": int,
        "paid_users": int,
        "total_revenue_month": float,
        "total_ai_cost_month": float,
        "estimated_profit_month": float,
        "users_with_loss": int,
        "high_cost_users": int,
        "avg_cost_per_user": float
    }
    """
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    
    try:
        from models import User, CostAnalytics
        from datetime import datetime
        from sqlalchemy import func
        
        now = datetime.utcnow()
        year, month = now.year, now.month
        start = datetime(year, month, 1).date()
        end = datetime(year + (1 if month == 12 else 0), 1 if month == 12 else month + 1, 1).date()
        
        # Count users by type
        total_users = User.query.filter(User.role != 'admin').count()
        trial_users = User.query.filter(User.plan_name == 'free_trial', User.role != 'admin').count()
        paid_users = total_users - trial_users
        
        # Sum costs and revenue for this month
        analytics = CostAnalytics.query.filter(
            CostAnalytics.date >= start,
            CostAnalytics.date < end
        ).all()
        
        total_ai_cost_vnd = sum(a.ai_cost_vnd for a in analytics)
        total_revenue_vnd = sum(a.revenue_vnd for a in analytics)
        estimated_profit_vnd = total_revenue_vnd - total_ai_cost_vnd
        
        # Count unprofitable users
        users_with_loss = len([a for a in analytics if not a.is_profitable])
        high_cost_users = len([a for a in analytics if a.profit_loss_vnd < -50000])  # -50k threshold
        
        # Average cost per user
        avg_cost_per_user = total_ai_cost_vnd / total_users if total_users > 0 else 0
        
        return jsonify({
            "success": True,
            "summary": {
                "total_users": total_users,
                "trial_users": trial_users,
                "paid_users": paid_users,
                "total_revenue_month_vnd": round(total_revenue_vnd, 0),
                "total_ai_cost_month_vnd": round(total_ai_cost_vnd, 0),
                "estimated_profit_month_vnd": round(estimated_profit_vnd, 0),
                "users_with_loss": users_with_loss,
                "high_cost_users": high_cost_users,
                "avg_cost_per_user_vnd": round(avg_cost_per_user, 0)
            }
        })
    except Exception as e:
        print(f"[ADMIN] Error getting analytics summary: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/admin/analytics/users', methods=['GET'])
def admin_analytics_users():
    """
    PART 3: Get cost analytics for each user (for admin dashboard profitability view)
    
    Query params:
        sort_by: "cost" | "profit" | "name" (default: "cost")
        limit: int (default: 50)
    
    Returns list of users with their cost/profit data
    """
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    
    try:
        from models import User, CostAnalytics
        from datetime import datetime
        from sqlalchemy import func
        
        sort_by = request.args.get('sort_by', 'cost')
        limit = request.args.get('limit', 50, type=int)
        
        now = datetime.utcnow()
        year, month = now.year, now.month
        start = datetime(year, month, 1).date()
        end = datetime(year + (1 if month == 12 else 0), 1 if month == 12 else month + 1, 1).date()
        
        # Get analytics grouped by user
        analytics_by_user = db.session.query(
            CostAnalytics.user_id,
            func.sum(CostAnalytics.ai_cost_vnd).label('total_cost'),
            func.sum(CostAnalytics.revenue_vnd).label('total_revenue'),
            func.count(CostAnalytics.id).label('chat_days'),
            func.sum(CostAnalytics.chat_count).label('total_chats')
        ).filter(
            CostAnalytics.date >= start,
            CostAnalytics.date < end
        ).group_by(CostAnalytics.user_id).all()
        
        users_data = []
        for user_id, cost, revenue, chat_days, total_chats in analytics_by_user:
            user = User.query.get(user_id)
            if not user:
                continue
            
            profit_loss = (revenue or 0) - (cost or 0)
            profit_percentage = ((profit_loss / (revenue or 1)) * 100) if revenue else 0
            
            # Determine status and warning level
            if profit_loss >= 0:
                status = "profit"
                warning_level = "green"
            elif profit_loss > -50000:
                status = "breakeven"
                warning_level = "yellow"
            else:
                status = "loss"
                warning_level = "red"
            
            users_data.append({
                "user_id": user_id,
                "user_name": user.name,
                "user_email": user.email,
                "plan": user.plan_name,
                "ai_cost_vnd": round(cost or 0, 0),
                "revenue_vnd": round(revenue or 0, 0),
                "profit_loss_vnd": round(profit_loss, 0),
                "profit_percentage": round(profit_percentage, 1),
                "chats_this_month": total_chats or 0,
                "days_active": chat_days or 0,
                "status": status,
                "warning_level": warning_level
            })
        
        # Sort
        if sort_by == "profit":
            users_data.sort(key=lambda x: x['profit_loss_vnd'])
        elif sort_by == "name":
            users_data.sort(key=lambda x: x['user_name'])
        else:  # sort_by == "cost"
            users_data.sort(key=lambda x: x['ai_cost_vnd'], reverse=True)
        
        return jsonify({
            "success": True,
            "users": users_data[:limit],
            "total_records": len(users_data)
        })
    except Exception as e:
        print(f"[ADMIN] Error getting user analytics: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/admin/analytics/user/<int:user_id>', methods=['GET'])
def admin_analytics_user_detail(user_id):
    """
    PART 3: Get detailed cost analytics for a specific user
    
    Returns:
    {
        "user": {...},
        "plan_info": {...},
        "today_stats": {...},
        "month_stats": {...},
        "cost_warning": {...},
        "actions": [...]  # Recommended admin actions
    }
    """
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    
    try:
        from models import User, UsageLog, CostAnalytics, Plan
        from datetime import datetime, date
        from services.cost_service import CostService
        from services.quota_service import QuotaService
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        
        cost_service = get_cost_service()
        quota_service = get_quota_service()
        
        # Get plan info
        plan = Plan.query.filter_by(name=user.plan_name).first()
        plan_info = plan.to_dict() if plan else {}
        
        # Today's stats
        today = date.today()
        today_cost_vnd = cost_service.get_daily_cost(user_id, today)
        today_chats = cost_service.get_daily_chat_count(user_id, today)
        
        # Month's stats
        now = datetime.utcnow()
        month_cost_vnd = cost_service.get_monthly_cost(user_id, now.year, now.month)
        month_chats = cost_service.get_monthly_chat_count(user_id, now.year, now.month)
        
        # Revenue
        daily_revenue = plan.price / 30 if plan else 0  # Prorate
        month_revenue = plan.price if plan else 0
        
        # Cost warnings
        cost_warning = quota_service.get_cost_warning(user_id, today_cost_vnd, user.plan_name)
        
        # Recommended actions
        actions = []
        if today_cost_vnd > (plan.price * 0.7) if plan else False:
            actions.append({
                "priority": "high",
                "action": "REDUCE_QUOTA",
                "reason": "User is using 70%+ of daily budget"
            })
        if today_chats >= (plan_info.get("chat_per_day", 10)):
            actions.append({
                "priority": "medium",
                "action": "LIMIT_CHATS",
                "reason": "User has reached daily chat limit"
            })
        if not user.is_locked and month_cost_vnd > month_revenue and month_revenue > 0:
            actions.append({
                "priority": "high",
                "action": "CONSIDER_LOCK",
                "reason": "User is generating more cost than revenue this month"
            })
        
        return jsonify({
            "success": True,
            "user": user.to_dict(),
            "plan_info": plan_info,
            "today_stats": {
                "cost_vnd": round(today_cost_vnd, 0),
                "chats": today_chats,
                "remaining_quota": max(0, plan_info.get("chat_per_day", 10) - today_chats)
            },
            "month_stats": {
                "cost_vnd": round(month_cost_vnd, 0),
                "revenue_vnd": round(month_revenue, 0),
                "profit_loss_vnd": round(month_revenue - month_cost_vnd, 0),
                "chats": month_chats
            },
            "cost_warning": cost_warning,
            "recommended_actions": actions
        })
    except Exception as e:
        print(f"[ADMIN] Error getting user detail: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/admin/analytics/user/<int:user_id>/quota', methods=['PATCH'])
def admin_update_user_quota(user_id):
    """
    PART 3: Admin can manually adjust quota limits for a specific user
    """
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    
    try:
        data = request.get_json() or {}
        user = User.query.get(user_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        
        # For now, adjust the plan - in future could have per-user quota overrides
        # This is a simplified version - you'd need a UserQuotaOverride model for full flexibility
        
        return jsonify({
            "success": True,
            "message": "Quota adjustment feature coming soon"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==========================================
# Additional Admin Analytics APIs
# ==========================================

@app.route('/api/admin/analytics/profit-loss', methods=['GET'])
def admin_profit_loss():
    """Get profit/loss analytics"""
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    
    try:
        from models import CostAnalytics, PaymentHistory
        from sqlalchemy import func
        from datetime import datetime, timedelta
        
        # Calculate for today
        today = datetime.utcnow().date()
        
        # Total revenue from payments
        total_revenue = db.session.query(func.sum(PaymentHistory.amount)).filter(
            PaymentHistory.currency == 'VND',
            PaymentHistory.status.in_(['approved', 'completed']),
            func.date(PaymentHistory.created_at) == today
        ).scalar() or 0
        
        # Total costs from AI usage
        total_costs_vnd = db.session.query(func.sum(CostAnalytics.ai_cost_vnd)).filter(
            CostAnalytics.date == today
        ).scalar() or 0
        net_profit = total_revenue - total_costs_vnd
        
        return jsonify({
            "success": True,
            "profit_loss": {
                "total_revenue": int(total_revenue),
                "total_costs": int(total_costs_vnd),
                "net_profit": int(net_profit)
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/admin/analytics/ai-usage', methods=['GET'])
def admin_ai_usage():
    """Get AI usage analytics"""
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    
    try:
        period = request.args.get('period', 'today')
        from models import UsageLog
        from sqlalchemy import func
        from datetime import datetime, timedelta
        
        if period == 'today':
            start_date = datetime.utcnow().date()
        elif period == 'week':
            start_date = datetime.utcnow().date() - timedelta(days=7)
        elif period == 'month':
            start_date = datetime.utcnow().date() - timedelta(days=30)
        else:
            start_date = datetime.utcnow().date()
        
        # Count messages and tokens
        usage = db.session.query(
            func.count(UsageLog.id).label('total_messages'),
            func.sum(UsageLog.estimated_tokens).label('total_tokens'),
            func.sum(UsageLog.estimated_cost_usd).label('estimated_cost')
        ).filter(
            func.date(UsageLog.created_at) >= start_date
        ).first()
        
        return jsonify({
            "success": True,
            "usage": {
                "total_messages": usage.total_messages or 0,
                "total_tokens": usage.total_tokens or 0,
                "estimated_cost": float(usage.estimated_cost or 0)
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/admin/analytics/costs', methods=['GET'])
def admin_costs():
    """Get cost analytics"""
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    
    try:
        from models import CostAnalytics
        from sqlalchemy import func
        from datetime import datetime, timedelta
        
        today = datetime.utcnow().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        costs = {}
        for period, start_date in [('today', today), ('week', week_ago), ('month', month_ago)]:
            cost = db.session.query(func.sum(CostAnalytics.ai_cost_vnd)).filter(
                CostAnalytics.date >= start_date
            ).scalar() or 0
            costs[period] = float(cost)
        
        # Calculate profit (simplified - just costs for now)
        profit = {k: v * -1 for k, v in costs.items()}  # Negative costs as profit
        
        return jsonify({
            "success": True,
            "costs": costs,
            "profit": profit
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/admin/affiliate/stats', methods=['GET'])
def admin_affiliate_stats():
    """Get affiliate statistics"""
    admin_id, resp, code = require_admin(request)
    if resp:
        return resp, code
    
    try:
        from models import AffiliateProfile, AffiliateCommission
        from sqlalchemy import func
        
        # Count affiliates
        total_affiliates = AffiliateProfile.query.count()
        active_affiliates = AffiliateProfile.query.filter(
            AffiliateProfile.status.in_(['active', 'approved'])
        ).count()
        
        # Sum commissions
        total_commissions = db.session.query(func.sum(AffiliateCommission.commission_amount)).filter(
            AffiliateCommission.status == 'paid'
        ).scalar() or 0
        
        pending_commissions = db.session.query(func.sum(AffiliateCommission.commission_amount)).filter(
            AffiliateCommission.status.in_(['pending', 'approved', 'unpaid'])
        ).scalar() or 0
        
        return jsonify({
            "success": True,
            "stats": {
                "total_affiliates": total_affiliates,
                "active_affiliates": active_affiliates,
                "total_commissions": int(total_commissions),
                "pending_commissions": int(pending_commissions)
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/user/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    category = data.get('category', 'general')
    content = data.get('content', '')
    rating = data.get('rating', 0)
    if not content:
        return jsonify({"success": False, "error": "Nội dung phản hồi là bắt buộc"}), 400
    user_service = get_user_service()
    feedback = user_service.create_feedback(user_id, category, content, rating)
    return jsonify({"success": True, "feedback": feedback.to_dict()})


@app.route('/api/user/reminder/check', methods=['GET'])
def check_reminder():
    user_id = request.args.get('user_id', type=int)
    user_service = get_user_service()
    user = user_service.get_user(user_id)
    if not user:
        return jsonify({"success": False, "error": "User không tồn tại"}), 404
    if not user.reminder_enabled:
        return jsonify({"success": True, "reminder": None})
    from datetime import datetime
    current_hour = datetime.utcnow().strftime('%H:%M')
    due = current_hour >= user.reminder_hour
    return jsonify({
        "success": True,
        "reminder": {
            "enabled": user.reminder_enabled,
            "hour": user.reminder_hour,
            "message": user.reminder_message,
            "due": due
        }
    })


@app.route('/admin')
def admin_page():
    # Check admin authentication
    user_id = session.get('user_id')
    user_role = session.get('user_role')
    if not user_id or user_role != 'admin':
        return jsonify({"success": False, "error": "Admin access required"}), 403
    return render_template('admin.html')

def init_services():
    """Khởi tạo các service với debug logging"""
    global ai_service, history_manager
    
    # Log config info
    import config as app_config
    print(f"[INIT] AI Provider: {app_config.AI_PROVIDER}")
    print(f"[INIT] Model: {app_config.get_model_config()['model']}")
    print(f"[INIT] API Key configured: {'✅ Yes' if app_config.GEMINI_API_KEY else '❌ No'}")
    
    # Initialize AI service
    ai_service = get_ai_service()
    print("✅ AI Service initialized")
    
    # Initialize history manager
    history_manager = get_history_manager()
    print("✅ History Manager initialized")
    
    # Initialize roleplay service
    _roleplay_service = get_roleplay_service()
    print("✅ Roleplay Service initialized")
    
    # Initialize user service
    from services.user_service import get_user_service
    get_user_service()
    print("✅ User Service initialized")
    
    # Initialize reminder service
    from services.reminder_service import get_reminder_service
    get_reminder_service()
    print("✅ Reminder Service initialized")
    
    print("✅ All services initialized!")

# ==========================================
# Roleplay API Endpoints
# ==========================================
@app.route('/api/roleplay/roles', methods=['GET'])
def get_roles():
    """Get available roles for roleplay"""
    return jsonify({
        "success": True,
        "roles": ROLES
    })

@app.route('/api/roleplay/situations', methods=['GET'])
def get_situations():
    """Get available situations for roleplay"""
    return jsonify({
        "success": True,
        "situations": SITUATIONS
    })

@app.route('/api/roleplay/start', methods=['POST'])
def start_roleplay():
    """
    Start a new roleplay session
    
    Request body:
    {
        "role": "teacher|friend|customer|colleague|interviewer|salesperson",
        "situation": "greeting|self_intro|directions|shopping|cafe|interview|customer_service|workplace",
        "user_name": "optional user name"
    }
    """
    try:
        data = request.json
        role = data.get('role', 'teacher')
        situation = data.get('situation', 'greeting')
        user_name = data.get('user_name', 'you')
        
        # Load user profile for personalization
        user_profile = None
        try:
            user_profile = load_profile()
        except Exception as e:
            print(f"Could not load user profile: {e}")
        
        # Get roleplay service
        service = get_roleplay_service()
        
        # Start roleplay with profile
        result = service.start_roleplay(role, situation, user_name, user_profile)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/roleplay/chat', methods=['POST'])
def roleplay_chat():
    """
    Send message in roleplay mode and get AI response with analysis
    
    Request body:
    {
        "message": "User's message"
    }
    
    Response:
    {
        "success": true,
        "ai_response": "AI's natural response",
        "analysis": {
            "emotions": ["confident", "friendly"],
            "naturalness": 4,
            "suggestions": ["Try using contractions"],
            "practice_sentence": "Improved version"
        }
    }
    """
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                "success": False,
                "error": "Please provide a message"
            }), 400
        
        service = get_roleplay_service()
        result = service.chat_roleplay(user_message)
        
        # Save to history
        try:
            hm = get_history_manager()
            hm.add_roleplay_interaction(
                user_message,
                result.get('ai_response', ''),
                result.get('analysis', {})
            )
        except Exception as e:
            print(f"Error saving roleplay history: {e}")
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/roleplay/feedback', methods=['GET'])
def get_roleplay_feedback():
    """Get summary feedback for the current roleplay session"""
    try:
        service = get_roleplay_service()
        feedback = service.get_feedback_summary()
        
        return jsonify({
            "success": True,
            "feedback": feedback
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/roleplay/suggest', methods=['GET'])
def get_roleplay_suggestion():
    """
    Get AI suggestion for what to say next
    Returns simple and natural versions
    """
    try:
        service = get_roleplay_service()
        
        # Get last AI message for context
        last_ai_msg = ""
        if service.conversation_history:
            for msg in reversed(service.conversation_history):
                if msg.get('role') == 'assistant':
                    last_ai_msg = msg.get('content', '')
                    break
        
        # Generate suggestions based on context
        suggestions = {
            "simple": "I don't know much about that.",
            "natural": "I'm not really familiar with that, could you tell me more?",
            "context": last_ai_msg
        }
        
        # Customize based on situation
        if service.current_situation:
            situation_key = None
            for key, val in SITUATIONS.items():
                if val['name'] == service.current_situation['name']:
                    situation_key = key
                    break
            
            if situation_key == 'greeting':
                suggestions['simple'] = "I'm from Vietnam. Nice to meet you!"
                suggestions['natural'] = "I'm actually from Vietnam. What about you, where are you from?"
            elif situation_key == 'cafe':
                suggestions['simple'] = "I want a coffee, please."
                suggestions['natural'] = "Could I get a coffee? Actually, make it a latte. Thanks!"
            elif situation_key == 'shopping':
                suggestions['simple'] = "How much is this?"
                suggestions['natural'] = "This looks nice! How much does it cost?"
            elif situation_key == 'interview':
                suggestions['simple'] = "I work as a [job]. I have [X] years experience."
                suggestions['natural'] = "Currently, I'm working as a [job]. I've been doing this for about [X] years now."
            elif situation_key == 'workplace':
                suggestions['simple'] = "I need help with this."
                suggestions['natural'] = "Hey, could you give me a hand with this task? I'm a bit stuck."
        
        return jsonify({
            "success": True,
            "suggestions": suggestions
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/roleplay/reset', methods=['POST'])
def reset_roleplay():
    """Reset the roleplay service (start fresh)"""
    try:
        global _roleplay_service
        _roleplay_service = None
        
        return jsonify({
            "success": True,
            "message": "Roleplay session reset"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ==========================================
# Situation Advisor API Endpoints
# ==========================================
@app.route('/api/situation/analyze', methods=['POST'])
def analyze_situation():
    """
    Phân tích tình huống thực tế và đưa ra câu trả lời phù hợp
    
    Request body:
    {
        "situation": "Tôi đang gặp khách hỏi giá..."
    }
    
    Response:
    {
        "success": true,
        "situation_vn": "Khách hàng hỏi về giá",
        "situation_en": "Customer asking about price",
        "solution_vn": "Hướng dẫn xử lý",
        "solution_en": "How to handle",
        "simple_en": "This costs 250k",
        "simple_vn": "Giá là 250k",
        "natural_en": "The price is...",
        "natural_vn": "Giá là...",
        "cultural_vn": "Lưu ý văn hóa",
        "cultural_en": "Cultural note",
        "practice_prompt_vn": "Bây giờ em thử...",
        "practice_prompt_en": "Now try..."
    }
    """
    try:
        data = request.json
        situation = data.get('situation', '').strip()
        
        if not situation:
            return jsonify({
                "success": False,
                "error": "Vui lòng nhập tình huống bạn đang gặp"
            }), 400
        
        # Load user profile for personalization
        user_profile = None
        try:
            user_profile = load_profile()
        except Exception as e:
            print(f"Could not load user profile: {e}")
        
        # Get advisor service
        advisor = get_situation_advisor()
        
        # Analyze situation
        result = advisor.analyze_situation(situation, user_profile)
        
        # Save to history
        try:
            hm = get_history_manager()
            hm.add_situation_record(
                situation_text=situation,
                advice=result,
                user_profile=user_profile
            )
        except Exception as e:
            print(f"Error saving situation history: {e}")
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Analyze situation error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/situation/practice', methods=['GET'])
def get_situation_practice():
    """
    Get practice sentence for the current situation
    
    Query params:
    - level: 'simple' or 'natural'
    
    Response:
    {
        "success": true,
        "en": "Practice sentence in English",
        "vn": "Practice sentence in Vietnamese"
    }
    """
    try:
        level = request.args.get('level', 'simple')
        
        advisor = get_situation_advisor()
        result = advisor.get_practice_sentence(level)
        
        return jsonify({
            "success": True,
            "en": result['en'],
            "vn": result['vn'],
            "level": level
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/situation/history', methods=['GET'])
def get_situation_history():
    """Get history of analyzed situations"""
    try:
        hm = get_history_manager()
        history = hm.get_situation_history(limit=10)
        
        return jsonify({
            "success": True,
            "history": history
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==========================================
# User Authentication & Progress APIs
# ==========================================

def persist_user_session(user):
    session.permanent = True
    session['user_id'] = user['id']
    session['user_email'] = user.get('email')
    session['user_role'] = user.get('role', 'user')


@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        data = request.get_json()
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        name = data.get('name')
        referral_code = data.get('referral_code')
        
        from services.user_service import get_user_service
        user_service = get_user_service()
        
        success, result = user_service.register_user(
            email=email, phone=phone, password=password, name=name,
            referral_code=referral_code
        )
        
        if success:
            persist_user_session(result['user'])
            return jsonify({"success": True, **result})
        else:
            return jsonify({"success": False, **result}), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        
        from services.user_service import get_user_service
        user_service = get_user_service()
        
        success, result = user_service.login_user(
            email=email, phone=phone, password=password
        )
        
        if success:
            persist_user_session(result['user'])
            return jsonify({"success": True, **result})
        else:
            return jsonify({"success": False, **result}), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/auth/me', methods=['GET'])
def get_current_user():
    """Get current logged in user from session"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"success": False, "error": "Not logged in"}), 401
        
        from services.user_service import get_user_service
        user_service = get_user_service()
        user = user_service.get_user(user_id)
        
        if not user:
            # Clear invalid session
            session.clear()
            return jsonify({"success": False, "error": "User not found"}), 401
        
        return jsonify({"success": True, "user": user.to_dict()})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout user"""
    try:
        session.clear()
        return jsonify({"success": True, "message": "Đã đăng xuất"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/auth/profile', methods=['POST'])
def setup_profile():
    """Setup user profile after registration"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        profile = data.get('profile', {})
        
        from services.user_service import get_user_service
        user_service = get_user_service()
        
        success, result = user_service.setup_profile(user_id, profile)
        
        if success:
            persist_user_session(result['user'])
            return jsonify({"success": True, **result})
        else:
            return jsonify({"success": False, **result}), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/user/profile', methods=['GET'])
def get_user_profile():
    try:
        user_id = request.args.get('user_id', type=int)
        user = get_user_service().get_user(user_id)
        if not user:
            return jsonify({"success": False, "error": "User không tồn tại"}), 404
        return jsonify({"success": True, "user": user.to_dict()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/user/profile', methods=['PATCH'])
def patch_user_profile():
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        profile_data = data.get('profile', {})
        success, result = get_user_service().setup_profile(user_id, profile_data)
        if success:
            return jsonify({"success": True, **result})
        return jsonify({"success": False, **result}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/user/usage', methods=['GET'])
def user_usage():
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({"success": False, "error": "user_id required"}), 400
        user_service = get_user_service()
        logs = [log.to_dict() for log in user_service.get_user_usage(user_id)]
        return jsonify({"success": True, "usage": logs})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/user/affiliate', methods=['GET'])
def user_affiliate():
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({"success": False, "error": "user_id required"}), 400
        user_service = get_user_service()
        affiliate_data = user_service.get_user_affiliate(user_id)
        return jsonify({"success": True, "affiliate": affiliate_data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/user/progress', methods=['GET'])
def get_progress():
    """Get user progress"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({"success": False, "error": "user_id required"}), 400
        
        from services.user_service import get_user_service
        user_service = get_user_service()
        
        user = user_service.get_user(user_id)
        progress = user_service.get_user_progress(user_id)
        common_errors = user_service.get_common_errors(user_id, limit=5)
        
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        
        return jsonify({
            "success": True,
            "user": user.to_dict(),
            "progress": progress.to_dict() if progress else None,
            "common_errors": common_errors
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==========================================
# Feedback APIs
# ==========================================

@app.route('/api/user/submit-feedback', methods=['POST'])
def submit_user_feedback():
    """Submit user feedback"""
    try:
        data = request.get_json()
        user_id = session.get('user_id')  # Get from session
        category = data.get('category')
        content = data.get('content')
        rating = data.get('rating', 0)
        
        if not category or not content:
            return jsonify({"success": False, "error": "Category and content are required"}), 400
        
        from models import Feedback
        feedback = Feedback(
            user_id=user_id,
            category=category,
            content=content,
            rating=rating
        )
        db.session.add(feedback)
        db.session.commit()
        
        return jsonify({"success": True, "feedback": feedback.to_dict(), "message": "Cảm ơn phản hồi của em!"})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/admin/feedback', methods=['GET'])
def get_admin_feedback():
    """Get feedback (admin only)"""
    try:
        # Check admin permission
        user_id = session.get('user_id')
        user_role = session.get('user_role')
        if not user_id or user_role != 'admin':
            return jsonify({"success": False, "error": "Admin access required"}), 403
        
        from models import Feedback
        feedback_list = Feedback.query.order_by(Feedback.created_at.desc()).all()
        
        return jsonify({
            "success": True, 
            "feedback": [f.to_dict() for f in feedback_list]
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/admin/feedback/<int:feedback_id>', methods=['PATCH'])
def update_admin_feedback_status(feedback_id):
    """Update feedback status (admin only)"""
    try:
        # Check admin permission
        user_id = session.get('user_id')
        user_role = session.get('user_role')
        if not user_id or user_role != 'admin':
            return jsonify({"success": False, "error": "Admin access required"}), 403
        
        data = request.get_json()
        status = data.get('status')
        
        if status not in ['new', 'reviewed', 'resolved']:
            return jsonify({"success": False, "error": "Invalid status"}), 400
        
        from models import Feedback
        feedback = Feedback.query.get(feedback_id)
        if not feedback:
            return jsonify({"success": False, "error": "Feedback not found"}), 404
        
        feedback.status = status
        feedback.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({"success": True, "feedback": feedback.to_dict()})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/user/progress', methods=['POST'])
def update_progress():
    """Update user progress after session"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        session_data = data.get('session', {})
        
        from services.user_service import get_user_service
        user_service = get_user_service()
        
        # Update streak
        user_service.update_streak(user_id)
        
        # Record session
        user_service.record_session(
            user_id=user_id,
            duration=session_data.get('duration', 5),
            sentences=session_data.get('sentences', 0),
            grammar_score=session_data.get('grammar_score'),
            natural_score=session_data.get('natural_score'),
            errors=session_data.get('errors', [])
        )
        
        # Track errors
        for error in session_data.get('errors', []):
            user_service.add_common_error(
                user_id=user_id,
                error_type=error.get('type'),
                wrong=error.get('wrong'),
                correct=error.get('correct')
            )
        
        return jsonify({"success": True, "message": "Progress updated"})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/user/activity', methods=['POST'])
def record_activity():
    """Record user activity"""
    try:
        data = request.get_json()
        
        from services.user_service import get_user_service
        user_service = get_user_service()
        
        user_service.record_activity(
            user_id=data.get('user_id'),
            activity_type=data.get('type'),
            content=data.get('content'),
            ai_response=data.get('ai_response'),
            grammar_score=data.get('grammar_score'),
            natural_score=data.get('natural_score'),
            errors=data.get('errors', [])
        )
        
        return jsonify({"success": True})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/admin/send-reminders', methods=['POST'])
def admin_send_reminders():
    data = request.get_json() or {}
    admin_id = data.get('admin_id')
    if not is_admin_user(admin_id):
        return jsonify({"success": False, "error": "Unauthorized"}), 403
    try:
        from services.reminder_service import get_reminder_service
        reminder_service = get_reminder_service()
        reminder_service.check_and_send_reminders()
        return jsonify({"success": True, "message": "Reminders checked and sent"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({
        "status": "ok",
        "app": "Ms. Smile English",
        "version": APP_VERSION
    })


if __name__ == '__main__':
    print("=" * 50)
    print("🌟 Ms. Smile English - Starting...")
    print("=" * 50)
    init_services()
    print("=" * 50)
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Server running at http://0.0.0.0:{port}")
    print("📱 Mở browser và truy cập địa chỉ trên")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=port)
