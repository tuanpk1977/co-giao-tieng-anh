"""Fixed hybrid roadmap seed data.

This keeps the default learning path cheap: core lesson content is static,
while AI is only enabled on targeted actions such as explain, coach, roleplay,
and correction.
"""

ROADMAP_LEVELS = [
    {
        "id": "starter",
        "title": "Starter",
        "description": "Nen tang cho nguoi moi hoc: greetings, school, family, daily objects.",
        "target": "CEFR Pre-A1",
        "order": 1,
    },
    {
        "id": "flyer",
        "title": "Flyer",
        "description": "Mo rong tu vung va cau dai hon theo Cambridge Flyers.",
        "target": "CEFR A2",
        "order": 2,
    },
    {"id": "ket", "title": "KET", "description": "Tien A2-Key: daily life, travel, short messages.", "target": "A2", "order": 3},
    {"id": "pet", "title": "PET", "description": "B1 Preliminary: opinions, stories, problem solving.", "target": "B1", "order": 4},
    {"id": "ielts_foundation", "title": "IELTS Foundation", "description": "Nen tang IELTS: topic vocabulary and simple task answers.", "target": "IELTS 4.0", "order": 5},
    {"id": "ielts_50", "title": "IELTS 5.0", "description": "IELTS band 5.0: paragraph writing, speaking part 1-2.", "target": "IELTS 5.0", "order": 6},
    {"id": "ielts_65", "title": "IELTS 6.5+", "description": "IELTS band 6.5+: coherence, argument, advanced roleplay.", "target": "IELTS 6.5+", "order": 7},
    {"id": "business", "title": "Business English", "description": "Meetings, email, presentation and negotiation basics.", "target": "Workplace", "order": 8},
    {"id": "sales", "title": "English for Sales", "description": "Customer needs, product pitch, objection handling.", "target": "Sales", "order": 9},
    {"id": "cafe", "title": "English for Cafe Staff", "description": "Taking orders, apologizing, recommending drinks.", "target": "Cafe Staff", "order": 10},
    {"id": "factory", "title": "English for Factory Workers", "description": "Safety, shifts, machine issues and supervisor communication.", "target": "Factory", "order": 11},
]


def _lesson(level_id, unit_id, lesson_type, title, order, content, ai=False, ai_type="none", audio_url=""):
    return {
        "id": f"{unit_id}_{lesson_type}",
        "levelId": level_id,
        "unitId": unit_id,
        "type": lesson_type,
        "title": title,
        "content": content,
        "audioUrl": audio_url,
        "order": order,
        "isAiEnabled": ai,
        "aiFeatureType": ai_type,
    }


ROADMAP_UNITS = [
    {
        "id": "starter_u1",
        "levelId": "starter",
        "title": "Unit 1: Hello and My Class",
        "description": "Say hello, introduce yourself, and talk about classroom objects.",
        "order": 1,
        "lessons": [
            _lesson("starter", "starter_u1", "vocabulary", "Classroom Words", 1, {
                "words": [
                    {"word": "book", "meaning": "quyen sach", "example": "This is my book."},
                    {"word": "pen", "meaning": "but", "example": "I have a blue pen."},
                    {"word": "teacher", "meaning": "giao vien", "example": "She is my teacher."},
                    {"word": "student", "meaning": "hoc sinh", "example": "I am a student."},
                    {"word": "desk", "meaning": "ban hoc", "example": "The book is on the desk."},
                ]
            }),
            _lesson("starter", "starter_u1", "grammar", "I am / This is", 2, {
                "rules": ["Use 'I am' to introduce yourself.", "Use 'This is' for one object or person."],
                "examples": ["I am Lan.", "This is my teacher.", "This is a pen."],
            }, ai=True, ai_type="explain"),
            _lesson("starter", "starter_u1", "listening", "Classroom Dialogue", 3, {
                "dialogue": [
                    {"speaker": "A", "text": "Hello. What is your name?"},
                    {"speaker": "B", "text": "My name is Linh."},
                    {"speaker": "A", "text": "This is my book."},
                ]
            }),
            _lesson("starter", "starter_u1", "speaking", "Introduce Yourself", 4, {
                "practice": ["Hello, my name is ...", "I am a student.", "This is my book."]
            }, ai=True, ai_type="speaking_correction"),
            _lesson("starter", "starter_u1", "quiz", "Mini Quiz", 5, {
                "questions": [
                    {"question": "'Book' means?", "options": ["but", "sach", "ban"], "answer": "sach"},
                    {"question": "Choose correct: ___ am Lan.", "options": ["I", "You", "This"], "answer": "I"},
                ]
            }),
            _lesson("starter", "starter_u1", "review", "Review", 6, {
                "prompts": ["Say 3 classroom words.", "Introduce yourself in one sentence."]
            }, ai=True, ai_type="coach"),
        ],
    },
    {
        "id": "starter_u2",
        "levelId": "starter",
        "title": "Unit 2: My Family",
        "description": "Talk about family members with simple sentences.",
        "order": 2,
        "lessons": [
            _lesson("starter", "starter_u2", "vocabulary", "Family Words", 1, {
                "words": [
                    {"word": "mother", "meaning": "me", "example": "This is my mother."},
                    {"word": "father", "meaning": "bo", "example": "This is my father."},
                    {"word": "sister", "meaning": "chi/em gai", "example": "She is my sister."},
                    {"word": "brother", "meaning": "anh/em trai", "example": "He is my brother."},
                ]
            }),
            _lesson("starter", "starter_u2", "grammar", "He is / She is", 2, {
                "rules": ["Use 'he' for a boy/man.", "Use 'she' for a girl/woman."],
                "examples": ["He is my father.", "She is my sister."],
            }, ai=True, ai_type="explain"),
            _lesson("starter", "starter_u2", "quiz", "Mini Quiz", 3, {
                "questions": [{"question": "Choose: ___ is my mother.", "options": ["He", "She", "It"], "answer": "She"}]
            }),
        ],
    },
    {
        "id": "flyer_u1",
        "levelId": "flyer",
        "title": "Unit 1: Daily Routines",
        "description": "Talk about routines and time with present simple.",
        "order": 1,
        "lessons": [
            _lesson("flyer", "flyer_u1", "vocabulary", "Daily Routine Words", 1, {
                "words": [
                    {"word": "wake up", "meaning": "thuc day", "example": "I wake up at six."},
                    {"word": "brush my teeth", "meaning": "danh rang", "example": "I brush my teeth every morning."},
                    {"word": "have breakfast", "meaning": "an sang", "example": "She has breakfast at seven."},
                    {"word": "go to school", "meaning": "di hoc", "example": "We go to school by bus."},
                ]
            }),
            _lesson("flyer", "flyer_u1", "grammar", "Present Simple", 2, {
                "rules": ["Use present simple for habits.", "Add s/es with he, she, it."],
                "examples": ["I wake up at six.", "She goes to school at seven."],
            }, ai=True, ai_type="explain"),
            _lesson("flyer", "flyer_u1", "listening", "Morning Routine", 3, {
                "dialogue": [
                    {"speaker": "A", "text": "What time do you wake up?"},
                    {"speaker": "B", "text": "I wake up at six thirty."},
                ]
            }),
            _lesson("flyer", "flyer_u1", "speaking", "My Morning", 4, {
                "practice": ["I wake up at ...", "I have breakfast at ...", "I go to school by ..."]
            }, ai=True, ai_type="speaking_correction"),
            _lesson("flyer", "flyer_u1", "quiz", "Mini Quiz", 5, {
                "questions": [{"question": "She ___ breakfast at seven.", "options": ["have", "has", "having"], "answer": "has"}]
            }),
            _lesson("flyer", "flyer_u1", "review", "Review", 6, {
                "prompts": ["Tell your morning routine in 3 sentences."]
            }, ai=True, ai_type="coach"),
        ],
    },
    {
        "id": "flyer_u2",
        "levelId": "flyer",
        "title": "Unit 2: Places in Town",
        "description": "Ask and answer about places and directions.",
        "order": 2,
        "lessons": [
            _lesson("flyer", "flyer_u2", "vocabulary", "Town Places", 1, {
                "words": [
                    {"word": "library", "meaning": "thu vien", "example": "The library is near my school."},
                    {"word": "station", "meaning": "nha ga", "example": "The station is on King Street."},
                    {"word": "between", "meaning": "o giua", "example": "The cafe is between the bank and the shop."},
                ]
            }),
            _lesson("flyer", "flyer_u2", "grammar", "Where is ...?", 2, {
                "rules": ["Use 'Where is' to ask about one place.", "Use prepositions: next to, between, opposite."],
                "examples": ["Where is the library?", "It is next to the park."],
            }, ai=True, ai_type="explain"),
            _lesson("flyer", "flyer_u2", "quiz", "Mini Quiz", 3, {
                "questions": [{"question": "The cafe is ___ the bank and shop.", "options": ["between", "under", "behind"], "answer": "between"}]
            }),
        ],
    },
]


for level in ROADMAP_LEVELS:
    if level["id"] not in {"starter", "flyer"}:
        for idx in range(1, 3):
            unit_id = f"{level['id']}_u{idx}"
            ROADMAP_UNITS.append({
                "id": unit_id,
                "levelId": level["id"],
                "title": f"Unit {idx}: Core Skills",
                "description": f"Fixed unit scaffold for {level['title']}.",
                "order": idx,
                "lessons": [
                    _lesson(level["id"], unit_id, "vocabulary", "Core Vocabulary", 1, {"words": []}),
                    _lesson(level["id"], unit_id, "grammar", "Core Grammar", 2, {"rules": [], "examples": []}, ai=True, ai_type="explain"),
                    _lesson(level["id"], unit_id, "listening", "Model Dialogue", 3, {"dialogue": []}),
                    _lesson(level["id"], unit_id, "speaking", "Speaking Practice", 4, {"practice": []}, ai=True, ai_type="speaking_correction"),
                    _lesson(level["id"], unit_id, "quiz", "Mini Quiz", 5, {"questions": []}),
                    _lesson(level["id"], unit_id, "review", "Review", 6, {"prompts": []}, ai=True, ai_type="coach"),
                ],
            })


PLACEMENT_QUESTIONS = [
    {"id": "q1", "skill": "vocabulary", "question": "Choose the greeting.", "options": ["Hello", "Desk", "Blue", "Run"], "answer": "Hello"},
    {"id": "q2", "skill": "grammar", "question": "I ___ a student.", "options": ["am", "is", "are", "be"], "answer": "am"},
    {"id": "q3", "skill": "vocabulary", "question": "'Mother' means?", "options": ["me", "bo", "anh trai", "ban"], "answer": "me"},
    {"id": "q4", "skill": "grammar", "question": "She ___ breakfast at 7.", "options": ["have", "has", "having", "to have"], "answer": "has"},
    {"id": "q5", "skill": "reading", "question": "Tom wakes up at six. What time does he wake up?", "options": ["5", "6", "7", "8"], "answer": "6"},
    {"id": "q6", "skill": "grammar", "question": "Where ___ the library?", "options": ["am", "is", "are", "do"], "answer": "is"},
    {"id": "q7", "skill": "vocabulary", "question": "A place to read books is a ...", "options": ["library", "station", "factory", "kitchen"], "answer": "library"},
    {"id": "q8", "skill": "grammar", "question": "I went to school yesterday. This is ...", "options": ["past", "future", "present", "question"], "answer": "past"},
    {"id": "q9", "skill": "reading", "question": "If someone says 'Could you repeat that?', they want you to ...", "options": ["say again", "stop", "write", "leave"], "answer": "say again"},
    {"id": "q10", "skill": "grammar", "question": "I have lived here ___ 2020.", "options": ["since", "for", "at", "on"], "answer": "since"},
    {"id": "q11", "skill": "vocabulary", "question": "A formal word for 'help' is ...", "options": ["assist", "sleep", "buy", "walk"], "answer": "assist"},
    {"id": "q12", "skill": "grammar", "question": "If I had time, I ___ help you.", "options": ["would", "will", "am", "do"], "answer": "would"},
    {"id": "q13", "skill": "ielts", "question": "IELTS Writing Task 2 usually asks for ...", "options": ["an essay", "a map only", "spelling list", "numbers only"], "answer": "an essay"},
    {"id": "q14", "skill": "business", "question": "'Could we reschedule?' means ...", "options": ["change time", "cancel forever", "pay now", "hire staff"], "answer": "change time"},
    {"id": "q15", "skill": "grammar", "question": "The report ___ by the manager yesterday.", "options": ["was reviewed", "review", "reviews", "is review"], "answer": "was reviewed"},
]
