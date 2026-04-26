"""
User Profile Manager - Quản lý hồ sơ người học
Lưu trữ và truy xuất thông tin cá nhân hóa
"""

import json
import os
from typing import Dict, Any, Optional

# Default profile path
PROFILE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
PROFILE_FILE = os.path.join(PROFILE_DIR, 'user_profile.json')

DEFAULT_PROFILE = {
    "name": "bạn",
    "age": "",
    "level": "beginner",  # beginner, elementary, intermediate
    "goal": "communication",  # communication, work, travel, interview, student
    "job": "",
    "field": "",
    "daily_time": "15",  # 10, 15, 30 minutes
    "created_at": "",
    "onboarded": False
}


def ensure_profile_dir():
    """Đảm bảo thư mục data tồn tại"""
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR)


def load_profile() -> Dict[str, Any]:
    """
    Load user profile từ file
    Returns: Dictionary chứa thông tin profile
    """
    ensure_profile_dir()
    
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
                profile = json.load(f)
                # Merge với default để đảm bảo có tất cả fields
                for key, value in DEFAULT_PROFILE.items():
                    if key not in profile:
                        profile[key] = value
                return profile
        except Exception as e:
            print(f"[Profile] Lỗi đọc file: {e}, dùng default")
            return DEFAULT_PROFILE.copy()
    
    return DEFAULT_PROFILE.copy()


def save_profile(profile: Dict[str, Any]) -> bool:
    """
    Lưu user profile vào file
    
    Args:
        profile: Dictionary chứa thông tin profile
        
    Returns:
        True nếu lưu thành công, False nếu thất bại
    """
    ensure_profile_dir()
    
    try:
        with open(PROFILE_FILE, 'w', encoding='utf-8') as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[Profile] Lỗi lưu file: {e}")
        return False


def update_profile(updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Cập nhật profile với các giá trị mới
    
    Args:
        updates: Dictionary chứa các field cần cập nhật
        
    Returns:
        Profile sau khi cập nhật
    """
    profile = load_profile()
    profile.update(updates)
    save_profile(profile)
    return profile


def is_onboarded() -> bool:
    """Kiểm tra xem user đã hoàn thành onboarding chưa"""
    profile = load_profile()
    return profile.get('onboarded', False)


def get_level_vietnamese(level: str) -> str:
    """Chuyển đổi level sang tiếng Việt"""
    levels = {
        'beginner': 'mất gốc',
        'elementary': 'cơ bản',
        'intermediate': 'trung bình'
    }
    return levels.get(level, 'mất gốc')


def get_goal_vietnamese(goal: str) -> str:
    """Chuyển đổi goal sang tiếng Việt"""
    goals = {
        'communication': 'giao tiếp',
        'work': 'đi làm',
        'travel': 'du lịch',
        'interview': 'phỏng vấn',
        'student': 'học sinh'
    }
    return goals.get(goal, 'giao tiếp')


def get_profile_for_prompt() -> str:
    """
    Tạo text mô tả profile để thêm vào SYSTEM_PROMPT
    
    Returns:
        String mô tả người học
    """
    p = load_profile()
    
    name = p.get('name', 'bạn')
    level = get_level_vietnamese(p.get('level', 'beginner'))
    goal = get_goal_vietnamese(p.get('goal', 'communication'))
    job = p.get('job', '')
    field = p.get('field', '')
    daily_time = p.get('daily_time', '15')
    
    profile_text = f"""
THÔNG TIN HỌC VIÊN:
- Tên: {name}
- Trình độ: {level}
- Mục tiêu: học tiếng Anh để {goal}
- Thời gian học mỗi ngày: {daily_time} phút"""
    
    if job:
        profile_text += f"\n- Nghề nghiệp: {job}"
    if field:
        profile_text += f"\n- Lĩnh vực: {field}"
    
    return profile_text


def reset_profile():
    """Reset profile về default"""
    save_profile(DEFAULT_PROFILE.copy())


# Singleton instance
_profile_cache = None

def get_user_profile() -> Dict[str, Any]:
    """Lấy profile (có cache)"""
    global _profile_cache
    if _profile_cache is None:
        _profile_cache = load_profile()
    return _profile_cache
