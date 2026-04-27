"""
AI Service Module - Nâng cấp cho Ms. Smile English
Hỗ trợ: OpenAI (chính), Demo (không cần API), Gemini, Qwen
Tính năng: Conversation mode, ép phản xạ, feedback thông minh
"""

import json
import requests
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

# Import config
import sys
sys.path.append('..')
from config import (
    AI_PROVIDER, OPENAI_API_KEY, GEMINI_API_KEY, QWEN_API_KEY,
    get_model_config, SYSTEM_PROMPT
)

# Không import OpenAI SDK - dùng HTTP API trực tiếp để tương thích Python 3.14


class AIService:
    """Service class nâng cấp - Tập trung vào luyện phản xạ và hội thoại 2 chiều"""
    
    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or AI_PROVIDER
        self.config = get_model_config()
        self.conversation_state = {
            "current_topic": "greeting",  # greeting, introduction, daily, etc.
            "last_question": None,
            "user_responses_count": 0,
            "errors_made": []
        }
        
        # Debug log
        print(f"[INIT] AI Provider: {self.provider}")
        print(f"[INIT] Model: {self.config.get('model', 'unknown')}")
        print(f"[INIT] Time: {datetime.now().strftime('%H:%M:%S')}")
        
        if self.provider == "openai":
            self._init_openai()
        elif self.provider == "demo":
            self._init_demo()
        elif self.provider == "gemini":
            self._init_gemini()
        elif self.provider == "qwen":
            self._init_qwen()
        else:
            raise ValueError(f"Provider không hỗ trợ: {self.provider}")
    
    def _init_openai(self):
        """Khởi tạo OpenAI - dùng HTTP API trực tiếp"""
        self.api_key = OPENAI_API_KEY
        print(f"[INIT] OpenAI API Key: {'✅ Đã có' if self.api_key else '❌ Thiếu'}")
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY chưa được cấu hình!")
        
        print(f"[INIT] ✅ OpenAI will use HTTP API (Python 3.14 compatible)")
    
    def _init_demo(self):
        """Demo mode - không cần API key"""
        print(f"[INIT] 🎮 DEMO MODE - No API required")
        self.client = None
    
    def _init_gemini(self):
        """Khởi tạo Gemini HTTP API"""
        self.api_key = GEMINI_API_KEY
        print(f"[INIT] Gemini API Key: {'✅ Đã có' if self.api_key else '❌ Thiếu'}")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY chưa được cấu hình!")
    
    def _init_qwen(self):
        """Khởi tạo Qwen"""
        self.api_key = QWEN_API_KEY
        print(f"[INIT] Qwen API Key: {'✅ Đã có' if self.api_key else '❌ Thiếu'}")
        if not self.api_key:
            raise ValueError("QWEN_API_KEY chưa được cấu hình!")
    
    def chat(self, user_message: str, conversation_history: List[Dict] = None, mode: str = "conversation", user_profile: Dict = None) -> str:
        """
        Gửi message đến AI và nhận phản hồi
        
        Args:
            user_message: Tin nhắn của người dùng
            conversation_history: Lịch sử cuộc trò chuyện (optional)
            user_profile: Profile người dùng (level, occupation) để cá nhân hóa phản hồi
            
        Returns:
            Phản hồi từ AI
        """
        if conversation_history is None:
            conversation_history = []
        
        # Xây dựng system prompt với user context
        system_prompt = SYSTEM_PROMPT
        
        # BẮT BUỘC: Quy tắc format song ngữ
        bilingual_format = """

🔴 QUY TẮC BẮT BUỘC - FORMAT TRẢ LỜI SONG NGỮ:

AI LUÔN LUÔN trả lời theo format sau, KHÔNG được bỏ qua:

🇺🇸 English:
<câu tiếng Anh tự nhiên, ngắn, phù hợp hội thoại>

🇻🇳 Tiếng Việt:
<dịch nghĩa dễ hiểu>

📘 Giải thích:
- Từ vựng chính: giải thích các từ quan trọng
- Cấu trúc câu: cấu trúc ngữ pháp đã dùng
- Gợi ý câu nói: cách nói tự nhiên hơn nếu có

QUY TẮC XỬ LÝ:
- Nếu user viết tiếng Việt → chuyển ý sang tiếng Anh tự nhiên, rồi giải thích bằng tiếng Việt
- Nếu user viết tiếng Anh sai → sửa nhẹ, giải thích lỗi bằng tiếng Việt
- Nếu user viết tiếng Anh đúng → khen, giải thích từ vựng và cấu trúc
- Luôn dùng giọng cô giáo thân thiện, dễ thương

⚠️ KHÔNG được trả lời chỉ 1 ngôn ngữ. BẮT BUỘC song ngữ Anh-Việt với format trên!
"""
        system_prompt += bilingual_format
        
        # Thêm context về user profile nếu có
        if user_profile:
            level = user_profile.get('level', 'beginner')
            occupation = user_profile.get('occupation', '')
            
            context = f"""

👤 THÔNG TIN HỌC VIÊN:
- Trình độ: {level}
"""
            if occupation:
                context += f"- Nghề nghiệp: {occupation}\n"
                context += f"- Tập trung dùng từ vựng liên quan đến: {occupation}\n"
            
            system_prompt += context
        
        # Xây dựng messages
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_message})
        
        # Update conversation state
        self.conversation_state["user_responses_count"] += 1
        
        # Nếu là lần đầu hoặc quá 5 lượt, reset topic
        if self.conversation_state["user_responses_count"] > 5:
            self.conversation_state["current_topic"] = "new"
            self.conversation_state["user_responses_count"] = 0
        
        # Gọi provider tương ứng với try/except để log lỗi chi tiết
        try:
            if self.provider == "demo":
                ai_response = self._call_demo(messages, user_message)
            elif self.provider == "openai":
                ai_response = self._call_openai(messages)
            elif self.provider == "gemini":
                ai_response = self._call_gemini(messages)
            elif self.provider == "qwen":
                ai_response = self._call_qwen(messages)
            else:
                print(f"[WARN] Provider '{self.provider}' không xác định, dùng demo mode")
                ai_response = self._call_demo(messages, user_message)
            
            print(f"[CHAT SUCCESS] Response length: {len(ai_response)} chars")
            
        except Exception as e:
            print(f"[CHAT ERROR] Provider: {self.provider}, Error: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return f"""❌ Lỗi hệ thống: {str(e)}

VN Tiếng Việt:
Hệ thống gặp lỗi khi gọi AI. Vui lòng thử lại sau.

📘 Giải thích:
- Lỗi: {str(e)}
- Provider: {self.provider}
- Vui lòng kiểm tra API key hoặc thử lại sau."""
        
        # Ép format song ngữ nếu AI không tuân thủ
        has_english = 'US English:' in ai_response or '🇺🇸 English:' in ai_response
        has_vietnamese = 'VN Tiếng Việt:' in ai_response or '🇻🇳 Tiếng Việt:' in ai_response
        has_explanation = '📘 Giải thích:' in ai_response
        
        if not (has_english and has_vietnamese and has_explanation):
            print(f"[WARN] AI response không đúng format, tự bọc lại...")
            # Tự động bọc lại đúng format
            ai_response = f"""US English:
{ai_response}

VN Tiếng Việt:
[Cần dịch tiếng Việt chính xác]

📘 Giải thích:
Phản hồi chưa đúng format song ngữ."""
        
        return ai_response
    
    def _call_openai(self, messages: List[Dict]) -> str:
        """Gọi OpenAI API - Dùng HTTP REST API trực tiếp (Python 3.14 compatible)"""
        start_time = time.time()
        try:
            model = self.config.get("model", "gpt-4o-mini")
            print(f"[API] Calling OpenAI {model}...")
            
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model,
                "messages": messages,
                "temperature": self.config.get("temperature", 0.7),
                "max_tokens": self.config.get("max_tokens", 1000)
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                result = data["choices"][0]["message"]["content"]
                print(f"[API] ✅ OpenAI response in {elapsed:.2f}s ({len(result)} chars)")
                return result
            else:
                error_data = response.json() if response.text else {}
                error_msg = error_data.get("error", {}).get("message", f"HTTP {response.status_code}")
                print(f"[API] ❌ OpenAI HTTP error: {error_msg}")
                print(f"[API] Response status: {response.status_code}")
                print(f"[API] Response text: {response.text[:500]}")
                raise Exception(f"OpenAI API error: {error_msg}")
            
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"[API] ❌ OpenAI exception after {elapsed:.2f}s: {e}")
            import traceback
            print(traceback.format_exc())
            raise e
    
    def _call_demo(self, messages: List[Dict], user_message: str = "") -> str:
        """Demo mode - trả về câu trả lời mẫu theo format SONG NGỮ để test UI"""
        import random
        
        user_lower = user_message.lower()
        
        # Case 1: User chào / xin chào
        if "hello" in user_lower or "xin chào" in user_lower:
            return """🇺🇸 English:
Hello! I'm Ms. Smile. Welcome to our English class! � What would you like to learn today?

🇻🇳 Tiếng Việt:
Xin chào! Cô là Ms. Smile. Chào mừng em đến với lớp học tiếng Anh! 😊 Hôm nay em muốn học gì?

📘 Giải thích:
- Hello: Xin chào
- Welcome: Chào mừng
- Would like: muốn (lịch sự)

- Cấu trúc:
  What would you like to + verb?

- Gợi ý nói:
  What do you want to learn? (cách nói thông dụng hơn)
"""
        
        # Case 2: User nói về tên
        elif "name" in user_lower or "tên" in user_lower:
            return """🇺🇸 English:
Oh nice to meet you! 😊 My name is Ms. Smile. What's your name?

🇻🇳 Tiếng Việt:
Rất vui được gặp em! � Tên cô là Ms. Smile. Em tên gì?

📘 Giải thích:
- Nice to meet you: Rất vui được gặp (bạn/em)
- What's your name: Bạn/em tên gì?

- Cấu trúc:
  My name is + [tên]
  What's your name?

- Gợi ý nói:
  I'm Ms. Smile. (ngắn gọn hơn)
"""
        
        # Case 3: User nói "nice to meet you"
        elif "nice" in user_lower or "meet" in user_lower:
            return """�🇸 English:
Nice to meet you too! 👏 Where are you from? Tell me a little about yourself!

🇻🇳 Tiếng Việt:
Cô cũng rất vui được gặp em! 👏 Em đến từ đâu? Kể cô nghe chút về em nhé!

� Giải thích:
- Nice to meet you too: Cũng rất vui được gặp bạn
- Where are you from: Bạn đến từ đâu?
- Tell me: Kể cho tôi nghe

- Cấu trúc:
  Nice to meet you + too
  Where are you from?

- Gợi ý nói:
  I'm from Vietnam. (Tôi đến từ Việt Nam)
  I come from Ho Chi Minh City.
"""
        
        # Case 4: User viết tiếng Việt (gặp khách nước ngoài)
        elif "khách" in user_lower or "foreign" in user_lower or "mình" in user_lower:
            return """🇺🇸 English:
I often meet foreign clients at work. What industry are you in?

�🇳 Tiếng Việt:
Tôi thường gặp khách nước ngoài trong công việc. Em làm trong ngành gì?

📘 Giải thích:
- foreign clients: khách hàng nước ngoài
- often: thường xuyên
- at work: trong công việc
- industry: ngành nghề

- Cấu trúc:
  I often + verb + object

- Gợi ý nói:
  I meet foreign clients every day.
  I work with international customers.
"""
        
        # Case 5: User viết sai tiếng Anh (I very like English)
        elif "very" in user_lower and "like" in user_lower:
            return """🇺🇸 English:
I like English very much! 😊 What do you like most about it?

🇻🇳 Tiếng Việt:
Tôi thích tiếng Anh rất nhiều! 😊 Em thích điều gì nhất về tiếng Anh?

📘 Giải thích:
- Lỗi: "I very like English" ❌
- Đúng: "I like English very much" ✅
- very much: rất nhiều (đứng sau động từ)

- Cấu trúc:
  I like + noun + very much

- Gợi ý nói:
  I really like English.
  I love English!
"""
        
        # Default: trả lời ngẫu nhiên theo format song ngữ
        else:
            default_responses = [
                """🇺🇸 English:
Oh that's interesting! Tell me more about it. 😊

🇻🇳 Tiếng Việt:
Ôi thật thú vị! Kể cô nghe thêm nhé. 😊

📘 Giải thích:
- interesting: thú vị
- tell me more: kể cho tôi nghe thêm

- Cấu trúc:
  That's + adjective

- Gợi ý nói:
  Can you tell me more?
  I'd love to hear more!
""",
                """🇺🇸 English:
Good job! 👏 You're doing great. Keep practicing!

🇻🇳 Tiếng Việt:
Làm tốt lắm! 👏 Em đang làm rất tốt. Tiếp tục luyện tập nhé!

📘 Giải thích:
- Good job: Làm tốt lắm
- doing great: đang làm tốt
- keep practicing: tiếp tục luyện tập

- Cấu trúc:
  You're doing + adjective

- Gợi ý nói:
  Keep up the good work!
  You're improving!
"""
            ]
            return random.choice(default_responses)
    
    def _call_qwen(self, messages: List[Dict]) -> str:
        """Gọi Qwen API (Alibaba DashScope)"""
        try:
            url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Chuyển đổi format messages cho Qwen
            prompt = self._convert_messages_to_prompt(messages)
            
            payload = {
                "model": self.config["model"],
                "input": {
                    "messages": messages
                },
                "parameters": {
                    "temperature": self.config["temperature"],
                    "max_tokens": self.config["max_tokens"]
                }
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            return data.get("output", {}).get("text", "Không nhận được phản hồi")
        except Exception as e:
            print(f"[DEBUG] Qwen error: {e}")
            return f"❌ Lỗi kết nối AI (Qwen): {str(e)}. Vui lòng kiểm tra API key."
    
    def _call_gemini(self, messages: List[Dict]) -> str:
        """Gọi Google Gemini API - Dùng HTTP REST API trực tiếp (Python 3.14 compatible)"""
        try:
            # Tạo prompt từ messages
            prompt_parts = []
            
            # Thêm system prompt đầu tiên
            prompt_parts.append(SYSTEM_PROMPT)
            prompt_parts.append("\n---\n")
            
            # Thêm conversation history
            for msg in messages:
                role = msg.get("role", "")
                content = msg.get("content", "")
                
                if role == "system":
                    continue  # Đã thêm ở trên
                elif role == "user":
                    prompt_parts.append(f"Học viên: {content}")
                elif role == "assistant":
                    prompt_parts.append(f"Ms. Smile: {content}")
            
            # Thêm yêu cầu format phản hồi
            prompt_parts.append("\nHãy phản hồi như Ms. Smile:")
            
            full_prompt = "\n".join(prompt_parts)
            
            print(f"[DEBUG] Calling Gemini API with prompt length: {len(full_prompt)} chars")
            
            # Gọi Gemini REST API trực tiếp
            # Model names: gemini-2.0-flash, gemini-2.0-flash-001, gemini-2.5-flash
            model_name = self.config.get("model", "gemini-2.0-flash")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": full_prompt}]
                }],
                "generationConfig": {
                    "temperature": self.config.get("temperature", 0.7),
                    "maxOutputTokens": self.config.get("max_tokens", 1000),
                }
            }
            
            headers = {"Content-Type": "application/json"}
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            print(f"[DEBUG] Gemini API status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Parse response
                if "candidates" in data and len(data["candidates"]) > 0:
                    candidate = data["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        text = candidate["content"]["parts"][0].get("text", "")
                        if text:
                            print(f"[DEBUG] Gemini response received: {len(text)} chars")
                            return text
                
                return "❌ Không nhận được phản hồi hợp lệ từ AI. Em thử lại nhé!"
            else:
                error_data = response.json() if response.text else {}
                error_msg = error_data.get("error", {}).get("message", f"HTTP {response.status_code}")
                print(f"[DEBUG] Gemini API error: {error_msg}")
                
                if response.status_code == 400:
                    return "❌ API key Gemini không hợp lệ. Vui lòng kiểm tra lại trong config.py!"
                elif response.status_code == 429:
                    if "credits" in error_msg.lower() or "billing" in error_msg.lower() or "depleted" in error_msg.lower():
                        return "❌ API key đã hết credits. Vui lòng:\n1. Truy cập https://ai.studio.google.com/app/apikey\n2. Tạo API key mới (miễn phí có 1500 requests/ngày)\n3. Hoặc thêm billing vào project"
                    return "❌ Đã hết quota Gemini. Em thử lại sau nhé!"
                elif response.status_code >= 500:
                    return "❌ Server Gemini đang bận. Em thử lại sau nhé!"
                else:
                    return f"❌ Lỗi kết nối AI (Gemini): {error_msg}. Em thử lại sau nhé!"
                
        except requests.exceptions.Timeout:
            print(f"[DEBUG] Gemini API timeout")
            return "❌ Kết nối quá chậm. Em kiểm tra mạng và thử lại nhé!"
        except requests.exceptions.ConnectionError:
            print(f"[DEBUG] Gemini API connection error")
            return "❌ Lỗi kết nối mạng. Em kiểm tra internet nhé!"
        except Exception as e:
            error_msg = str(e)
            print(f"[DEBUG] Gemini API error: {error_msg}")
            return f"❌ Lỗi kết nối AI (Gemini): {error_msg}. Em thử lại sau nhé!"
    
    def _convert_messages_to_prompt(self, messages: List[Dict]) -> str:
        """Chuyển đổi danh sách messages thành prompt string"""
        prompt_parts = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        return "\n".join(prompt_parts)
    
    def generate_lesson(self, level: str = "beginner") -> Dict[str, Any]:
        """
        Tạo bài học mới với AI
        
        Args:
            level: Cấp độ (beginner, elementary, intermediate)
            
        Returns:
            Dictionary chứa nội dung bài học
        """
        prompt = f"""Tạo một bài học tiếng Anh cấp độ {level} gồm:

1. 5 từ vựng (từ đơn giản, thông dụng) - mỗi từ có:
   - Từ tiếng Anh
   - Phiên âm IPA
   - Nghĩa tiếng Việt
   - Ví dụ câu ngắn

2. 3 mẫu câu thông dụng - mỗi câu có:
   - Câu tiếng Anh
   - Dịch nghĩa tiếng Việt
   - Tình huống sử dụng

3. 1 đoạn hội thoại ngắn (2-3 lượt nói mỗi người) về chủ đề hàng ngày

4. 3 câu để luyện nói (đọc lại sau khi nghe)

5. 1 bài tập nhỏ (trắc nghiệm hoặc điền từ)

Trả về dạng JSON theo format:
{{
    "vocabulary": [{{"word": "...", "ipa": "...", "meaning": "...", "example": "..."}}],
    "sentences": [{{"english": "...", "vietnamese": "...", "situation": "..."}}],
    "dialogue": [{{"speaker": "A/B", "text": "...", "translation": "..."}}],
    "practice": ["...", "...", "..."],
    "exercise": {{"type": "...", "question": "...", "options": [...], "correct": "..."}}
}}"""

        try:
            # Sử dụng chat thông thường nhưng yêu cầu JSON output
            response = self.chat(prompt)
            
            # Parse JSON từ response
            # Tìm JSON trong response nếu có text bao quanh
            json_start = response.find('{')
            json_end = response.rfind('}')
            
            if json_start != -1 and json_end != -1:
                json_str = response[json_start:json_end + 1]
                return json.loads(json_str)
            else:
                # Fallback nếu không parse được JSON
                return self._create_fallback_lesson()
                
        except Exception as e:
            print(f"Lỗi tạo bài học: {e}")
            return self._create_fallback_lesson()
    
    def _create_fallback_lesson(self) -> Dict[str, Any]:
        """Tạo bài học mặc định khi AI không hoạt động"""
        return {
            "vocabulary": [
                {"word": "hello", "ipa": "/həˈloʊ/", "meaning": "xin chào", "example": "Hello! How are you?"},
                {"word": "thank you", "ipa": "/ˈθæŋk juː/", "meaning": "cảm ơn bạn", "example": "Thank you very much!"},
                {"word": "please", "ipa": "/pliːz/", "meaning": "làm ơn", "example": "Please sit down."},
                {"word": "sorry", "ipa": "/ˈsɔːri/", "meaning": "xin lỗi", "example": "I'm sorry I'm late."},
                {"word": "goodbye", "ipa": "/ˌɡʊdˈbaɪ/", "meaning": "tạm biệt", "example": "Goodbye! See you tomorrow!"}
            ],
            "sentences": [
                {"english": "My name is [Name].", "vietnamese": "Tên tôi là [Tên].", "situation": "Giới thiệu bản thân"},
                {"english": "Nice to meet you.", "vietnamese": "Rất vui được gặp bạn.", "situation": "Khi gặp người lần đầu"},
                {"english": "Where are you from?", "vietnamese": "Bạn đến từ đâu?", "situation": "Hỏi về quê quán"}
            ],
            "dialogue": [
                {"speaker": "A", "text": "Hello! What's your name?", "translation": "Xin chào! Bạn tên gì?"},
                {"speaker": "B", "text": "Hi! My name is Linh. And you?", "translation": "Chào! Tôi tên là Linh. Còn bạn?"},
                {"speaker": "A", "text": "I'm Nam. Nice to meet you, Linh!", "translation": "Tôi là Nam. Rất vui được gặp bạn, Linh!"},
                {"speaker": "B", "text": "Nice to meet you too!", "translation": "Tôi cũng rất vui được gặp bạn!"}
            ],
            "practice": [
                "Hello, my name is [Your Name].",
                "Nice to meet you.",
                "Thank you very much!"
            ],
            "exercise": {
                "type": "multiple_choice",
                "question": "'Hello' có nghĩa là gì?",
                "options": ["Tạm biệt", "Xin chào", "Cảm ơn", "Xin lỗi"],
                "correct": "Xin chào"
            }
        }
    
    def evaluate_speech(self, spoken_text: str, expected_text: str) -> Dict[str, Any]:
        """
        Đánh giá câu nói của học viên
        
        Args:
            spoken_text: Câu học viên nói (đã chuyển từ speech-to-text)
            expected_text: Câu mẫu đúng
            
        Returns:
            Dictionary chứa đánh giá
        """
        prompt = f"""Đánh giá câu nói của học viên:

Câu mẫu đúng: "{expected_text}"
Câu học viên nói: "{spoken_text}"

Phân tích và trả về JSON:
{{
    "correct": true/false,
    "accuracy": "high/medium/low",
    "mistakes": ["lỗi 1", "lỗi 2"],
    "correction": "Câu đúng nên nói",
    "suggestion": "Cách nói tự nhiên hơn (nếu có)",
    "feedback": "Lời nhận xét động viên bằng tiếng Việt"
}}"""

        try:
            response = self.chat(prompt)
            
            # Parse JSON
            json_start = response.find('{')
            json_end = response.rfind('}')
            
            if json_start != -1 and json_end != -1:
                json_str = response[json_start:json_end + 1]
                return json.loads(json_str)
            else:
                return self._create_fallback_evaluation(spoken_text, expected_text)
                
        except Exception as e:
            return self._create_fallback_evaluation(spoken_text, expected_text)
    
    def _create_fallback_evaluation(self, spoken: str, expected: str) -> Dict[str, Any]:
        """Tạo đánh giá mặc định"""
        is_correct = spoken.lower().strip() == expected.lower().strip()
        
        return {
            "correct": is_correct,
            "accuracy": "high" if is_correct else "medium",
            "mistakes": [] if is_correct else ["Có thể có lỗi phát âm hoặc từ"],
            "correction": expected,
            "suggestion": expected,
            "feedback": "Tuyệt vời! Em phát âm rất tốt! 🎉" if is_correct else "Gần đúng rồi! Cố gắng thêm một chút nhé! 💪"
        }


# Singleton instance
_ai_service = None

def get_ai_service(provider: Optional[str] = None) -> AIService:
    """Lấy instance của AIService (singleton pattern)"""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService(provider)
    return _ai_service
