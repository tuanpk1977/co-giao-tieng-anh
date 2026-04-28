"""
AI Roleplay Service - Luyện hội thoại thực tế với AI
Tạo người đối thoại ảo để luyện nói theo tình huống
"""

import json
import requests
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

# Import config
import sys
sys.path.append('..')
from config import AI_PROVIDER, OPENAI_API_KEY, GEMINI_API_KEY, QWEN_API_KEY


# Role definitions với personality
ROLES = {
    "teacher": {
        "name": "Ms. Johnson",
        "personality": "friendly teacher",
        "style": "encouraging, patient, gently corrects mistakes",
        "greeting": "Hello! I'm Ms. Johnson. Let's practice English together. How are you today?"
    },
    "friend": {
        "name": "Alex",
        "personality": "casual foreign friend",
        "style": "relaxed, uses slang, friendly and supportive",
        "greeting": "Hey! I'm Alex. Nice to meet you! So, tell me about yourself."
    },
    "customer": {
        "name": "Mr. Smith",
        "personality": "business customer",
        "style": "professional but friendly, clear and direct",
        "greeting": "Good morning! I'm interested in your products. Can you help me?"
    },
    "colleague": {
        "name": "Sarah",
        "personality": "work colleague",
        "style": "casual professional, helpful, team-oriented",
        "greeting": "Hi there! I'm Sarah from the next desk. How's your day going?"
    },
    "interviewer": {
        "name": "Ms. Davis",
        "personality": "HR interviewer",
        "style": "formal, professional, asks good questions",
        "greeting": "Hello, I'm Ms. Davis from HR. Thank you for coming today. Please, have a seat and tell me about yourself."
    },
    "salesperson": {
        "name": "Tom",
        "personality": "helpful shop assistant",
        "style": "enthusiastic, helpful, describes products well",
        "greeting": "Hi! Welcome to our store! I'm Tom. What are you looking for today?"
    }
}


# Situation contexts
SITUATIONS = {
    "greeting": {
        "name": "Chào hỏi lần đầu",
        "context": "First time meeting someone",
        "goals": ["Introduce yourself", "Ask about them", "Keep conversation going"]
    },
    "self_intro": {
        "name": "Giới thiệu bản thân",
        "context": "Telling someone about yourself",
        "goals": ["Name, job, hobbies", "Be interesting", "Ask follow-up questions"]
    },
    "directions": {
        "name": "Hỏi đường",
        "context": "Asking for and giving directions",
        "goals": ["Ask clearly", "Understand directions", "Confirm understanding"]
    },
    "shopping": {
        "name": "Mua hàng",
        "context": "Buying something in a store",
        "goals": ["Ask about products", "Discuss price", "Make decision"]
    },
    "cafe": {
        "name": "Gọi món nước/cà phê",
        "context": "Ordering at a cafe or restaurant",
        "goals": ["Order clearly", "Ask about menu", "Be polite"]
    },
    "interview": {
        "name": "Phỏng vấn xin việc",
        "context": "Job interview situation",
        "goals": ["Answer professionally", "Show qualifications", "Ask good questions"]
    },
    "customer_service": {
        "name": "Nói chuyện với khách hàng",
        "context": "Helping a customer with their needs",
        "goals": ["Be helpful", "Solve problems", "Be professional"]
    },
    "workplace": {
        "name": "Giao tiếp trong xưởng/công việc",
        "context": "Talking with coworkers at work",
        "goals": ["Discuss tasks", "Ask for help", "Be collaborative"]
    }
}


class RoleplayService:
    """Service cho roleplay conversation với AI"""
    
    def __init__(self, provider: str = None):
        self.provider = provider or AI_PROVIDER
        self.api_key = self._get_api_key()
        self.conversation_history = []
        self.current_role = None
        self.current_situation = None
        self.user_profile = None  # Store user profile for personalization
        self.last_user_message_time = None
        self.conversation_turn = 0
        
    def _get_api_key(self):
        if self.provider == "openai":
            return OPENAI_API_KEY
        elif self.provider == "gemini":
            return GEMINI_API_KEY
        elif self.provider == "qwen":
            return QWEN_API_KEY
        return None
    
    def start_roleplay(self, role: str, situation: str, user_name: str = "you", 
                      user_profile: Dict = None) -> Dict[str, Any]:
        """
        Bắt đầu roleplay mới
        
        Args:
            role: vai người đối thoại (teacher, friend, customer, etc.)
            situation: tình huống (greeting, shopping, etc.)
            user_name: tên người học
            user_profile: thông tin user để cá nhân hóa
            
        Returns:
            Dict chứa greeting và thông tin setup
        """
        self.current_role = ROLES.get(role, ROLES["teacher"])
        self.current_situation = SITUATIONS.get(situation, SITUATIONS["greeting"])
        self.conversation_history = []
        # Normalize user_profile
        if user_profile is None:
            self.user_profile = {}
        elif isinstance(user_profile, str):
            self.user_profile = {"name": user_profile}
        elif isinstance(user_profile, dict):
            self.user_profile = user_profile
        else:
            self.user_profile = {}
        self.conversation_turn = 0
        self.last_user_message_time = datetime.now()
        
        # Create system prompt cho roleplay với personalization
        system_prompt = self._create_roleplay_prompt(user_name)
        
        # Get initial greeting from AI
        greeting = self._generate_personalized_greeting(user_name)
        
        return {
            "success": True,
            "role": self.current_role,
            "situation": self.current_situation,
            "greeting": greeting,
            "system_prompt": system_prompt
        }
    
    def _generate_personalized_greeting(self, user_name: str) -> str:
        """Tạo greeting dựa trên user profile"""
        role = self.current_role
        situation = self.current_situation
        
        # Get profile info for personalization
        level = self.user_profile.get('level', 'beginner') if self.user_profile else 'beginner'
        job = self.user_profile.get('job', '') if self.user_profile else ''
        goal = self.user_profile.get('goal', 'communication') if self.user_profile else 'communication'
        
        # Customize greeting based on user level
        if level == 'beginner':
            # Simpler greeting for beginners
            simple_greetings = {
                'greeting': f"Hi {user_name}! I'm {role['name']}. Nice to meet you! Where are you from?",
                'self_intro': f"Hello {user_name}! I'm {role['name']}. Tell me about yourself - what do you do?",
                'cafe': f"Hi {user_name}! Welcome! What would you like to drink?",
                'shopping': f"Hello {user_name}! Looking for something special today?",
                'interview': f"Hello {user_name}, I'm {role['name']}. Let's talk about your experience. What job do you do now?",
                'workplace': f"Hey {user_name}! I'm {role['name']}. How's your work going today?",
                'customer_service': f"Hi {user_name}! I'm {role['name']}. How can I help you today?",
                'directions': f"Hello {user_name}! Do you need help finding something? Where do you want to go?"
            }
        else:
            # More natural greeting for intermediate
            simple_greetings = {
                'greeting': f"Hey {user_name}! I'm {role['name']}. So nice to meet you! What brings you here today?",
                'self_intro': f"Hi {user_name}! I'm {role['name']}. I'd love to hear about what you do. What's your story?",
                'cafe': f"Hey {user_name}! Great to see you! What can I get started for you?",
                'shopping': f"Hi {user_name}! Looking for anything in particular, or just browsing?",
                'interview': f"Hello {user_name}, I'm {role['name']}. Thanks for coming in. Tell me a bit about your background.",
                'workplace': f"Hey {user_name}! How's everything going on your end?",
                'customer_service': f"Hi {user_name}! I'm {role['name']}. What can I do for you today?",
                'directions': f"Hello {user_name}! You look a bit lost. Where are you trying to get to?"
            }
        
        # Get situation key
        situation_key = None
        for key, val in SITUATIONS.items():
            if val['name'] == situation['name']:
                situation_key = key
                break
        
        # If job-related situation and we know user's job, personalize
        if job and situation_key in ['workplace', 'interview', 'customer_service']:
            if 'engineer' in job.lower() or 'mechanic' in job.lower() or 'technical' in job.lower():
                return f"Hi {user_name}! I'm {role['name']}. I heard you work in technical field. What kind of projects are you working on lately?"
            elif 'sales' in job.lower() or 'marketing' in job.lower():
                return f"Hey {user_name}! I'm {role['name']}. Working in sales must be interesting! How do you usually approach new customers?"
            elif 'cafe' in job.lower() or 'coffee' in job.lower() or 'barista' in job.lower():
                return f"Hi {user_name}! I'm {role['name']}. Working with coffee sounds fun! What's your favorite drink to make?"
        
        return simple_greetings.get(situation_key, role['greeting'])
    
    def _create_roleplay_prompt(self, user_name: str) -> str:
        """Tạo system prompt cho roleplay mode với personalization"""
        role = self.current_role
        situation = self.current_situation
        
        # Get user profile info
        level = self.user_profile.get('level', 'beginner') if self.user_profile else 'beginner'
        job = self.user_profile.get('job', '') if self.user_profile else ''
        goal = self.user_profile.get('goal', 'communication') if self.user_profile else 'communication'
        
        # Adjust conversation style based on level
        if level == 'beginner':
            complexity_instruction = """Use SIMPLE language:
- Short sentences (5-8 words max)
- Basic vocabulary only
- One idea per sentence
- Speak slowly and clearly"""
        elif level == 'elementary':
            complexity_instruction = """Use CLEAR language:
- Short sentences (up to 12 words)
- Common vocabulary
- Simple questions"""
        else:  # intermediate
            complexity_instruction = """Use NATURAL language:
- Normal conversation speed
- Varied vocabulary
- Natural flow"""
        
        # Job-specific context if available
        job_context = ""
        if job:
            job_context = f"\nThe user works as: {job}. Try to relate the conversation to their field when appropriate."
        
        prompt = f"""You are {role['name']}, a {role['personality']}. 
Your speaking style is: {role['style']}

CURRENT SITUATION: {situation['name']}
Context: {situation['context']}
Conversation goals: {', '.join(situation['goals'])}

USER PROFILE:
Name: {user_name}
Level: {level}
Goal: {goal}{job_context}

CRITICAL RULES (MUST FOLLOW):
1. ALWAYS end your response with a QUESTION to keep conversation going
2. Stay in character as {role['name']} at all times
3. Keep responses SHORT (1-2 sentences)
4. React naturally to what the user says
5. NEVER give long explanations or lectures
6. If user makes mistakes, ignore them and respond naturally (don't correct)

COMPLEXITY LEVEL ({level}):
{complexity_instruction}

CONVERSATION FLOW:
- React to user's message briefly (1 sentence)
- Ask a related follow-up question
- Example: "That sounds nice! What do you like about it?"
- Example: "I see! How long have you been doing that?"
- Example: "Really? Tell me more about that!"

ANTI-STOP RULES:
- Never end with just "That's great" or "I see" - always ask something
- If user gives short answer, ask for details
- Keep the conversation ball rolling

Remember: You're a REAL person chatting, not a teacher. Keep it short, natural, and ALWAYS ask a follow-up question!"""
        
        return prompt
    
    def chat_roleplay(self, user_message: str) -> Dict[str, Any]:
        """
        Xử lý message trong roleplay mode
        
        Args:
            user_message: câu user nói
            
        Returns:
            Dict chứa AI response và phân tích
        """
        if not self.current_role or not self.current_situation:
            return {
                "success": False,
                "error": "Roleplay not initialized. Call start_roleplay first."
            }
        
        # Update tracking
        self.last_user_message_time = datetime.now()
        self.conversation_turn += 1
        
        # Add to history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Get AI response
        ai_response = self._get_ai_response()
        
        # Analyze user message
        analysis = self._analyze_user_message(user_message)
        
        # Add AI response to history
        self.conversation_history.append({"role": "assistant", "content": ai_response})
        
        # Keep history manageable
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
        
        return {
            "success": True,
            "ai_response": ai_response,
            "analysis": analysis,
            "conversation_turn": len(self.conversation_history) // 2
        }
    
    def _get_ai_response(self) -> str:
        """Gọi AI để lấy response"""
        if self.provider == "openai":
            return self._call_openai()
        elif self.provider == "demo":
            return self._call_demo()
        else:
            return self._call_openai()  # Default to OpenAI
    
    def _call_openai(self) -> str:
        """Gọi OpenAI API"""
        try:
            system_prompt = self._create_roleplay_prompt("you")
            
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.conversation_history[-10:])  # Last 10 messages
            
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-4o-mini",
                "messages": messages,
                "temperature": 0.8,
                "max_tokens": 150  # Keep responses short
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                return "I'm sorry, I didn't catch that. Could you say it again?"
                
        except Exception as e:
            print(f"[Roleplay] OpenAI error: {e}")
            return "Sorry, I'm having trouble responding. Let's try again!"
    
    def _call_demo(self) -> str:
        """Demo responses khi không có API"""
        import random
        
        demo_responses = [
            "That's interesting! Tell me more about that.",
            "I see! What do you think about it?",
            "Oh really? How did that make you feel?",
            "Nice! So what's your plan next?",
            "I understand. Anything else you'd like to share?",
            "Sounds good! By the way, have you tried...?",
            "That's cool! What about...?",
        ]
        
        return random.choice(demo_responses)
    
    def _analyze_user_message(self, user_message: str) -> Dict[str, Any]:
        """
        Phân tích chi tiết câu nói của user
        Trả về format mới với lỗi cụ thể + giải thích tiếng Việt
        """
        import re
        
        message_lower = user_message.lower().strip()
        words = message_lower.split()
        original_message = user_message.strip()
        
        # Initialize result structure
        result = {
            "original_sentence": original_message,
            "errors": [],
            "corrections": [],
            "explanations_vn": [],
            "emotions": [],
            "grammar_score": 3,
            "naturalness_score": 3,
            "better_version": "",
            "word_count": len(words)
        }
        
        # === DETAILED ERROR ANALYSIS ===
        errors = []
        corrections = []
        explanations = []
        
        # 1. Check for common word choice errors
        word_errors = self._check_word_errors(message_lower, original_message)
        errors.extend(word_errors['errors'])
        corrections.extend(word_errors['corrections'])
        explanations.extend(word_errors['explanations'])
        
        # 2. Check for missing articles (a/an/the)
        article_errors = self._check_articles(message_lower, original_message)
        errors.extend(article_errors['errors'])
        corrections.extend(article_errors['corrections'])
        explanations.extend(article_errors['explanations'])
        
        # 3. Check for missing auxiliaries (is/are/am/do/does)
        aux_errors = self._check_auxiliaries(message_lower, original_message)
        errors.extend(aux_errors['errors'])
        corrections.extend(aux_errors['corrections'])
        explanations.extend(aux_errors['explanations'])
        
        # 4. Check prepositions
        prep_errors = self._check_prepositions(message_lower, original_message)
        errors.extend(prep_errors['errors'])
        corrections.extend(prep_errors['corrections'])
        explanations.extend(prep_errors['explanations'])
        
        # 5. Check for contractions (naturalness)
        contraction_suggestions = self._check_contractions(message_lower, original_message)
        
        # === EMOTION ANALYSIS ===
        emotions = self._detect_emotions(message_lower, words)
        
        # === SCORING ===
        grammar_score = self._calculate_grammar_score(errors, len(words))
        naturalness_score = self._calculate_naturalness_v2(message_lower, words, contraction_suggestions)
        
        # === GENERATE BETTER VERSION ===
        better_version = self._generate_better_version(original_message, errors, corrections, contraction_suggestions)
        
        # === FORMAT FINAL OUTPUT ===
        result.update({
            "errors": errors,
            "corrections": corrections,
            "explanations_vn": explanations,
            "emotions": emotions,
            "grammar_score": grammar_score,
            "naturalness_score": naturalness_score,
            "better_version": better_version,
            "suggestions": self._format_suggestions_vn(errors, explanations, contraction_suggestions),
            "practice_sentence": better_version
        })
        
        return result
    
    def _check_word_errors(self, message_lower: str, original: str) -> Dict:
        """Kiểm tra lỗi chọn từ phổ biến"""
        errors = []
        corrections = []
        explanations = []
        
        # Common word errors with corrections
        word_error_patterns = [
            (r'\bvery\s+(like|love|enjoy|hate|want|need)\b', 
             r'really\s+\1',
             '"very" không đi với động từ → dùng "really"'),
            (r'\bi\s+am\s+agree\b',
             r'I agree',
             'Agree là động từ, không cần "am" → I agree'),
            (r'\bi\s+am\s+disagree\b',
             r'I disagree',
             'Disagree là động từ, không cần "am" → I disagree'),
            (r'\bi\s+am\s+feel\b',
             r'I feel',
             'Feel là động từ, không cần "am" → I feel'),
            (r'\bi\s+am\s+think\b',
             r'I think',
             'Think là động từ, không cần "am" → I think'),
            (r'\bi\s+am\s+know\b',
             r'I know',
             'Know là động từ, không cần "am" → I know'),
            (r'\bexplain\s+me\b',
             r'explain to me',
             'Explain cần giới từ "to" → explain to me'),
            (r'\bsuggest\s+me\b',
             r'suggest to me',
             'Suggest cần giới từ "to" → suggest to me'),
            (r'\bgo\s+to\s+home\b',
             r'go home',
             'Home là trạng từ, không cần "to" → go home'),
            (r'\bdiscuss\s+about\b',
             r'discuss',
             'Discuss đã có nghĩa "nói về", không cần "about"'),
            (r'\blook\s+forward\s+to\s+see\b',
             r'look forward to seeing',
             'Sau "to" trong cụm này là V-ing → seeing'),
            (r'\binterested\s+on\b',
             r'interested in',
             'Interested đi với giới từ "in"'),
            (r'\bresponsible\s+of\b',
             r'responsible for',
             'Responsible đi với giới từ "for"'),
            (r'\bsimilar\s+with\b',
             r'similar to',
             'Similar đi với giới từ "to"'),
            (r'\bmany\s+much\b',
             r'many/much',
             'Many cho danh từ đếm được, much cho không đếm được'),
            (r'\bmuch\s+people\b',
             r'many people',
             'People đếm được → dùng many, không dùng much'),
            (r'\bhow\s+to\s+say\s+this\s+word\b',
             r'how do you say this word',
             'Hỏi cách nói: How do you say...'),
            (r'\bwhat\s+you\s+call\b',
             r'what do you call',
             'Cần trợ động từ: What do you call...'),
        ]
        
        import re
        for pattern, correction, explanation in word_error_patterns:
            if re.search(pattern, message_lower):
                errors.append(re.search(pattern, message_lower).group())
                corrections.append(correction.replace(r'\1', re.search(pattern, message_lower).group(1) if re.search(pattern, message_lower).groups() else ''))
                explanations.append(explanation)
        
        return {"errors": errors, "corrections": corrections, "explanations": explanations}
    
    def _check_articles(self, message_lower: str, original: str) -> Dict:
        """Kiểm tra lỗi mạo từ"""
        errors = []
        corrections = []
        explanations = []
        
        import re
        
        # Check for missing 'a/an' before singular countable nouns
        # Simple pattern: "I am engineer" → "I am an engineer"
        article_patterns = [
            (r'\bi\s+am\s+([aeiou][a-z]+)\b', r'an \1', 'Thiếu mạo từ "an" trước nguyên âm'),
            (r'\bi\s+am\s+([bcdfgjklmnpqrstvxz][a-z]+)\b', r'a \1', 'Thiếu mạo từ "a" trước phụ âm'),
            (r'\bi\s+have\s+(\w+)\s+([aeiou][a-z]+)\b', r'have a \2', 'Thiếu mạo từ "a/an"'),
        ]
        
        # Only flag if it looks like a profession/role
        professions = ['engineer', 'doctor', 'teacher', 'student', 'manager', 'developer', 
                       'artist', 'architect', 'actor', 'accountant', 'nurse', 'lawyer']
        
        for prof in professions:
            if re.search(rf'\bi\s+am\s+{prof}\b', message_lower):
                if prof[0] in 'aeiou':
                    errors.append(f"I am {prof}")
                    corrections.append(f"I am an {prof}")
                    explanations.append(f'"{prof}" bắt đầu bằng nguyên âm → thêm "an"')
                else:
                    errors.append(f"I am {prof}")
                    corrections.append(f"I am a {prof}")
                    explanations.append(f'Cần mạo từ "a" trước nghề nghiệp')
        
        return {"errors": errors, "corrections": corrections, "explanations": explanations}
    
    def _check_auxiliaries(self, message_lower: str, original: str) -> Dict:
        """Kiểm tra thiếu trợ động từ (is/are/am/do/does)"""
        errors = []
        corrections = []
        explanations = []
        
        import re
        
        # Questions missing auxiliary
        question_patterns = [
            (r'\bwhere\s+you\s+(live|work|study)\b', r'Where do you \1', 'Câu hỏi thiếu trợ động từ "do"'),
            (r'\bwhat\s+you\s+(do|want|like|think)\b', r'What do you \1', 'Câu hỏi thiếu trợ động từ "do"'),
            (r'\bhow\s+you\s+(feel|do|go)\b', r'How do you \1', 'Câu hỏi thiếu trợ động từ "do"'),
            (r'\bwhen\s+you\s+(come|go|start)\b', r'When do you \1', 'Câu hỏi thiếu trợ động từ "do"'),
            (r'\bwhy\s+you\s+(do|think|say)\b', r'Why do you \1', 'Câu hỏi thiếu trợ động từ "do"'),
        ]
        
        for pattern, correction, explanation in question_patterns:
            match = re.search(pattern, message_lower)
            if match:
                errors.append(match.group())
                corrections.append(correction.replace(r'\1', match.group(1)))
                explanations.append(explanation)
        
        # Check for missing "is/are" in "there" constructions
        if 'there' in message_lower:
            if re.search(r'\bthere\s+(many|some|a\s+lot|few|several)\b', message_lower):
                # Check if missing "are"
                if not re.search(r'\bthere\s+(are|is)\b', message_lower):
                    errors.append("There many/several...")
                    corrections.append("There are many/several...")
                    explanations.append('Sau "there" cần động từ "to be" (is/are)')
        
        return {"errors": errors, "corrections": corrections, "explanations": explanations}
    
    def _check_prepositions(self, message_lower: str, original: str) -> Dict:
        """Kiểm tra lỗi giới từ"""
        errors = []
        corrections = []
        explanations = []
        
        import re
        
        prep_patterns = [
            (r'\barrive\s+to\b', r'arrive at/in', 'Arrive đi với "at" (nhỏ) hoặc "in" (lớn)'),
            (r'\blive\s+in\s+(hanoi|hochiminh|danang|saigon)\b', r'live in', 'OK - live in + thành phố'),
            (r'\bdepend\s+of\b', r'depend on', 'Depend đi với giới từ "on"'),
            (r'\blisten\s+music\b', r'listen to music', 'Listen là nội động từ, cần "to"'),
            (r'\btalk\s+you\b', r'talk to you', 'Talk đi với giới từ "to/with"'),
            (r'\bspeak\s+english\s+with\s+you\b', None, 'OK - speak + ngôn ngữ'),
        ]
        
        for pattern, correction, explanation in prep_patterns:
            if re.search(pattern, message_lower):
                match = re.search(pattern, message_lower)
                if correction:  # Only flag if there's a correction
                    errors.append(match.group())
                    corrections.append(correction)
                    explanations.append(explanation)
        
        return {"errors": errors, "corrections": corrections, "explanations": explanations}
    
    def _check_contractions(self, message_lower: str, original: str) -> List[Dict]:
        """Kiểm tra xem có thể dùng contractions để tự nhiên hơn"""
        suggestions = []
        
        contraction_pairs = [
            ('i am', "I'm", 'Dùng "I\'m" thay "I am" tự nhiên hơn'),
            ('you are', "you're", 'Dùng "you\'re" thay "you are"'),
            ('he is', "he's", 'Dùng "he\'s" thay "he is"'),
            ('she is', "she's", 'Dùng "she\'s" thay "she is"'),
            ('it is', "it's", 'Dùng "it\'s" thay "it is"'),
            ('they are', "they're", 'Dùng "they\'re" thay "they are"'),
            ('we are', "we're", 'Dùng "we\'re" thay "we are"'),
            ('do not', "don't", 'Dùng "don\'t" thay "do not"'),
            ('does not', "doesn't", 'Dùng "doesn\'t" thay "does not"'),
            ('did not', "didn't", 'Dùng "didn\'t" thay "did not"'),
            ('is not', "isn't", 'Dùng "isn\'t" thay "is not"'),
            ('are not', "aren't", 'Dùng "aren\'t" thay "are not"'),
            ('was not', "wasn't", 'Dùng "wasn\'t" thay "was not"'),
            ('were not', "weren't", 'Dùng "weren\'t" thay "were not"'),
            ('cannot', "can't", 'Dùng "can\'t" thay "cannot"'),
            ('could not', "couldn't", 'Dùng "couldn\'t" thay "could not"'),
            ('would not', "wouldn't", 'Dùng "wouldn\'t" thay "would not"'),
            ('should not', "shouldn't", 'Dùng "shouldn\'t" thay "should not"'),
            ('will not', "won't", 'Dùng "won\'t" thay "will not"'),
            ('i have', "I've", 'Dùng "I\'ve" thay "I have"'),
            ('you have', "you've", 'Dùng "you\'ve" thay "you have"'),
            ('i will', "I'll", 'Dùng "I\'ll" thay "I will"'),
            ('you will', "you'll", 'Dùng "you\'ll" thay "you will"'),
        ]
        
        for full, contraction, explanation in contraction_pairs:
            if full in message_lower:
                suggestions.append({
                    'original': full,
                    'contraction': contraction,
                    'explanation': explanation
                })
        
        return suggestions
    
    def _detect_emotions(self, message_lower: str, words: List[str]) -> List[str]:
        """Phát hiện cảm xúc trong câu"""
        emotions = []
        
        if any(w in message_lower for w in ['sure', 'definitely', 'absolutely', 'of course', 'certainly', 'exactly']):
            emotions.append("confident")
        
        if any(w in message_lower for w in ['um', 'uh', 'maybe', 'perhaps', 'i think', 'sort of', 'kind of']):
            emotions.append("hesitant")
        
        if any(w in message_lower for w in ['great', 'awesome', 'nice', 'love', 'like', 'thanks', 'thank', 'wonderful', 'amazing']):
            emotions.append("friendly")
        
        if any(w in message_lower for w in ['please', 'sorry', 'excuse', 'would you', 'could you', 'may i']):
            emotions.append("polite")
        
        if len(words) <= 2:
            emotions.append("unclear")
        
        if self.current_situation and self.current_situation.get('name') in ['Casual chat', 'Coffee shop']:
            if any(w in message_lower for w in ['dear sir', 'madam', 'yours faithfully', 'sincerely']):
                emotions.append("too formal")
        
        return emotions if emotions else ["neutral"]
    
    def _calculate_grammar_score(self, errors: List[str], word_count: int) -> int:
        """Tính điểm ngữ pháp 1-5"""
        if not errors:
            return 5
        
        error_count = len(errors)
        
        # Score based on error density
        if word_count == 0:
            return 3
        
        error_ratio = error_count / word_count
        
        if error_ratio == 0:
            return 5
        elif error_ratio <= 0.1:
            return 4
        elif error_ratio <= 0.2:
            return 3
        elif error_ratio <= 0.3:
            return 2
        else:
            return 1
    
    def _calculate_naturalness_v2(self, message_lower: str, words: List[str], contractions: List[Dict]) -> int:
        """Tính điểm tự nhiên 1-5"""
        score = 3
        
        # +1 for appropriate length
        if 5 <= len(words) <= 20:
            score += 1
        
        # -1 if too short
        if len(words) < 3:
            score -= 1
        
        # +1 for using contractions
        if contractions:
            score += 0.5
        
        # +1 for contractions already used
        if any(c in message_lower for c in ["'m", "'re", "'s", "'ll", "'d", "'ve", "n't"]):
            score += 0.5
        
        # -1 if too many fillers
        fillers = message_lower.count('um') + message_lower.count('uh')
        if fillers > 2:
            score -= 1
        
        # Check for complete sentences
        if message_lower.strip()[-1] in '.!?':
            score += 0.5
        
        return max(1, min(5, int(score)))
    
    def _generate_better_version(self, original: str, errors: List[str], corrections: List[str], contractions: List[Dict]) -> str:
        """Tạo phiên bản câu tốt hơn"""
        import re
        
        improved = original
        
        # Apply corrections
        for error, correction in zip(errors, corrections):
            if error and correction:
                improved = re.sub(re.escape(error), correction, improved, flags=re.IGNORECASE)
        
        # Apply contractions for naturalness
        for contr in contractions:
            improved = re.sub(r'\b' + re.escape(contr['original']) + r'\b', contr['contraction'], improved, flags=re.IGNORECASE)
        
        # Clean up fillers
        improved = re.sub(r'\b(um|uh)\b[,\s]*', '', improved, flags=re.IGNORECASE)
        
        # Capitalize first letter
        improved = improved.strip()
        if improved:
            improved = improved[0].upper() + improved[1:]
        
        # Add period if missing
        if improved and improved[-1] not in '.!?':
            improved += '.'
        
        # Clean up extra spaces
        improved = re.sub(r'\s+', ' ', improved)
        
        return improved
    
    def _format_suggestions_vn(self, errors: List[str], explanations: List[str], contractions: List[Dict]) -> List[str]:
        """Format suggestions cho UI"""
        suggestions = []
        
        for exp in explanations:
            suggestions.append(exp)
        
        for contr in contractions[:2]:  # Limit contraction suggestions
            suggestions.append(contr['explanation'])
        
        return suggestions
    
    def _calculate_naturalness(self, message: str, words: List[str]) -> int:
        """Tính điểm tự nhiên 1-5"""
        score = 3  # Base score
        
        # +1 for appropriate length (not too short, not too long)
        if 5 <= len(words) <= 20:
            score += 1
        
        # -1 if too short
        if len(words) < 3:
            score -= 1
        
        # +1 if uses contractions (natural speech)
        if any(c in message.lower() for c in ["'m", "'re", "'s", "'ll", "'d", "'ve"]):
            score += 1
        
        # -1 if too many filler words
        fillers = message.lower().count('um') + message.lower().count('uh')
        if fillers > 2:
            score -= 1
        
        # Check for complete sentences
        if message.strip()[-1] in '.!?':
            score += 0.5
        
        return max(1, min(5, int(score)))
    
    def _generate_suggestions(self, message: str, words: List[str]) -> List[str]:
        """Tạo gợi ý cải thiện"""
        suggestions = []
        
        # Suggest contractions for more natural speech
        if "i am" in message.lower():
            suggestions.append("Try 'I'm' instead of 'I am' for more natural speech")
        if "you are" in message.lower():
            suggestions.append("Try 'you're' instead of 'you are'")
        if "do not" in message.lower():
            suggestions.append("Try 'don't' instead of 'do not'")
        
        # Suggest alternatives if very short
        if len(words) < 3:
            suggestions.append("Try adding a bit more detail to your answer")
        
        # Suggest reducing fillers
        fillers = message.lower().count('um') + message.lower().count('uh')
        if fillers > 1:
            suggestions.append("Try to pause instead of using 'um' - it's okay to take a moment!")
        
        return suggestions
    
    def _generate_practice_sentence(self, user_message: str) -> str:
        """Tạo câu luyện lại tốt hơn"""
        # Simple improvements
        improved = user_message
        
        # Basic improvements
        improved = improved.replace("I am ", "I'm ")
        improved = improved.replace("You are ", "You're ")
        improved = improved.replace("It is ", "It's ")
        improved = improved.replace("Do not ", "Don't ")
        improved = improved.replace("Cannot ", "Can't ")
        
        # Remove excessive fillers
        import re
        improved = re.sub(r'\b(um|uh)\b[,\s]*', '', improved, flags=re.IGNORECASE)
        
        # Capitalize first letter
        improved = improved.strip()
        if improved:
            improved = improved[0].upper() + improved[1:]
        
        # Add period if missing
        if improved and improved[-1] not in '.!?':
            improved += '.'
        
        return improved
    
    def get_feedback_summary(self) -> Dict[str, Any]:
        """Tạo tóm tắt sau buổi luyện"""
        if not self.conversation_history:
            return {"error": "No conversation yet"}
        
        # Analyze all user messages
        user_messages = [msg["content"] for msg in self.conversation_history if msg["role"] == "user"]
        
        total_turns = len(user_messages)
        total_words = sum(len(msg.split()) for msg in user_messages)
        
        # Collect emotions
        all_emotions = []
        for msg in user_messages:
            analysis = self._analyze_user_message(msg)
            all_emotions.extend(analysis["emotions"])
        
        # Most common emotions
        from collections import Counter
        emotion_counts = Counter(all_emotions)
        top_emotions = emotion_counts.most_common(3)
        
        return {
            "total_turns": total_turns,
            "total_words": total_words,
            "average_words_per_turn": round(total_words / total_turns, 1) if total_turns > 0 else 0,
            "top_emotions": top_emotions,
            "role": self.current_role["name"] if self.current_role else None,
            "situation": self.current_situation["name"] if self.current_situation else None
        }


# Singleton instance
_roleplay_service = None

def get_roleplay_service(provider: str = None) -> RoleplayService:
    """Get or create singleton instance"""
    global _roleplay_service
    if _roleplay_service is None:
        _roleplay_service = RoleplayService(provider)
    return _roleplay_service
