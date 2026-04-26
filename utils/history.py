"""
History Management Module
Quản lý lịch sử học tập của người dùng
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any
import config


class HistoryManager:
    """Quản lý lịch sử học tập"""
    
    def __init__(self):
        self.data_dir = config.DATA_DIR
        self.history_file = os.path.join(self.data_dir, "learning_history.json")
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Đảm bảo thư mục data tồn tại"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _load_history(self) -> List[Dict]:
        """Đọc lịch sử từ file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return []
        return []
    
    def _save_history(self, history: List[Dict]):
        """Lưu lịch sử vào file"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    def add_lesson(self, lesson_data: Dict[str, Any]):
        """
        Thêm bài học mới vào lịch sử
        
        Args:
            lesson_data: Dictionary chứa thông tin bài học
        """
        history = self._load_history()
        
        lesson_record = {
            "date": datetime.now().isoformat(),
            "type": "lesson",
            "vocabulary_learned": len(lesson_data.get("vocabulary", [])),
            "sentences_practiced": len(lesson_data.get("practice", [])),
            "content": lesson_data
        }
        
        history.append(lesson_record)
        self._save_history(history)
    
    def add_chat_interaction(self, user_message: str, ai_response: str, 
                            mistakes: List[str] = None):
        """
        Thêm tương tác chat vào lịch sử
        
        Args:
            user_message: Tin nhắn của người dùng
            ai_response: Phản hồi của AI
            mistakes: Danh sách lỗi phát hiện được (nếu có)
        """
        history = self._load_history()
        
        chat_record = {
            "date": datetime.now().isoformat(),
            "type": "chat",
            "user_message": user_message,
            "ai_response": ai_response,
            "mistakes": mistakes or []
        }
        
        history.append(chat_record)
        self._save_history(history)
    
    def add_speaking_practice(self, spoken_text: str, expected_text: str,
                              evaluation: Dict[str, Any]):
        """
        Thêm bài tập nói vào lịch sử
        
        Args:
            spoken_text: Câu người học nói
            expected_text: Câu mẫu
            evaluation: Kết quả đánh giá
        """
        history = self._load_history()
        
        practice_record = {
            "date": datetime.now().isoformat(),
            "type": "speaking",
            "spoken_text": spoken_text,
            "expected_text": expected_text,
            "correct": evaluation.get("correct", False),
            "accuracy": evaluation.get("accuracy", "low"),
            "mistakes": evaluation.get("mistakes", [])
        }
        
        history.append(practice_record)
        self._save_history(history)
    
    def add_roleplay_interaction(self, user_message: str, ai_response: str,
                                 analysis: Dict[str, Any]):
        """
        Thêm tương tác roleplay vào lịch sử
        
        Args:
            user_message: Tin nhắn của người dùng
            ai_response: Phản hồi của AI trong vai roleplay
            analysis: Phân tích câu nói (emotions, naturalness, etc.)
        """
        history = self._load_history()
        
        roleplay_record = {
            "date": datetime.now().isoformat(),
            "type": "roleplay",
            "user_message": user_message,
            "ai_response": ai_response,
            "emotions": analysis.get("emotions", []),
            "naturalness": analysis.get("naturalness", 3),
            "suggestions": analysis.get("suggestions", []),
            "practice_sentence": analysis.get("practice_sentence", ""),
            "word_count": analysis.get("word_count", 0)
        }
        
        history.append(roleplay_record)
        self._save_history(history)
    
    def get_roleplay_stats(self) -> Dict[str, Any]:
        """
        Lấy thống kê roleplay
        
        Returns:
            Dictionary chứa thống kê roleplay
        """
        history = self._load_history()
        roleplay_records = [h for h in history if h.get("type") == "roleplay"]
        
        if not roleplay_records:
            return {
                "total_sessions": 0,
                "total_turns": 0,
                "average_naturalness": 0,
                "common_emotions": [],
                "common_suggestions": []
            }
        
        # Calculate stats
        total_turns = len(roleplay_records)
        avg_naturalness = sum(h.get("naturalness", 3) for h in roleplay_records) / total_turns
        
        # Collect emotions
        all_emotions = []
        for h in roleplay_records:
            all_emotions.extend(h.get("emotions", []))
        
        from collections import Counter
        emotion_counts = Counter(all_emotions)
        common_emotions = emotion_counts.most_common(5)
        
        # Collect suggestions
        all_suggestions = []
        for h in roleplay_records:
            all_suggestions.extend(h.get("suggestions", []))
        suggestion_counts = Counter(all_suggestions)
        common_suggestions = suggestion_counts.most_common(5)
        
        return {
            "total_sessions": total_turns,  # Each turn counts as a session entry
            "total_turns": total_turns,
            "average_naturalness": round(avg_naturalness, 1),
            "common_emotions": common_emotions,
            "common_suggestions": common_suggestions
        }
    
    def add_situation_record(self, situation_text: str, advice: Dict[str, Any],
                            user_profile: Dict = None):
        """
        Thêm tình huống thực tế đã phân tích vào lịch sử
        
        Args:
            situation_text: Tình huống user nhập
            advice: Kết quả phân tích và câu trả lời gợi ý
            user_profile: Thông tin user
        """
        history = self._load_history()
        
        record = {
            "date": datetime.now().isoformat(),
            "type": "situation",
            "situation_text": situation_text[:200],  # Limit length
            "situation_vn": advice.get("situation_vn", ""),
            "situation_en": advice.get("situation_en", ""),
            "simple_en": advice.get("simple_en", ""),
            "natural_en": advice.get("natural_en", ""),
            "user_level": user_profile.get("level", "beginner") if user_profile else "beginner",
            "user_job": user_profile.get("job", "") if user_profile else "",
            "field": self._detect_situation_field(situation_text)
        }
        
        history.append(record)
        self._save_history(history)
    
    def _detect_situation_field(self, text: str) -> str:
        """Phát hiện lĩnh vực của tình huống"""
        text_lower = text.lower()
        
        if any(w in text_lower for w in ['giá', 'price', 'bán', 'sale', 'customer', 'khách']):
            return 'sales'
        elif any(w in text_lower for w in ['cafe', 'coffee', 'gọi món', 'order', 'ăn', 'food']):
            return 'service'
        elif any(w in text_lower for w in ['máy', 'machine', 'kỹ thuật', 'technical', 'repair', 'sửa']):
            return 'technical'
        elif any(w in text_lower for w in ['email', 'meeting', 'báo cáo', 'report', 'văn phòng', 'office']):
            return 'office'
        elif any(w in text_lower for w in ['đường', 'direction', 'location', 'where', 'ở đâu']):
            return 'navigation'
        else:
            return 'general'
    
    def get_situation_history(self, limit: int = 10) -> List[Dict]:
        """
        Lấy lịch sử tình huống đã phân tích
        
        Args:
            limit: Số bản ghi tối đa
            
        Returns:
            Danh sách tình huống gần đây
        """
        history = self._load_history()
        situations = [h for h in history if h.get("type") == "situation"]
        return situations[-limit:][::-1]  # Mới nhất lên đầu
    
    def get_situation_stats(self) -> Dict[str, Any]:
        """Thống kê các tình huống đã phân tích"""
        history = self._load_history()
        situations = [h for h in history if h.get("type") == "situation"]
        
        if not situations:
            return {
                "total_situations": 0,
                "common_fields": [],
                "average_per_day": 0
            }
        
        # Count by field
        field_counts = {}
        for s in situations:
            field = s.get("field", "general")
            field_counts[field] = field_counts.get(field, 0) + 1
        
        common_fields = sorted(field_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_situations": len(situations),
            "common_fields": common_fields,
            "average_per_day": round(len(situations) / max(1, self._get_learning_days(history)), 1)
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Lấy thống kê học tập
        
        Returns:
            Dictionary chứa thống kê
        """
        history = self._load_history()
        
        total_lessons = sum(1 for h in history if h.get("type") == "lesson")
        total_chats = sum(1 for h in history if h.get("type") == "chat")
        total_speaking = sum(1 for h in history if h.get("type") == "speaking")
        
        # Tính số câu đã luyện
        total_sentences = sum(
            h.get("sentences_practiced", 0) 
            for h in history if h.get("type") == "lesson"
        )
        total_sentences += total_speaking
        
        # Thu thập lỗi thường gặp
        all_mistakes = []
        for h in history:
            if "mistakes" in h and h["mistakes"]:
                all_mistakes.extend(h["mistakes"])
        
        # Đếm tần suất lỗi
        mistake_counts = {}
        for m in all_mistakes:
            mistake_counts[m] = mistake_counts.get(m, 0) + 1
        
        # Sắp xếp lỗi theo tần suất
        common_mistakes = sorted(
            mistake_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]  # Top 5 lỗi
        
        return {
            "total_lessons": total_lessons,
            "total_chat_interactions": total_chats,
            "total_speaking_practices": total_speaking,
            "total_sentences_practiced": total_sentences,
            "common_mistakes": common_mistakes,
            "learning_days": self._get_learning_days(history),
            "last_study_date": self._get_last_study_date(history)
        }
    
    def _get_learning_days(self, history: List[Dict]) -> int:
        """Đếm số ngày đã học (unique dates)"""
        dates = set()
        for h in history:
            date_str = h.get("date", "")
            if date_str:
                try:
                    date = datetime.fromisoformat(date_str).date()
                    dates.add(date)
                except:
                    pass
        return len(dates)
    
    def _get_last_study_date(self, history: List[Dict]) -> str:
        """Lấy ngày học gần nhất"""
        if not history:
            return None
        
        try:
            dates = [
                datetime.fromisoformat(h.get("date", ""))
                for h in history if h.get("date")
            ]
            if dates:
                last_date = max(dates)
                return last_date.strftime("%d/%m/%Y")
        except:
            pass
        
        return None
    
    def get_recent_history(self, limit: int = 10) -> List[Dict]:
        """
        Lấy lịch sử gần đây
        
        Args:
            limit: Số bản ghi tối đa
            
        Returns:
            Danh sách bản ghi gần đây nhất
        """
        history = self._load_history()
        return history[-limit:][::-1]  # Đảo ngược để mới nhất lên đầu
    
    def clear_history(self):
        """Xóa toàn bộ lịch sử"""
        if os.path.exists(self.history_file):
            os.remove(self.history_file)


# Singleton instance
_history_manager = None

def get_history_manager() -> HistoryManager:
    """Lấy instance của HistoryManager"""
    global _history_manager
    if _history_manager is None:
        _history_manager = HistoryManager()
    return _history_manager
