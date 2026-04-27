"""
Ms. Smile English - Main Flask Application
Backend API cho ứng dụng học tiếng Anh
"""

# VERSION - để track deploy
APP_VERSION = "bilingual-v2-2026-04-27"

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

# Import services
from services.ai_service import get_ai_service
from services.roleplay_service import get_roleplay_service, ROLES, SITUATIONS
from services.situation_advisor import get_situation_advisor
from utils.history import get_history_manager
from utils.user_profile import (
    load_profile, save_profile, update_profile, is_onboarded,
    get_profile_for_prompt, reset_profile
)

app = Flask(__name__, 
    template_folder='templates',
    static_folder='static'
)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///ms_smile.db')
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

@app.route('/api/health', methods=['GET'])
def health_check():
    """Kiểm tra trạng thái server"""
    return jsonify({
        "status": "ok",
        "message": "Ms. Smile English is running! ",
        "version": APP_VERSION
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
            from services.user_service import get_user_service
            user_service = get_user_service()
            user = user_service.get_user(user_id)
            if user:
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
            if local_profile:
                user_profile = {
                    'level': local_profile.get('level', 'beginner'),
                    'occupation': local_profile.get('job', ''),
                    'goal': local_profile.get('goal', ''),
                    'meet_foreigners': local_profile.get('meet_foreigners', False)
                }
        
        # Gọi AI với user profile để cá nhân hóa
        ai_response = service.chat(user_message, conversation_history, user_profile=user_profile)
        
        except Exception as e:
            print(f"[CHAT ERROR] Exception caught: {str(e)}")
            import traceback
            print(traceback.format_exc())
            ai_response = f"""❌ Lỗi hệ thống: {str(e)}

VN Tiếng Việt:
Hệ thống gặp lỗi khi xử lý. Vui lòng thử lại sau.

📘 Giải thích:
Lỗi: {str(e)}"""
        
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
        
        # Log JSON response trước khi return
        response_data = {
            "success": True,
            "reply": ai_response,
            "response": ai_response,
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
        if request.method == 'POST':
            data = request.json or {}
            level = data.get('level', 'beginner')
        else:
            level = request.args.get('level', 'beginner')
        
        # Validate level
        valid_levels = ['beginner', 'elementary', 'intermediate']
        if level not in valid_levels:
            level = 'beginner'
        
        # Lấy AI service và tạo bài học
        service = get_ai_service()
        lesson = service.generate_lesson(level)
        
        # Lưu vào lịch sử
        try:
            hm = get_history_manager()
            hm.add_lesson(lesson)
        except Exception as e:
            print(f"Lỗi lưu bài học: {e}")
        
        return jsonify({
            "success": True,
            "level": level,
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

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        data = request.get_json()
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        name = data.get('name')
        
        from services.user_service import get_user_service
        user_service = get_user_service()
        
        success, result = user_service.register_user(
            email=email, phone=phone, password=password, name=name
        )
        
        if success:
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
            return jsonify({"success": True, **result})
        else:
            return jsonify({"success": False, **result}), 400
            
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
            return jsonify({"success": True, **result})
        else:
            return jsonify({"success": False, **result}), 400
            
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
@app.route("/health")
def health():
    """Health check endpoint for Render"""
    return jsonify({
        "status": "ok",
        "app": "Ms. Smile English",
        "version": "1.0.0"
    })


def send_reminders():
    """Admin endpoint to trigger reminder emails"""
    try:
        from services.reminder_service import get_reminder_service
        reminder_service = get_reminder_service()
        reminder_service.check_and_send_reminders()
        
        return jsonify({"success": True, "message": "Reminders checked and sent"})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


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
