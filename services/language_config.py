"""
Language/teacher configuration for the multi-language foundation.

Keep this module small and data-driven so adding Japanese, Korean or Chinese
later does not require changing auth/chat/profile code.
"""
from copy import deepcopy

DEFAULT_LANGUAGE = "english"

LANGUAGE_CONFIGS = {
    "english": {
        "code": "english",
        "label": "English",
        "languageName": "English",
        "teacherName": "Ms. Smile",
        "appName": "Ms. Smile English",
        "icon": "👩‍🏫",
        "themeColor": "#f72585",
        "beta": False,
        "voice": {
            "lang": "en-US",
            "nameHint": "female",
            "rate": 1.0,
        },
        "lessonCategories": [
            "Starter",
            "Flyer",
            "KET",
            "PET",
            "IELTS Foundation",
            "Business English",
        ],
        "systemPrompt": (
            "You are Ms. Smile, a warm and practical English tutor for Vietnamese learners. "
            "Help learners speak natural English, explain mistakes briefly in Vietnamese, "
            "and keep answers encouraging, clear, and useful."
        ),
        "welcomeMessage": (
            "Xin chào em! 🌟\n"
            "Cô là Ms. Smile, cô giáo tiếng Anh của em đây! 😊\n"
            "Hôm nay em muốn học gì nào? Cô có thể:\n"
            "- 💬 Chat và sửa lỗi cho em\n"
            "- 📚 Cho em bài học mới\n"
            "- 🎯 Luyện phát âm cùng em\n"
            "Em cứ nhập tiếng Việt hoặc tiếng Anh nhé! Cô sẽ giúp em! 💪"
        ),
        "responseHeader": "🇺🇸 English",
        "bilingualNote": "Bắt buộc trả lời song ngữ Anh - Việt.",
    },
    "japanese": {
        "code": "japanese",
        "label": "Japanese",
        "languageName": "Japanese",
        "teacherName": "Ms. Sakura",
        "appName": "Ms. Smile Japanese",
        "icon": "🌸",
        "themeColor": "#ec4899",
        "beta": True,
        "voice": {
            "lang": "ja-JP",
            "nameHint": "female",
            "rate": 0.95,
        },
        "lessonCategories": [
            "JLPT N5",
            "JLPT N4",
            "JLPT N3",
            "JLPT N2",
            "JLPT N1",
        ],
        "systemPrompt": (
            "Bạn là Ms. Sakura, cô giáo tiếng Nhật thân thiện cho người Việt. "
            "Dạy tiếng Nhật bằng cách đơn giản, có romaji khi cần, dịch tiếng Việt rõ ràng, "
            "và nhắc nhẹ rằng nội dung tiếng Nhật đang ở bản beta nếu thiếu bài học."
        ),
        "welcomeMessage": (
            "Xin chào em! 🌸\n"
            "Cô là Ms. Sakura, cô giáo tiếng Nhật của em. Japanese hiện đang beta.\n"
            "Em có thể hỏi câu giao tiếp, luyện phát âm hoặc học từ/câu cơ bản.\n"
            "Nếu lộ trình chưa đủ bài, cô vẫn hỗ trợ bằng chat song ngữ nhé!"
        ),
        "responseHeader": "🇯🇵 Japanese",
        "bilingualNote": "Bắt buộc trả lời song ngữ Nhật - Việt, thêm romaji khi hữu ích.",
    },
}


def normalize_language(code):
    code = (code or DEFAULT_LANGUAGE).strip().lower()
    return code if code in LANGUAGE_CONFIGS else DEFAULT_LANGUAGE


def get_language_config(code=None):
    return deepcopy(LANGUAGE_CONFIGS[normalize_language(code)])


def get_public_language_config(code=None):
    cfg = get_language_config(code)
    return {
        "code": cfg["code"],
        "label": cfg["label"],
        "languageName": cfg["languageName"],
        "teacherName": cfg["teacherName"],
        "appName": cfg["appName"],
        "icon": cfg["icon"],
        "themeColor": cfg["themeColor"],
        "beta": cfg["beta"],
        "voice": cfg["voice"],
        "lessonCategories": cfg["lessonCategories"],
        "welcomeMessage": cfg["welcomeMessage"],
        "responseHeader": cfg["responseHeader"],
    }


def get_public_language_configs():
    return [
        get_public_language_config(code)
        for code in LANGUAGE_CONFIGS
    ]


def get_user_language(user):
    return normalize_language(getattr(user, "preferred_language", None))
