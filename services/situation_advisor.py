"""
Situation Advisor Service - Cố vấn tình huống thực tế
Phân tích tình huống giao tiếp và đưa ra câu tiếng Anh phù hợp
"""

import json
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime

# Import config
import sys
sys.path.append('..')
from config import AI_PROVIDER, OPENAI_API_KEY, GEMINI_API_KEY, QWEN_API_KEY


class SituationAdvisor:
    """
    Service để phân tích tình huống thực tế và đưa ra câu tiếng Anh phù hợp
    """
    
    def __init__(self, provider: str = None):
        self.provider = provider or AI_PROVIDER
        self.api_key = self._get_api_key()
        self.current_situation = None
        self.user_profile = None
        
    def _get_api_key(self):
        if self.provider == "openai":
            return OPENAI_API_KEY
        elif self.provider == "gemini":
            return GEMINI_API_KEY
        elif self.provider == "qwen":
            return QWEN_API_KEY
        return None
    
    def analyze_situation(self, situation_text: str, user_profile: Dict = None) -> Dict[str, Any]:
        """
        Phân tích tình huống và đưa ra câu trả lời phù hợp
        
        Args:
            situation_text: Mô tả tình huống user đang gặp (tiếng Việt hoặc tiếng Anh)
            user_profile: Thông tin user để cá nhân hóa
            
        Returns:
            Dict chứa phân tích và câu trả lời theo format bắt buộc
        """
        self.current_situation = situation_text
        self.user_profile = user_profile or {}
        
        # Detect language of input
        is_vietnamese = self._detect_vietnamese(situation_text)
        
        # Build system prompt
        system_prompt = self._build_advisor_prompt()
        
        # Call AI
        if self.provider == "openai":
            result = self._call_openai_advisor(situation_text, system_prompt)
        else:
            result = self._call_demo_advisor(situation_text)
        
        # Add metadata
        result['timestamp'] = datetime.now().isoformat()
        result['situation_original'] = situation_text
        result['user_level'] = self.user_profile.get('level', 'beginner')
        
        return result
    
    def _detect_vietnamese(self, text: str) -> bool:
        """Detect if text is in Vietnamese"""
        vietnamese_chars = ['à', 'á', 'ạ', 'ả', 'ã', 'â', 'ầ', 'ấ', 'ậ', 'ẩ', 'ẫ', 'ă', 'ằ', 'ắ', 'ặ', 'ẳ', 'ẵ',
                          'è', 'é', 'ẹ', 'ẻ', 'ẽ', 'ê', 'ề', 'ế', 'ệ', 'ể', 'ễ',
                          'ì', 'í', 'ị', 'ỉ', 'ĩ',
                          'ò', 'ó', 'ọ', 'ỏ', 'õ', 'ô', 'ồ', 'ố', 'ộ', 'ổ', 'ỗ', 'ơ', 'ờ', 'ớ', 'ợ', 'ở', 'ỡ',
                          'ù', 'ú', 'ụ', 'ủ', 'ũ', 'ư', 'ừ', 'ứ', 'ự', 'ử', 'ữ',
                          'ỳ', 'ý', 'ỵ', 'ỷ', 'ỹ',
                          'đ', 'Đ']
        return any(char in text.lower() for char in vietnamese_chars)
    
    def _build_advisor_prompt(self) -> str:
        """Build system prompt cho situation advisor"""
        
        level = self.user_profile.get('level', 'beginner')
        job = self.user_profile.get('job', '')
        goal = self.user_profile.get('goal', 'communication')
        
        # Adjust complexity
        if level == 'beginner':
            complexity = "SIMPLE sentences (5-8 words), basic vocabulary, one idea per sentence"
        elif level == 'elementary':
            complexity = "Clear sentences (8-12 words), common vocabulary"
        else:
            complexity = "Natural sentences, varied vocabulary, polite expressions"
        
        # Job context
        job_context = ""
        if job:
            job_context = f"\nUser works in: {job}. Tailor advice to their field when relevant."
        
        return f"""You are an English communication advisor helping Vietnamese people handle real-life situations.

USER PROFILE:
Level: {level}
Goal: {goal}{job_context}

CRITICAL INSTRUCTIONS:
1. Response MUST be in this exact format with BOTH Vietnamese and English:

🧩 TÌNH HUỐNG:
VI: [Phân tích tình huống bằng tiếng Việt - 1 câu ngắn]
EN: [Tình huống tiếng Anh - 1 câu ngắn]

✅ CÁCH XỬ LÝ:
VI: [Hướng dẫn cách xử lý bằng tiếng Việt - 1-2 câu]
EN: [Cách xử lý tiếng Anh]

💬 CÂU ĐƠN GIẢN ({complexity}):
EN: "[Câu tiếng Anh đơn giản, dễ nhớ, dễ nói]"
VI: "[Dịch tiếng Việt]"

✨ CÂU TỰ NHIÊN HƠN:
EN: "[Câu tiếng Anh tự nhiên, lịch sự, native speaker hay dùng]"
VI: "[Dịch tiếng Việt]"

⚠️ LƯU Ý VĂN HÓA:
VI: [Lưu ý về văn hóa hoặc cách giao tiếp phù hợp - 1 câu]
EN: [Cultural note in English]

🔁 EM LUYỆN LẠI:
VI: Bây giờ em thử trả lời bằng tiếng Anh nhé: [Đặt câu hỏi ngắn để user luyện]
EN: Now try to respond in English: [Ask a simple follow-up question]

2. Rules:
- Keep ALL sections (🧩 ✅ 💬 ✨ ⚠️ 🔁)
- VI: and EN: must be on separate lines
- Câu tiếng Anh phải ngắn, thực tế, dùng được ngay
- Không giảng dài, không lý thuyết
- Ưu tiên câu đơn giản cho người mới học
- Luôn có phần "Em luyện lại" để user thực hành

3. Examples of good responses:
💬 CÂU ĐƠN GIẢN:
EN: "This product costs 250,000 VND."
VI: "Sản phẩm này giá 250.000 đồng."

✨ CÂU TỰ NHIÊN HƠN:
EN: "The price is 250,000 VND. Would you like to see more details?"
VI: "Giá là 250.000 đồng. Anh/chị có muốn xem thêm chi tiết không?"

⚠️ LƯU Ý VĂN HÓA:
VI: Luôn mỉm cười và giữ giọng điệu thân thiện khi nói giá.
EN: Always smile and keep a friendly tone when mentioning prices.

🔁 EM LUYỆN LẠI:
VI: Bây giờ em thử trả lời bằng tiếng Anh nhé: "How much does this cost?"
EN: Now try to respond in English: "How much does this cost?"

Remember: Be practical, be concise, be encouraging!"""
    
    def _call_openai_advisor(self, situation: str, system_prompt: str) -> Dict[str, Any]:
        """Call OpenAI API for situation analysis"""
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Situation: {situation}\n\nPlease analyze and give me advice in the exact format specified."}
            ]
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 800
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                content = response.json()["choices"][0]["message"]["content"]
                return self._parse_advisor_response(content)
            else:
                return self._fallback_response(situation)
                
        except Exception as e:
            print(f"[SituationAdvisor] OpenAI error: {e}")
            return self._fallback_response(situation)
    
    def _parse_advisor_response(self, content: str) -> Dict[str, Any]:
        """Parse AI response into structured format"""
        result = {
            'success': True,
            'situation_vn': '',
            'situation_en': '',
            'solution_vn': '',
            'solution_en': '',
            'simple_en': '',
            'simple_vn': '',
            'natural_en': '',
            'natural_vn': '',
            'cultural_vn': '',
            'cultural_en': '',
            'practice_prompt_vn': '',
            'practice_prompt_en': '',
            'raw_response': content
        }
        
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect sections
            if '🧩' in line or 'TÌNH HUỐNG' in line.upper():
                current_section = 'situation'
            elif '✅' in line or 'CÁCH XỬ LÝ' in line.upper():
                current_section = 'solution'
            elif '💬' in line or 'ĐƠN GIẢN' in line.upper():
                current_section = 'simple'
            elif '✨' in line or 'TỰ NHIÊN' in line.upper():
                current_section = 'natural'
            elif '⚠️' in line or 'LƯU Ý' in line.upper():
                current_section = 'cultural'
            elif '🔁' in line or 'LUYỆN LẠI' in line.upper():
                current_section = 'practice'
            
            # Parse content
            if line.startswith('VI:'):
                text = line[3:].strip()
                if current_section == 'situation':
                    result['situation_vn'] = text
                elif current_section == 'solution':
                    result['solution_vn'] = text
                elif current_section == 'simple':
                    result['simple_vn'] = text
                elif current_section == 'natural':
                    result['natural_vn'] = text
                elif current_section == 'cultural':
                    result['cultural_vn'] = text
                elif current_section == 'practice':
                    result['practice_prompt_vn'] = text
            
            elif line.startswith('EN:'):
                text = line[3:].strip()
                if current_section == 'situation':
                    result['situation_en'] = text
                elif current_section == 'solution':
                    result['solution_en'] = text
                elif current_section == 'simple':
                    result['simple_en'] = text
                elif current_section == 'natural':
                    result['natural_en'] = text
                elif current_section == 'cultural':
                    result['cultural_en'] = text
                elif current_section == 'practice':
                    result['practice_prompt_en'] = text
            
            # Also check for quoted sentences
            elif '"' in line and current_section == 'simple' and not result['simple_en']:
                # Extract text between quotes
                import re
                match = re.search(r'"([^"]+)"', line)
                if match and not line.startswith('VI:') and not line.startswith('EN:'):
                    result['simple_en'] = match.group(1)
            
            elif '"' in line and current_section == 'natural' and not result['natural_en']:
                import re
                match = re.search(r'"([^"]+)"', line)
                if match and not line.startswith('VI:') and not line.startswith('EN:'):
                    result['natural_en'] = match.group(1)
        
        return result
    
    def _fallback_response(self, situation: str) -> Dict[str, Any]:
        """Fallback response when AI fails"""
        return {
            'success': True,
            'situation_vn': 'Tình huống giao tiếp tiếng Anh',
            'situation_en': 'English communication situation',
            'solution_vn': 'Hãy bình tĩnh và nói rõ ràng.',
            'solution_en': 'Stay calm and speak clearly.',
            'simple_en': "I understand. Let me help you.",
            'simple_vn': "Tôi hiểu. Để tôi giúp bạn.",
            'natural_en': "I see what you mean. Let me see how I can assist you with that.",
            'natural_vn': "Tôi hiểu ý bạn. Để tôi xem tôi có thể giúp gì.",
            'cultural_vn': 'Luôn lịch sự và thân thiện.',
            'cultural_en': 'Always be polite and friendly.',
            'practice_prompt_vn': 'Bây giờ em thử nói: "Can you help me?"',
            'practice_prompt_en': 'Now try saying: "Can you help me?"',
            'raw_response': 'Fallback response',
            'is_fallback': True
        }
    
    def _call_demo_advisor(self, situation: str) -> Dict[str, Any]:
        """Demo response when no API available"""
        # Detect situation type
        situation_lower = situation.lower()
        
        if 'giá' in situation_lower or 'price' in situation_lower:
            return {
                'success': True,
                'situation_vn': 'Khách hàng hỏi về giá sản phẩm',
                'situation_en': 'Customer asking about product price',
                'solution_vn': 'Nói rõ giá và hỏi khách có cần xem thêm không.',
                'solution_en': 'State the price clearly and ask if they need to see more.',
                'simple_en': "This product costs 250,000 VND.",
                'simple_vn': "Sản phẩm này giá 250.000 đồng.",
                'natural_en': "The price is 250,000 VND. Would you like to see more details?",
                'natural_vn': "Giá là 250.000 đồng. Anh/chị có muốn xem thêm chi tiết không?",
                'cultural_vn': 'Luôn mỉm cười và giọng điệu thân thiện khi nói giá.',
                'cultural_en': 'Always smile and use a friendly tone when mentioning prices.',
                'practice_prompt_vn': 'Bây giờ em thử trả lời bằng tiếng Anh nhé: "How much is this product?"',
                'practice_prompt_en': 'Now try to respond in English: "How much is this product?"',
                'raw_response': 'Demo price response'
            }
        
        elif 'xin lỗi' in situation_lower or 'sorry' in situation_lower or 'lỗi' in situation_lower:
            return {
                'success': True,
                'situation_vn': 'Cần xin lỗi khách hàng',
                'situation_en': 'Need to apologize to a customer',
                'solution_vn': 'Xin lỗi chân thành và đề xuất cách khắc phục.',
                'solution_en': 'Apologize sincerely and suggest a solution.',
                'simple_en': "I'm sorry. Let me fix this for you.",
                'simple_vn': "Tôi xin lỗi. Để tôi sửa lại cho bạn.",
                'natural_en': "I sincerely apologize for this inconvenience. Let me make it right for you right away.",
                'natural_vn': "Tôi xin lỗi chân thành vì sự bất tiện này. Để tôi sửa lại ngay cho bạn.",
                'cultural_vn': 'Khi xin lỗi, hãy cúi đầu nhẹ và giữ giọng thành khẩn.',
                'cultural_en': 'When apologizing, bow slightly and maintain a sincere tone.',
                'practice_prompt_vn': 'Bây giờ em thử nói: "I\'m sorry for the mistake."',
                'practice_prompt_en': 'Now try saying: "I\'m sorry for the mistake."',
                'raw_response': 'Demo apology response'
            }
        
        elif 'gọi' in situation_lower or 'order' in situation_lower or 'cafe' in situation_lower or 'coffee' in situation_lower:
            return {
                'success': True,
                'situation_vn': 'Gọi món tại quán cà phê',
                'situation_en': 'Ordering at a coffee shop',
                'solution_vn': 'Nói rõ món muốn gọi và hỏi về giá nếu cần.',
                'solution_en': 'Clearly state your order and ask about price if needed.',
                'simple_en': "I want a coffee, please.",
                'simple_vn': "Tôi muốn một ly cà phê.",
                'natural_en': "Could I get a latte, please? And how much is that?",
                'natural_vn': "Cho tôi một ly latte nhé? Và giá là bao nhiêu ạ?",
                'cultural_vn': 'Luôn nói "please" và "thank you" khi gọi món.',
                'cultural_en': 'Always say "please" and "thank you" when ordering.',
                'practice_prompt_vn': 'Bây giờ em thử gọi món: "Can I have a coffee?"',
                'practice_prompt_en': 'Now try ordering: "Can I have a coffee?"',
                'raw_response': 'Demo ordering response'
            }
        
        elif 'hỏi đường' in situation_lower or 'direction' in situation_lower or 'đường' in situation_lower:
            return {
                'success': True,
                'situation_vn': 'Hỏi đường người nước ngoài',
                'situation_en': 'Asking for directions from a foreigner',
                'solution_vn': 'Hỏi lịch sự và xác nhận lại thông tin.',
                'solution_en': 'Ask politely and confirm the information.',
                'simple_en': "Excuse me, where is the station?",
                'simple_vn': "Xin lỗi, nhà ga ở đâu ạ?",
                'natural_en': "Excuse me, could you tell me how to get to the train station?",
                'natural_vn': "Xin lỗi, bạn có thể chỉ cho tôi đường đến nhà ga không?",
                'cultural_vn': 'Luôn nói "Excuse me" trước khi hỏi người lạ.',
                'cultural_en': 'Always say "Excuse me" before asking strangers.',
                'practice_prompt_vn': 'Bây giờ em thử hỏi: "Where is the bathroom?"',
                'practice_prompt_en': 'Now try asking: "Where is the bathroom?"',
                'raw_response': 'Demo directions response'
            }
        
        else:
            # Generic response
            return {
                'success': True,
                'situation_vn': 'Tình huống giao tiếp tiếng Anh',
                'situation_en': 'English communication situation',
                'solution_vn': 'Hãy bình tĩnh, nói rõ ràng và lịch sự.',
                'solution_en': 'Stay calm, speak clearly and politely.',
                'simple_en': "I understand. Let me help you.",
                'simple_vn': "Tôi hiểu. Để tôi giúp bạn.",
                'natural_en': "I see what you mean. Let me see how I can assist you with that.",
                'natural_vn': "Tôi hiểu ý bạn. Để tôi xem tôi có thể giúp gì.",
                'cultural_vn': 'Luôn lịch sự và thân thiện khi giao tiếp.',
                'cultural_en': 'Always be polite and friendly when communicating.',
                'practice_prompt_vn': 'Bây giờ em thử nói: "Can you help me, please?"',
                'practice_prompt_en': 'Now try saying: "Can you help me, please?"',
                'raw_response': 'Demo generic response'
            }
    
    def get_practice_sentence(self, level: str = 'simple') -> Dict[str, str]:
        """Get practice sentence for user to try"""
        if self.current_situation:
            result = self._call_demo_advisor(self.current_situation)
            
            if level == 'simple':
                return {
                    'en': result.get('simple_en', ''),
                    'vn': result.get('simple_vn', '')
                }
            else:
                return {
                    'en': result.get('natural_en', ''),
                    'vn': result.get('natural_vn', '')
                }
        
        return {'en': 'Hello, how can I help you?', 'vn': 'Xin chào, tôi có thể giúp gì cho bạn?'}


# Singleton instance
_advisor_instance = None

def get_situation_advisor(provider: str = None) -> SituationAdvisor:
    """Get singleton instance"""
    global _advisor_instance
    if _advisor_instance is None:
        _advisor_instance = SituationAdvisor(provider)
    return _advisor_instance
