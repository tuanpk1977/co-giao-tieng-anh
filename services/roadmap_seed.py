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
    {"id": "jp_intro", "title": "Japanese Starter", "description": "Nhap mon truoc N5: bang chu cai, so dem, thu ngay thang va cau chao hoi hang ngay.", "target": "Pre-N5", "order": 100, "language": "japanese"},
    {"id": "jp_n5", "title": "JLPT N5", "description": "Nen tang tieng Nhat: tu vung doi song, cau don gian va ngu phap co ban.", "target": "N5", "order": 101, "language": "japanese"},
    {"id": "jp_n4", "title": "JLPT N4", "description": "Mo rong giao tiep co ban: ke hoach, ly do, thoi quen va hoi dap tu nhien hon.", "target": "N4", "order": 102, "language": "japanese"},
    {"id": "jp_n3", "title": "JLPT N3", "description": "Trung cap: noi ve cong viec, truong hoc, cam xuc, y kien va tinh huong thuc te.", "target": "N3", "order": 103, "language": "japanese"},
    {"id": "jp_n2", "title": "JLPT N2", "description": "Trung cao cap: van phong, tin tuc, tranh luan nhe, keigo va doc hieu dai hon.", "target": "N2", "order": 104, "language": "japanese"},
    {"id": "jp_n1", "title": "JLPT N1", "description": "Nang cao: bieu dat tinh te, chu de xa hoi, kinh doanh va ngon ngu tu nhien.", "target": "N1", "order": 105, "language": "japanese"},
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


def _integrated_lesson(level_id, unit_id, order, title, topic, words, patterns, grammar, dialogue, speaking, quiz, extra_content=None):
    audio_base = f"/static/audio/{level_id}/{unit_id}_l{order}"

    def _vocab_payload(item, idx):
        if isinstance(item, dict):
            payload = dict(item)
        else:
            payload = {
                "word": item[0],
                "meaning": item[1],
                "example": item[2],
            }
            if len(item) > 3:
                payload["reading"] = item[3]
            if len(item) > 4:
                payload["translation"] = item[4]
            if len(item) > 5:
                payload["exampleReading"] = item[5]
            if len(item) > 6:
                payload["exampleTranslation"] = item[6]
        payload.setdefault("word", "")
        payload.setdefault("meaning", "")
        payload.setdefault("example", "")
        payload["audioUrl"] = payload.get("audioUrl") or f"{audio_base}_word_{idx + 1}.mp3"
        return payload

    def _dialogue_payload(item):
        if isinstance(item, dict):
            return dict(item)
        payload = {
            "speaker": item[0],
            "text": item[1],
        }
        if len(item) > 2:
            payload["reading"] = item[2]
        if len(item) > 3:
            payload["translation"] = item[3]
        return payload

    def _speaking_payload(item, idx):
        if isinstance(item, dict):
            payload = dict(item)
        else:
            payload = {"text": item[0] if isinstance(item, tuple) else item}
            if isinstance(item, tuple) and len(item) > 1:
                payload["reading"] = item[1]
            if isinstance(item, tuple) and len(item) > 2:
                payload["translation"] = item[2]
        payload.setdefault("text", "")
        payload["audioUrl"] = payload.get("audioUrl") or f"{audio_base}_speak_{idx + 1}.mp3"
        return payload

    first_speaking = ""
    if speaking:
        first_item = speaking[0]
        if isinstance(first_item, dict):
            first_speaking = first_item.get("text", "")
        elif isinstance(first_item, tuple):
            first_speaking = first_item[0]
        else:
            first_speaking = first_item

    content = {
        "vocabulary": [_vocab_payload(item, idx) for idx, item in enumerate(words)],
        "sentencePatterns": patterns,
        "grammar": grammar,
        "dialogue": [_dialogue_payload(item) for item in dialogue],
        "speaking": [_speaking_payload(item, idx) for idx, item in enumerate(speaking)],
        "quiz": quiz,
        "review": [
            f"Say 3 words about {topic}.",
            f"Make 2 sentences about {topic}.",
            f"Record yourself saying: {first_speaking or title}.",
        ],
    }
    if extra_content:
        content.update(extra_content)

    return {
        "id": f"{unit_id}_lesson_{order}",
        "levelId": level_id,
        "unitId": unit_id,
        "type": "integrated",
        "title": title,
        "topic": topic,
        "order": order,
        "isAiEnabled": True,
        "aiFeatureType": "speaking_correction",
        "audio": {
            "basePath": audio_base,
            "fallback": "browser_tts",
            "dialogueUrl": f"{audio_base}_dialogue.mp3",
            "slowRate": 0.8,
        },
        "content": content,
    }


STARTER_TOPICS = [
    ("Greetings", "Hello and Goodbye", [("hello", "xin chao", "Hello, Mai."), ("goodbye", "tam biet", "Goodbye, teacher."), ("morning", "buoi sang", "Good morning."), ("name", "ten", "My name is Nam."), ("fine", "khoe", "I am fine.")], ["Hello, I am ...", "My name is ...", "How are you?"], ["Use 'I am' to introduce yourself.", "Use 'How are you?' to ask about feelings."], [("A", "Hello. What is your name?"), ("B", "My name is Linh."), ("A", "Nice to meet you.")], ["Hello, my name is Linh.", "I am fine, thank you.", "Nice to meet you."], "'Hello' is a greeting."),
    ("Introductions", "Introduce Yourself", [("student", "hoc sinh", "I am a student."), ("teacher", "giao vien", "She is my teacher."), ("friend", "ban", "This is my friend."), ("class", "lop hoc", "I am in class."), ("meet", "gap", "Nice to meet you.")], ["I am a student.", "This is my friend.", "Nice to meet you."], ["Use 'This is' for one person or thing.", "Use 'a' before one job or role."], [("A", "Who is this?"), ("B", "This is my friend, An."), ("A", "Nice to meet you, An.")], ["I am a student.", "This is my friend.", "Nice to meet you, An."], "Choose: I am ___ student."),
    ("Family", "My Family", [("mother", "me", "This is my mother."), ("father", "bo", "This is my father."), ("sister", "chi em gai", "She is my sister."), ("brother", "anh em trai", "He is my brother."), ("family", "gia dinh", "I love my family.")], ["This is my mother.", "He is my brother.", "She is my sister."], ["Use 'he' for a boy or man.", "Use 'she' for a girl or woman."], [("A", "Who is she?"), ("B", "She is my sister."), ("A", "Is he your brother?"), ("B", "Yes, he is.")], ["This is my mother.", "He is my father.", "I love my family."], "Choose: ___ is my mother."),
    ("Colors", "Colors Around Me", [("red", "mau do", "The bag is red."), ("blue", "mau xanh duong", "My pen is blue."), ("green", "mau xanh la", "The tree is green."), ("yellow", "mau vang", "It is yellow."), ("white", "mau trang", "The board is white.")], ["It is red.", "My pen is blue.", "What color is it?"], ["Adjectives usually come before nouns.", "Use 'What color' to ask about color."], [("A", "What color is your bag?"), ("B", "It is red."), ("A", "My pen is blue.")], ["It is red.", "My pen is blue.", "What color is it?"], "What color is the sky?"),
    ("Numbers", "Numbers 1 to 20", [("one", "mot", "I have one book."), ("two", "hai", "I have two pens."), ("ten", "muoi", "There are ten desks."), ("twenty", "hai muoi", "I am twenty."), ("count", "dem", "Let's count.")], ["I have two pens.", "There are ten desks.", "How many books?"], ["Use plural -s after numbers greater than one.", "Use 'How many' to ask quantity."], [("A", "How many pens do you have?"), ("B", "I have two pens."), ("A", "Let's count together.")], ["I have two pens.", "There are ten desks.", "How many books do you have?"], "Choose: two ___"),
    ("Classroom", "Classroom Objects", [("book", "sach", "This is my book."), ("pen", "but", "I have a pen."), ("desk", "ban hoc", "The book is on the desk."), ("chair", "ghe", "Sit on the chair."), ("board", "bang", "Look at the board.")], ["This is my book.", "I have a pen.", "The book is on the desk."], ["Use 'a' for one thing.", "Use 'on' for something on top."], [("A", "Do you have a pen?"), ("B", "Yes, I have a pen."), ("A", "Put it on the desk.")], ["This is my book.", "I have a blue pen.", "The book is on the desk."], "Choose: This is ___ book."),
    ("Food", "Food I Like", [("rice", "com", "I eat rice."), ("bread", "banh mi", "I like bread."), ("egg", "trung", "I want an egg."), ("milk", "sua", "I drink milk."), ("water", "nuoc", "I want water.")], ["I like rice.", "I want water.", "Do you like bread?"], ["Use 'like' for things you enjoy.", "Use 'an' before vowel sounds like egg."], [("A", "Do you like bread?"), ("B", "Yes, I do."), ("A", "I want milk.")], ["I like rice.", "I want a cup of water.", "Do you like bread?"], "Choose: I want ___ egg."),
    ("Drinks", "Drinks and Cups", [("coffee", "ca phe", "I want coffee."), ("tea", "tra", "She drinks tea."), ("juice", "nuoc ep", "Orange juice is sweet."), ("cup", "coc", "A cup of tea, please."), ("bottle", "chai", "A bottle of water.")], ["A cup of tea, please.", "I would like juice.", "Can I have water?"], ["Use 'Can I have...' to ask politely.", "Use 'a cup of' for drinks."], [("A", "Can I have a cup of tea?"), ("B", "Yes, here you are."), ("A", "Thank you.")], ["Can I have a cup of tea?", "I would like orange juice.", "A bottle of water, please."], "Choose: a ___ of tea."),
    ("Daily Routine", "My Morning", [("wake up", "thuc day", "I wake up at six."), ("wash", "rua", "I wash my face."), ("brush", "chai", "I brush my teeth."), ("eat", "an", "I eat breakfast."), ("go", "di", "I go to school.")], ["I wake up at six.", "I brush my teeth.", "I go to school."], ["Use present simple for daily actions.", "Use 'at' with clock time."], [("A", "What do you do in the morning?"), ("B", "I brush my teeth."), ("A", "I go to school at seven.")], ["I wake up at six.", "I eat breakfast.", "I go to school at seven."], "Choose: I wake up ___ six."),
    ("Time", "Simple Time", [("o'clock", "gio dung", "It is seven o'clock."), ("morning", "sang", "I study in the morning."), ("afternoon", "chieu", "I play in the afternoon."), ("night", "dem", "Good night."), ("late", "tre", "I am late.")], ["It is seven o'clock.", "I study in the morning.", "Are you late?"], ["Use 'in the morning/afternoon'.", "Use 'at' for exact time."], [("A", "What time is it?"), ("B", "It is seven o'clock."), ("A", "Oh, I am late.")], ["It is seven o'clock.", "I study in the morning.", "I am not late."], "Choose: It is seven ___."),
    ("Shopping", "At a Small Shop", [("shop", "cua hang", "This shop is small."), ("buy", "mua", "I want to buy a pen."), ("price", "gia", "What is the price?"), ("cheap", "re", "It is cheap."), ("bag", "tui", "I need a bag.")], ["I want to buy a pen.", "How much is it?", "It is cheap."], ["Use 'How much' to ask price.", "Use 'want to' plus verb."], [("A", "How much is this pen?"), ("B", "It is ten thousand dong."), ("A", "I want to buy it.")], ["How much is this pen?", "I want to buy a bag.", "It is cheap."], "Choose: How ___ is it?"),
    ("Directions", "Go Left and Right", [("left", "trai", "Turn left."), ("right", "phai", "Turn right."), ("straight", "thang", "Go straight."), ("near", "gan", "The shop is near."), ("far", "xa", "The park is far.")], ["Turn left.", "Go straight.", "Is it near here?"], ["Use commands for directions.", "Use 'near' and 'far' after be."], [("A", "Where is the shop?"), ("B", "Go straight and turn left."), ("A", "Is it near?"), ("B", "Yes, it is.")], ["Go straight.", "Turn left.", "The shop is near here."], "Choose: Turn ___."),
    ("Restaurant", "At a Restaurant", [("menu", "thuc don", "Can I see the menu?"), ("order", "goi mon", "I want to order rice."), ("chicken", "ga", "I like chicken."), ("soup", "sup", "The soup is hot."), ("bill", "hoa don", "The bill, please.")], ["Can I see the menu?", "I would like chicken.", "The bill, please."], ["Use 'would like' to order politely.", "Use 'please' to be polite."], [("A", "Can I see the menu?"), ("B", "Yes, here you are."), ("A", "I would like chicken rice.")], ["Can I see the menu?", "I would like chicken rice.", "The bill, please."], "Choose: I ___ like chicken."),
    ("Feelings", "How I Feel", [("happy", "vui", "I am happy."), ("sad", "buon", "She is sad."), ("tired", "met", "He is tired."), ("hungry", "doi", "I am hungry."), ("thirsty", "khat", "I am thirsty.")], ["I am happy.", "Are you hungry?", "She is tired."], ["Use be + adjective for feelings.", "Ask 'Are you...?' for yes/no."], [("A", "Are you hungry?"), ("B", "Yes, I am."), ("A", "I am thirsty too.")], ["I am happy today.", "Are you hungry?", "I am tired."], "Choose: I ___ happy."),
    ("Body", "Parts of the Body", [("head", "dau", "My head hurts."), ("hand", "ban tay", "Raise your hand."), ("leg", "chan", "My leg is long."), ("eye", "mat", "I have two eyes."), ("ear", "tai", "I have two ears.")], ["I have two eyes.", "My hand hurts.", "Raise your hand."], ["Use 'have' for body parts.", "Use plural -s for two or more."], [("A", "What hurts?"), ("B", "My hand hurts."), ("A", "Please raise your hand.")], ["I have two eyes.", "My head hurts.", "Raise your hand."], "Choose: two ___."),
    ("Clothes", "What I Wear", [("shirt", "ao so mi", "I wear a shirt."), ("dress", "vay", "She wears a dress."), ("shoes", "giay", "My shoes are black."), ("hat", "mu", "This is my hat."), ("jacket", "ao khoac", "I need a jacket.")], ["I wear a shirt.", "My shoes are black.", "This is my hat."], ["Use 'wear' for clothes.", "Use 'are' with plural nouns."], [("A", "What are you wearing?"), ("B", "I am wearing a blue shirt."), ("A", "Your shoes are nice.")], ["I wear a blue shirt.", "My shoes are black.", "This is my hat."], "Choose: My shoes ___ black."),
    ("Weather", "Sunny or Rainy", [("sunny", "nang", "It is sunny."), ("rainy", "mua", "It is rainy."), ("hot", "nong", "It is hot today."), ("cold", "lanh", "It is cold."), ("windy", "gio", "It is windy.")], ["It is sunny.", "Is it cold today?", "I like rainy days."], ["Use 'It is' for weather.", "Use adjectives after be."], [("A", "How is the weather?"), ("B", "It is sunny and hot."), ("A", "I like sunny days.")], ["It is sunny today.", "It is cold at night.", "I like rainy days."], "Choose: It ___ rainy."),
    ("Animals", "Animals I Know", [("cat", "meo", "The cat is small."), ("dog", "cho", "My dog is friendly."), ("bird", "chim", "The bird can fly."), ("fish", "ca", "The fish is orange."), ("rabbit", "tho", "The rabbit is white.")], ["The cat is small.", "My dog is friendly.", "Can a bird fly?"], ["Use 'can' for ability.", "Use adjectives to describe animals."], [("A", "Do you have a pet?"), ("B", "Yes, I have a dog."), ("A", "Can it run fast?")], ["I have a small cat.", "My dog is friendly.", "A bird can fly."], "Choose: A bird can ___."),
    ("Home", "Rooms at Home", [("house", "nha", "This is my house."), ("room", "phong", "My room is small."), ("kitchen", "bep", "My mother is in the kitchen."), ("bedroom", "phong ngu", "I sleep in the bedroom."), ("bathroom", "phong tam", "The bathroom is clean.")], ["This is my house.", "My room is small.", "Where is the kitchen?"], ["Use 'in' for rooms.", "Use 'Where is' to ask location."], [("A", "Where is your mother?"), ("B", "She is in the kitchen."), ("A", "My room is small.")], ["This is my house.", "I sleep in the bedroom.", "The kitchen is clean."], "Choose: She is ___ the kitchen."),
    ("School Life", "At School", [("school", "truong hoc", "I go to school."), ("lesson", "bai hoc", "This lesson is easy."), ("homework", "bai tap ve nha", "I do homework."), ("break", "gio nghi", "We play at break."), ("test", "bai kiem tra", "I have a test.")], ["I go to school.", "I do homework.", "This lesson is easy."], ["Use present simple for routines.", "Use 'have' for tests/classes."], [("A", "Do you have homework?"), ("B", "Yes, I do."), ("A", "This lesson is easy.")], ["I go to school every day.", "I do my homework.", "This lesson is easy."], "Choose: I ___ homework."),
    ("Hobbies", "Things I Like", [("read", "doc", "I like to read."), ("draw", "ve", "She likes to draw."), ("sing", "hat", "I can sing."), ("dance", "nhay", "They dance well."), ("game", "tro choi", "I play games.")], ["I like to read.", "I can sing.", "Do you like games?"], ["Use 'like to' plus verb.", "Use 'can' plus base verb."], [("A", "What do you like to do?"), ("B", "I like to draw."), ("A", "I can sing.")], ["I like to read books.", "I can sing a song.", "Do you like games?"], "Choose: I like ___ read."),
    ("Transport", "Going Places", [("bus", "xe buyt", "I go by bus."), ("bike", "xe dap", "I ride a bike."), ("car", "xe hoi", "My father has a car."), ("walk", "di bo", "I walk to school."), ("taxi", "taxi", "Take a taxi.")], ["I go by bus.", "I walk to school.", "Do you ride a bike?"], ["Use 'by' with transport.", "Use 'to' before places."], [("A", "How do you go to school?"), ("B", "I go by bus."), ("A", "I walk to school.")], ["I go to school by bus.", "I ride a bike.", "I walk to the shop."], "Choose: I go ___ bus."),
    ("Park", "At the Park", [("park", "cong vien", "The park is big."), ("tree", "cay", "The tree is tall."), ("flower", "hoa", "The flower is red."), ("bench", "ghe dai", "Sit on the bench."), ("play", "choi", "We play in the park.")], ["The park is big.", "We play in the park.", "Sit on the bench."], ["Use 'in' for open places like park.", "Use simple commands for actions."], [("A", "Where do you play?"), ("B", "We play in the park."), ("A", "The flowers are beautiful.")], ["The park is big.", "We play in the park.", "Sit on the bench."], "Choose: We play ___ the park."),
    ("Birthday", "Happy Birthday", [("birthday", "sinh nhat", "Happy birthday!"), ("cake", "banh kem", "The cake is sweet."), ("gift", "qua", "This gift is for you."), ("party", "bua tiec", "The party is fun."), ("candle", "nen", "There are five candles.")], ["Happy birthday!", "This gift is for you.", "The cake is sweet."], ["Use 'for you' when giving something.", "Use 'There are' for plural things."], [("A", "Happy birthday!"), ("B", "Thank you."), ("A", "This gift is for you.")], ["Happy birthday!", "This gift is for you.", "The cake is sweet."], "Choose: This gift is ___ you."),
    ("Jobs", "People at Work", [("doctor", "bac si", "She is a doctor."), ("driver", "tai xe", "He is a driver."), ("cook", "dau bep", "My father is a cook."), ("farmer", "nong dan", "A farmer works on a farm."), ("worker", "cong nhan", "He is a worker.")], ["She is a doctor.", "What is his job?", "He works on a farm."], ["Use 'a/an' before one job.", "Use 'What is his/her job?'"], [("A", "What is her job?"), ("B", "She is a doctor."), ("A", "My father is a driver.")], ["She is a doctor.", "He is a driver.", "What is your job?"], "Choose: He is ___ driver."),
    ("Phone", "Simple Phone Talk", [("phone", "dien thoai", "This is my phone."), ("call", "goi", "I call my mother."), ("hello", "alo", "Hello, this is Nam."), ("wait", "doi", "Please wait."), ("busy", "ban", "I am busy now.")], ["Hello, this is Nam.", "Please wait.", "I am busy now."], ["Use 'This is...' on the phone.", "Use 'Please' for polite requests."], [("A", "Hello, this is Nam."), ("B", "Hi Nam. Is Mai there?"), ("A", "Please wait.")], ["Hello, this is Nam.", "Please wait a minute.", "I am busy now."], "Choose: Please ___."),
    ("Health", "I Feel Sick", [("sick", "om", "I feel sick."), ("fever", "sot", "I have a fever."), ("cough", "ho", "I have a cough."), ("medicine", "thuoc", "Take medicine."), ("rest", "nghi ngoi", "You should rest.")], ["I feel sick.", "I have a fever.", "You should rest."], ["Use 'have a' with illness words.", "Use 'should' for advice."], [("A", "Are you okay?"), ("B", "I feel sick."), ("A", "You should rest.")], ["I feel sick today.", "I have a cough.", "You should rest."], "Choose: I have ___ fever."),
    ("Weekend", "My Weekend", [("weekend", "cuoi tuan", "I play on the weekend."), ("visit", "tham", "I visit my grandma."), ("watch", "xem", "I watch TV."), ("clean", "don dep", "I clean my room."), ("sleep", "ngu", "I sleep late.")], ["I visit my grandma.", "I watch TV.", "What do you do on the weekend?"], ["Use 'on the weekend'.", "Use present simple for habits."], [("A", "What do you do on the weekend?"), ("B", "I visit my grandma."), ("A", "I clean my room.")], ["I visit my grandma.", "I watch TV on Sunday.", "I clean my room."], "Choose: ___ the weekend."),
    ("Review Starter", "Starter Review", [("ask", "hoi", "Ask a question."), ("answer", "tra loi", "Answer the question."), ("practice", "luyen tap", "Practice every day."), ("listen", "nghe", "Listen and repeat."), ("speak", "noi", "Speak English.")], ["I can introduce myself.", "I can ask for food.", "I can talk about my family."], ["Review: be, have, like, can, simple present.", "Speak in short clear sentences."], [("A", "What can you say in English?"), ("B", "I can introduce myself."), ("A", "Great. Keep practicing.")], ["I can introduce myself.", "I can talk about my family.", "I can order food."], "Choose: I ___ introduce myself."),
]


STARTER_TOPICS.append(
    ("Bank", "At the Bank", [("bank", "ngan hang", "The bank is near here."), ("money", "tien", "I need money."), ("card", "the", "I have a bank card."), ("account", "tai khoan", "This is my account."), ("cash", "tien mat", "I need cash.")], ["Where is the bank?", "I need cash.", "Can you help me?"], ["Use 'need' for something necessary.", "Use 'Can you...' to ask for help."], [("A", "Where is the bank?"), ("B", "It is near the shop."), ("A", "Thank you. I need cash.")], ["Where is the bank?", "I need cash.", "Can you help me, please?"], "Choose: I need cash.")
)


FLYER_TOPICS = [
    ("School Life", "A Busy School Day", [("subject", "mon hoc", "Math is my favorite subject."), ("timetable", "thoi khoa bieu", "Check the timetable."), ("library", "thu vien", "I borrow books from the library."), ("project", "du an", "We have a science project."), ("club", "cau lac bo", "I join the English club.")], ["My favorite subject is science.", "I have English on Monday.", "We are doing a project."], ["Use present continuous for actions happening now.", "Use 'favorite' before a noun."], [("A", "What is your favorite subject?"), ("B", "Science. We are doing a project."), ("A", "That sounds interesting.")], ["My favorite subject is science.", "We are doing a project.", "I join the English club."], "Choose: We ___ doing a project."),
    ("Travel", "Planning a Trip", [("trip", "chuyen di", "We are planning a trip."), ("ticket", "ve", "I need a train ticket."), ("station", "nha ga", "The station is crowded."), ("suitcase", "vali", "My suitcase is heavy."), ("map", "ban do", "Look at the map.")], ["We are going to Da Nang.", "I need a ticket.", "The station is near the hotel."], ["Use 'going to' for plans.", "Use adjectives to describe places/things."], [("A", "Where are you going?"), ("B", "We are going to Da Nang."), ("A", "Do you have your ticket?")], ["We are planning a trip.", "I need a train ticket.", "My suitcase is heavy."], "Choose: We are going ___ travel."),
    ("Weather", "Weather Forecast", [("forecast", "du bao", "The forecast says it will rain."), ("storm", "bao", "A storm is coming."), ("cloudy", "nhieu may", "It is cloudy today."), ("temperature", "nhiet do", "The temperature is low."), ("umbrella", "o", "Bring an umbrella.")], ["It will rain tomorrow.", "You should bring an umbrella.", "The temperature is high."], ["Use 'will' for weather predictions.", "Use 'should' for advice."], [("A", "What is the forecast?"), ("B", "It will rain tomorrow."), ("A", "Then I should bring an umbrella.")], ["It will rain tomorrow.", "You should bring an umbrella.", "The temperature is high today."], "Choose: It ___ rain tomorrow."),
    ("Hobbies", "Talking About Hobbies", [("collect", "suu tam", "I collect stamps."), ("practice", "luyen tap", "She practices piano."), ("competition", "cuoc thi", "He joined a competition."), ("creative", "sang tao", "Drawing is creative."), ("free time", "thoi gian ranh", "I read in my free time.")], ["I enjoy drawing.", "She is good at playing piano.", "What do you do in your free time?"], ["Use enjoy + verb-ing.", "Use good at + verb-ing."], [("A", "What do you do in your free time?"), ("B", "I enjoy drawing comics."), ("A", "Are you good at it?")], ["I enjoy drawing comics.", "She is good at playing piano.", "I read in my free time."], "Choose: I enjoy ___ books."),
    ("Phone Conversation", "Making a Phone Call", [("message", "tin nhan", "Can I leave a message?"), ("available", "co mat", "Is she available?"), ("speak", "noi chuyen", "May I speak to Tom?"), ("hold on", "cho may", "Please hold on."), ("call back", "goi lai", "I will call back later.")], ["May I speak to Tom?", "Can I leave a message?", "I will call back later."], ["Use 'May I...' for polite requests.", "Use 'will' for quick decisions."], [("A", "May I speak to Tom?"), ("B", "He is not available."), ("A", "Can I leave a message?")], ["May I speak to Tom?", "Can I leave a message?", "I will call back later."], "Choose: May I ___ to Tom?"),
    ("Ordering Food", "Ordering at a Cafe", [("recommend", "goi y", "What do you recommend?"), ("medium", "vua", "A medium coffee, please."), ("without", "khong co", "Tea without sugar."), ("takeaway", "mang di", "It is for takeaway."), ("receipt", "hoa don", "Can I have a receipt?")], ["What do you recommend?", "I would like a medium coffee.", "Can I have it without sugar?"], ["Use 'would like' for polite orders.", "Use 'without' to remove something."], [("A", "What do you recommend?"), ("B", "The chicken sandwich is good."), ("A", "I would like one, please.")], ["I would like a medium coffee.", "Can I have it without sugar?", "It is for takeaway."], "Choose: coffee ___ sugar."),
    ("Problem Solving", "Solving a Small Problem", [("problem", "van de", "We have a problem."), ("solution", "giai phap", "Let's find a solution."), ("broken", "hong", "The printer is broken."), ("fix", "sua", "Can you fix it?"), ("helpful", "co ich", "That is helpful.")], ["We have a problem.", "Can you help me fix it?", "Let's try another solution."], ["Use 'Let's' to suggest action.", "Use 'Can you...' to request help."], [("A", "The printer is broken."), ("B", "Let's ask the teacher for help."), ("A", "Good idea.")], ["We have a problem.", "Can you help me fix it?", "Let's try another solution."], "Choose: Let's ___ a solution."),
    ("Directions", "Finding a Place", [("corner", "goc pho", "Turn at the corner."), ("opposite", "doi dien", "The bank is opposite the park."), ("next to", "ke ben", "The shop is next to the cafe."), ("traffic light", "den giao thong", "Stop at the traffic light."), ("cross", "bang qua", "Cross the street carefully.")], ["The bank is opposite the park.", "Turn right at the traffic light.", "It is next to the cafe."], ["Use prepositions of place.", "Use imperatives for directions."], [("A", "Excuse me, where is the bank?"), ("B", "It is opposite the park."), ("A", "Do I turn right?")], ["The bank is opposite the park.", "Turn right at the traffic light.", "Cross the street carefully."], "Choose: opposite ___ park."),
    ("Health Advice", "At the Clinic", [("appointment", "cuoc hen", "I have an appointment."), ("headache", "dau dau", "I have a headache."), ("sore throat", "dau hong", "She has a sore throat."), ("temperature", "nhiet do", "Take your temperature."), ("advice", "loi khuyen", "The doctor gave advice.")], ["I have had a headache since yesterday.", "You should drink warm water.", "I need an appointment."], ["Use present perfect with since/for.", "Use should/shouldn't for advice."], [("A", "What is the problem?"), ("B", "I have had a headache since yesterday."), ("A", "You should rest.")], ["I have an appointment.", "I have had a headache since yesterday.", "You should drink warm water."], "Choose: since ___."),
    ("Shopping Choices", "Choosing a Gift", [("expensive", "dat", "This bag is expensive."), ("discount", "giam gia", "There is a discount."), ("size", "kich co", "What size do you need?"), ("try on", "thu do", "Can I try it on?"), ("receipt", "hoa don", "Keep the receipt.")], ["Can I try it on?", "Do you have a smaller size?", "It is too expensive."], ["Use too + adjective.", "Use comparative adjectives like smaller."], [("A", "Can I try this jacket on?"), ("B", "Sure. What size do you need?"), ("A", "Do you have a smaller size?")], ["Can I try it on?", "It is too expensive.", "Do you have a smaller size?"], "Choose: too ___."),
]

FLYER_TOPICS += [
    ("Airport", "At the Airport"), ("Hotel", "Checking In"), ("Lost Item", "I Lost My Bag"), ("Sports", "After the Match"),
    ("Music", "My Favorite Song"), ("Movies", "Going to the Cinema"), ("Environment", "Keeping the Park Clean"),
    ("Online Class", "Joining an Online Lesson"), ("Invitation", "Inviting a Friend"), ("Apology", "Saying Sorry"),
    ("Past Weekend", "What I Did Last Weekend"), ("Future Plans", "Plans for Next Month"), ("Comparisons", "Bigger and Better"),
    ("Storytelling", "A Short Story"), ("Email", "Writing a Simple Email"), ("Safety", "Safety Rules"),
    ("Museum", "At the Museum"), ("Library", "Borrowing a Book"), ("Volunteer", "Helping Others"), ("Flyer Review", "Flyer Review Challenge"),
]


def _expand_flyer_topic(item, idx):
    if len(item) > 2:
        return item
    topic, title = item
    key = topic.lower()
    words = [
        (key.split()[0], topic.lower(), f"I can talk about {topic.lower()}."),
        ("plan", "ke hoach", f"We need a plan for {topic.lower()}."),
        ("important", "quan trong", "This is important."),
        ("carefully", "can than", "Please listen carefully."),
        ("question", "cau hoi", "I have a question."),
    ]
    return (
        topic,
        title,
        words,
        [f"I can talk about {topic.lower()}.", "Could you help me, please?", "I think this is a good idea."],
        ["Use 'could' for polite requests.", "Use 'think' to give an opinion."],
        [("A", f"Can you help me with {topic.lower()}?"), ("B", "Sure. What do you need?"), ("A", "I have a question.")],
        [f"I can talk about {topic.lower()}.", "Could you help me, please?", "I think this is a good idea."],
        "Choose the polite request.",
    )


def _quiz(prompt, answer):
    return [
        {"question": prompt, "options": [answer, "wrong", "not sure"], "answer": answer},
        {"question": "Choose the polite sentence.", "options": ["Give me it.", "Could you help me, please?", "No help."], "answer": "Could you help me, please?"},
    ]


def _quiz_from_prompt(prompt):
    if "||" in prompt:
        question, answer = prompt.split("||", 1)
        return _quiz(question.strip(), answer.strip())
    return _quiz(prompt, prompt.split(":")[-1].strip() if ":" in prompt else "Could you help me, please?")


def _build_units(level_id, level_title, specs):
    units = []
    unit_count = (len(specs) + 4) // 5
    for unit_idx in range(unit_count):
        unit_id = f"{level_id}_u{unit_idx + 1}"
        group = specs[unit_idx * 5:(unit_idx + 1) * 5]
        if not group:
            continue
        same_topic_group = all(spec[0] == group[0][0] for spec in group)
        unit_topic_title = group[0][0] if same_topic_group else f"{level_title} Practice {unit_idx + 1}"
        unit_description = (
            f"Five skill lessons for {unit_topic_title}: vocabulary, grammar, listening, reading and writing."
            if same_topic_group
            else f"Five real-life {level_title} lessons with vocabulary, dialogue, speaking and quiz."
        )
        units.append({
            "id": unit_id,
            "levelId": level_id,
            "title": f"Unit {unit_idx + 1}: {unit_topic_title}",
            "description": unit_description,
            "order": unit_idx + 1,
            "lessons": [
                _integrated_lesson(
                    level_id,
                    unit_id,
                    lesson_idx + 1,
                    spec[1],
                    spec[0],
                    spec[2],
                    spec[3],
                    spec[4],
                    spec[5],
                    spec[6],
                    _quiz_from_prompt(spec[7]),
                    spec[8] if len(spec) > 8 else None,
                )
                for lesson_idx, spec in enumerate(group)
            ],
        })
    return units


STARTER_EXTRA_TOPICS = [
    "Personal Information", "My Address", "My Favorite Things", "My Best Friend", "My School Bag",
    "At the Market", "Fruit and Vegetables", "Breakfast Time", "After School", "Bedtime Routine",
    "My Neighborhood", "At the Bus Stop", "In the Playground", "At the Bookstore", "At the Pharmacy",
    "Simple Questions", "Yes and No Answers", "Asking Permission", "Saying Thank You", "Saying Sorry",
    "Small Talk", "Daily Chores", "Weekend Visit", "Simple Review 1", "Simple Review 2",
]


def _starter_extra_topic_spec(topic, idx):
    key = topic.lower()
    topic_word = key.split()[0]
    word_pool = [
        ("address", "dia chi"), ("favorite", "yeu thich"), ("market", "cho"), ("breakfast", "bua sang"),
        ("neighborhood", "khu pho"), ("bus stop", "tram xe buyt"), ("permission", "xin phep"),
        ("thank you", "cam on"), ("sorry", "xin loi"), ("chores", "viec nha"),
    ]
    selected = [(topic_word, key)] + [word_pool[(idx + offset) % len(word_pool)] for offset in range(4)]
    words = [
        (selected[0][0], selected[0][1], f"This lesson is about {key}."),
        (selected[1][0], selected[1][1], f"I can say something about {key}."),
        (selected[2][0], selected[2][1], "This word is useful every day."),
        (selected[3][0], selected[3][1], "Please repeat this word."),
        (selected[4][0], selected[4][1], "I can use this word in a sentence."),
    ]
    patterns = [f"I can talk about {key}.", "Can I ask a question?", "Thank you for helping me."]
    grammar = ["Use short present simple sentences.", "Use can for simple ability and permission."]
    dialogue = [("A", f"Can you talk about {key}?"), ("B", "Yes, I can say a short sentence."), ("A", "Good. Please repeat it.")]
    speaking = [f"I can talk about {key}.", "Can I ask a question?", "Thank you for helping me."]
    return (topic, topic, words, patterns, grammar, dialogue, speaking, "Choose a polite sentence.||Can I ask a question?")


STARTER_TOPICS += [_starter_extra_topic_spec(topic, idx) for idx, topic in enumerate(STARTER_EXTRA_TOPICS)]


def _starter_topic_series(actions, contexts, limit):
    topics = []
    for context in contexts:
        for action in actions:
            topics.append(f"{action} {context}")
            if len(topics) >= limit:
                return topics
    return topics


STARTER_TOPICS += [
    _starter_extra_topic_spec(topic, idx + len(STARTER_EXTRA_TOPICS))
    for idx, topic in enumerate(_starter_topic_series(
        ["Talking About", "Asking About", "Practicing", "Reviewing", "Using"],
        [
            "My Day", "My Family", "My Class", "Food and Drinks", "Colors and Numbers",
            "Home and Rooms", "School and Friends", "Shopping Words", "Travel Words",
        ],
        45,
    ))
]


STARTER_TOPICS += [
    _starter_extra_topic_spec(topic, idx + len(STARTER_EXTRA_TOPICS) + 45)
    for idx, topic in enumerate(_starter_topic_series(
        ["Learning", "Listening To", "Speaking About", "Writing About", "Reviewing"],
        ["My Morning", "My Lunch", "My Street", "My Weekend", "My English Class"],
        25,
    ))
]


STARTER_TOPICS += [
    _starter_extra_topic_spec(topic, idx + len(STARTER_EXTRA_TOPICS) + 70)
    for idx, topic in enumerate(_starter_topic_series(
        ["Learning", "Asking About", "Practicing", "Speaking About", "Reviewing"],
        [
            "My Clothes", "My Pets", "My Birthday", "My Favorite Food", "My Favorite Drink",
            "My House", "My Bedroom", "My School Day", "My Teacher", "My Friend",
            "At the Park", "At the Shop", "At the Restaurant", "At the Clinic", "At the Bank",
            "Going by Bus", "Going by Taxi", "Going by Bike", "Simple Weather", "Simple Jobs",
            "Simple Phone Calls", "Simple Questions", "Simple Answers", "Everyday English", "Starter Final Skills",
        ],
        125,
    ))
]


FLYER_TOPICS += [
    ("Science Fair", "At the Science Fair"), ("Camping Trip", "Going Camping"), ("Saving Money", "Saving Pocket Money"),
    ("Team Project", "Working in a Team"), ("Class Debate", "Giving a Simple Opinion"),
    ("Lost Direction", "Finding the Right Way"), ("Train Delay", "The Train Is Late"), ("Online Game", "Playing Online Safely"),
    ("Pet Care", "Taking Care of a Pet"), ("Healthy Lunch", "Choosing a Healthy Lunch"),
    ("School Rules", "Talking About Rules"), ("New Student", "Helping a New Student"), ("Birthday Invitation", "Planning a Party"),
    ("Holiday Plan", "Planning a Holiday"), ("Photo Description", "Describing a Photo"),
    ("Book Report", "Talking About a Book"), ("Simple News", "Telling Simple News"), ("Class Survey", "Asking Survey Questions"),
    ("Lost Password", "Fixing a Password Problem"), ("Video Call", "Joining a Video Call"),
    ("Helping at Home", "Helping at Home"), ("Town Festival", "At a Town Festival"), ("Travel Problem", "A Travel Problem"),
    ("Flyer Skills Review", "Flyer Skills Review"), ("Flyer Speaking Review", "Flyer Speaking Review"),
]


def _flyer_topic_series(skills, contexts, limit):
    topics = []
    for context in contexts:
        for skill in skills:
            topics.append((f"{skill} {context}", f"{skill} {context}"))
            if len(topics) >= limit:
                return topics
    return topics


FLYER_TOPICS += _flyer_topic_series(
    ["Explaining", "Comparing", "Planning", "Solving", "Reviewing"],
    [
        "School Life", "Travel Plans", "Weather Problems", "Hobbies and Clubs", "Phone Messages",
        "Food Orders", "Town Directions", "Health Advice", "Shopping Choices",
    ],
    45,
)


FLYER_TOPICS += _flyer_topic_series(
    ["Practicing", "Discussing", "Writing About", "Listening For", "Reviewing"],
    ["Travel Stories", "School Projects", "Shopping Problems", "Health Choices", "Town Activities"],
    25,
)


FLYER_TOPICS += _flyer_topic_series(
    ["Practicing", "Explaining", "Comparing", "Solving", "Reviewing"],
    [
        "Airport Problems", "Hotel Services", "Lost Items", "Sports Events", "Music Classes",
        "Movie Plans", "Environment Projects", "Online Lessons", "Party Invitations", "Apology Messages",
        "Past Weekend Stories", "Future Plans", "Comparisons", "Short Stories", "Simple Emails",
        "Safety Rules", "Museum Visits", "Library Tasks", "Volunteer Work", "Travel Questions",
        "Class Presentations", "Friendly Debates", "Daily News", "Speaking Tests", "Flyer Final Skills",
    ],
    125,
)


ROADMAP_UNITS = (
    _build_units("starter", "Starter", STARTER_TOPICS)
    + _build_units("flyer", "Flyer", [_expand_flyer_topic(item, idx) for idx, item in enumerate(FLYER_TOPICS)])
)


ADVANCED_LEVEL_TOPICS = {
    "ket": [
        "Daily Schedule", "Buying a Ticket", "Writing a Note", "Asking for Directions", "Making an Appointment",
        "Lost Property", "Weekend Activities", "Simple Email", "Public Transport", "At the Doctor",
        "School Notice", "Inviting a Friend", "Changing Plans", "Shopping Online", "At the Train Station",
        "Weather Plans", "Sports Club", "Library Card", "Hotel Question", "Phone Message",
        "Food Order", "Class Timetable", "Town Map", "Holiday Photo", "KET Review",
    ],
    "pet": [
        "Giving Opinions", "Solving a Problem", "Past Experience", "Future Arrangement", "Story Details",
        "Making Suggestions", "Agreeing Politely", "Describing Photos", "Community Event", "Study Advice",
        "Comparing Options", "Explaining Reasons", "Making Complaints", "Travel Story", "Healthy Habits",
        "Online Learning", "Volunteer Work", "Film Review", "City Changes", "Interview Practice",
        "Advice Letter", "Group Project", "Environmental Choice", "Personal Achievement", "PET Review",
    ],
    "ielts_foundation": [
        "Daily Routine", "Work and Study", "Home Town", "Food Topic", "Travel Topic",
        "Education Topic", "Technology Topic", "Environment Topic", "Opinion Paragraph", "Speaking Part 1",
        "Family Topic", "Hobbies Topic", "Health Topic", "Shopping Topic", "Transport Topic",
        "Culture Topic", "City Life", "Rural Life", "Simple Essay", "Task Response",
        "Vocabulary Range", "Grammar Accuracy", "Pronunciation Basics", "Fluency Basics", "IELTS Foundation Review",
    ],
    "ielts_50": [
        "Clear Opinion", "Main Idea", "Supporting Example", "Compare Advantages", "Describe a Chart",
        "Speaking Cue Card", "Linking Ideas", "Cause and Effect", "Problem Solution", "Conclusion Practice",
        "Task 1 Overview", "Task 2 Introduction", "Paraphrasing Question", "Explaining Trends", "Giving Examples",
        "Two-sided Essay", "Agree Disagree Essay", "Part 3 Answer", "Long Turn Notes", "Common Mistakes",
        "Coherence Practice", "Lexical Resource", "Grammar Range", "Pronunciation Control", "IELTS 5 Review",
    ],
    "ielts_65": [
        "Advanced Opinion", "Balanced Argument", "Complex Sentences", "Academic Vocabulary", "Data Summary",
        "Coherence Practice", "Abstract Topic", "Fluency Builder", "Paraphrasing", "Band 6.5 Review",
        "Counter Argument", "Concession Language", "Trend Comparison", "Process Description", "Map Description",
        "Nuanced Opinion", "Evidence and Logic", "Collocation Upgrade", "Error Reduction", "Natural Speaking",
        "Extended Answer", "Debate Practice", "Formal Tone", "Essay Cohesion", "IELTS 6.5 Final Review",
    ],
    "business": [
        "Meeting Update", "Reschedule a Call", "Client Email", "Project Deadline", "Presentation Opening",
        "Negotiation Basics", "Follow-up Message", "Work Problem", "Team Feedback", "Business Review",
        "Status Report", "Budget Question", "Customer Update", "Action Items", "Polite Reminder",
        "Small Talk at Work", "Deadline Risk", "Product Demo", "Manager Check-in", "Remote Meeting",
        "Clarifying Tasks", "Business Apology", "Proposal Summary", "Decision Making", "Business Final Review",
    ],
    "sales": [
        "Greeting a Customer", "Finding Needs", "Product Benefits", "Price Discussion", "Handling Objections",
        "Closing a Sale", "Follow-up Call", "Customer Complaint", "Promotion Offer", "Sales Review",
        "Qualifying Lead", "Explaining Features", "Comparing Packages", "Discount Request", "Building Trust",
        "After-sales Support", "Upsell Offer", "Renewal Reminder", "Delivery Question", "Service Recovery",
        "Cold Call Opening", "Demo Booking", "Pain Point", "Value Proposition", "Sales Final Review",
    ],
    "cafe": [
        "Taking an Order", "Recommending Drinks", "No Sugar Request", "Takeaway Order", "Apologizing to Customer",
        "Payment at Counter", "Busy Cafe", "Wrong Order", "Friendly Service", "Cafe Review",
        "Breakfast Combo", "Allergy Question", "Table Service", "Queue Management", "Loyalty Card",
        "Out of Stock", "Cleaning Table", "Special Request", "Receipt Request", "Customer Feedback",
        "Opening Shift", "Closing Shift", "New Menu Item", "Upselling Cake", "Cafe Final Review",
    ],
    "factory": [
        "Safety Instruction", "Shift Handover", "Machine Problem", "Ask a Supervisor", "Report an Issue",
        "Protective Equipment", "Quality Check", "Work Schedule", "Emergency Phrase", "Factory Review",
        "Tool Request", "Production Target", "Material Shortage", "Maintenance Call", "Break Time",
        "Incident Report", "Training Step", "Assembly Line", "Warehouse Location", "Delivery Delay",
        "Checklist Review", "Noise Warning", "Temperature Check", "Team Briefing", "Factory Final Review",
    ],
}

ADVANCED_LEVEL_TOPICS["ket"] += [
    "Doctor Appointment", "School Trip Form", "Changing a Ticket", "At the Post Office", "Simple Complaint",
    "Museum Opening Hours", "Sports Practice", "Bus Information", "New Classmate", "Lost Key",
    "Cafe Meeting", "Cinema Time", "Park Rules", "Buying Clothes", "Asking the Price",
    "Email to Teacher", "Weekend Invitation", "City Transport", "Simple Notice Reply", "Holiday Booking",
    "Family Visit", "After-school Club", "Short Story Message", "Daily Life Review", "KET Speaking Review",
]

ADVANCED_LEVEL_TOPICS["pet"] += [
    "School Uniform Debate", "Social Media Opinion", "Part-time Job", "Sports Competition", "Unexpected Problem",
    "Giving Advice to a Friend", "Comparing Two Photos", "Planning a Class Event", "Writing a Review", "Explaining a Mistake",
    "Travel Delay Story", "Healthy Lifestyle Choice", "Online Safety", "Local Community Problem", "Choosing a Course",
    "Describing a Memory", "Polite Disagreement", "Making a Recommendation", "Discussing Rules", "Future Career Plan",
    "Helping a Visitor", "Sharing Good News", "Solving Team Conflict", "PET Writing Review", "PET Speaking Review",
]

ADVANCED_LEVEL_TOPICS["ielts_foundation"] += [
    "Friends Topic", "Sports Topic", "Music Topic", "Books Topic", "Money Topic",
    "Public Transport", "Learning Languages", "Social Media", "Daily Technology", "Simple Graph",
    "Agree or Disagree", "Advantages Topic", "Disadvantages Topic", "Giving Reasons", "Adding Details",
    "Part 2 Story", "Describing a Person", "Describing a Place", "Describing an Object", "Simple Comparison",
    "Common Grammar Errors", "Topic Vocabulary Review", "Speaking Confidence", "Writing Basics Review", "IELTS Starter Review",
]

ADVANCED_LEVEL_TOPICS["ielts_50"] += [
    "Opinion Development", "Body Paragraph One", "Body Paragraph Two", "Chart Introduction", "Line Graph Trends",
    "Bar Chart Comparison", "Pie Chart Summary", "Map Vocabulary", "Process Vocabulary", "Cause Paragraph",
    "Solution Paragraph", "Discussion Essay", "Direct Question Essay", "Speaking Part 1 Details", "Speaking Part 2 Structure",
    "Speaking Part 3 Reasons", "Example Expansion", "Avoiding Repetition", "Grammar Accuracy Check", "Vocabulary Upgrade",
    "Clear Pronunciation", "Fluency Practice", "Writing Time Management", "IELTS 5 Writing Review", "IELTS 5 Speaking Review",
]

ADVANCED_LEVEL_TOPICS["ielts_65"] += [
    "Sophisticated Examples", "Evaluating Evidence", "Concession Paragraph", "Advanced Linking", "Nominalisation",
    "Complex Comparison", "Trend Precision", "Cautious Language", "High-level Paraphrase", "Cohesive Referencing",
    "Mixed Chart Response", "Advanced Process Report", "Map Change Description", "Abstract Discussion", "Policy Argument",
    "Society and Culture", "Technology Ethics", "Education Reform", "Environment Policy", "Workplace Change",
    "Speaking Nuance", "Stress and Intonation", "Error Correction Strategy", "Band 6.5 Writing Review", "Band 6.5 Speaking Review",
]

ADVANCED_LEVEL_TOPICS["business"] += [
    "Meeting Agenda", "Taking Minutes", "Confirming Details", "Requesting Approval", "Reporting Progress",
    "Project Risk", "Client Complaint", "Service Apology", "Negotiating Price", "Clarifying Scope",
    "Team Handover", "Performance Feedback", "Training Session", "Product Launch", "Sales Forecast",
    "Supplier Email", "Invoice Question", "Contract Summary", "Remote Work Update", "Urgent Deadline",
    "Presentation Q and A", "Executive Summary", "Decision Follow-up", "Business Email Review", "Business Speaking Review",
]

ADVANCED_LEVEL_TOPICS["sales"] += [
    "First Customer Contact", "Discovering Budget", "Matching Needs", "Explaining Packages", "Handling Price Concern",
    "Competitor Comparison", "Creating Urgency", "Building Rapport", "Asking for Decision", "Confirming Order",
    "Payment Terms", "Delivery Timeline", "Customer Follow-up", "Referral Request", "Loyalty Offer",
    "Service Upgrade", "Complaint Recovery", "Warranty Explanation", "Product Demonstration", "Negotiating Discount",
    "Closing Script", "Phone Sales Practice", "Sales Email Practice", "Sales Objection Review", "Sales Speaking Review",
]

ADVANCED_LEVEL_TOPICS["cafe"] += [
    "Greeting Regular Guests", "Explaining the Menu", "Coffee Strength", "Milk Options", "Food Allergy",
    "No Ice Request", "Changing an Order", "Table Reservation", "Large Group Order", "Handling a Queue",
    "Card Payment Problem", "Refund Request", "Late Order Apology", "Recommending Dessert", "Cleaning Spill",
    "Drive-through Order", "Delivery Order", "Customer Complaint", "Daily Special", "Stock Shortage",
    "Training New Staff", "Shift Handover", "Cafe Phone Call", "Cafe Service Review", "Cafe Speaking Review",
]

ADVANCED_LEVEL_TOPICS["factory"] += [
    "Morning Safety Briefing", "Reporting Late Arrival", "Checking Materials", "Machine Start-up", "Machine Shutdown",
    "Quality Defect", "Asking for Tools", "Reporting Low Stock", "Forklift Safety", "Warehouse Instruction",
    "Line Leader Update", "Production Delay", "Overtime Request", "Changing Shifts", "PPE Reminder",
    "Fire Drill", "First Aid Request", "Maintenance Schedule", "Packing Instruction", "Loading Area",
    "Supervisor Feedback", "Training Checklist", "Incident Follow-up", "Factory Safety Review", "Factory Speaking Review",
]


ADVANCED_EXPANSION_BLUEPRINTS = {
    "ket": {
        "skills": ["Asking About", "Changing", "Confirming", "Explaining", "Reviewing"],
        "contexts": [
            "Bank Visit", "Tourist Office", "School Office", "Local Event", "Sports Centre",
            "Train Journey", "Hotel Booking", "Online Order", "Doctor Visit", "KET Communication",
        ],
    },
    "pet": {
        "skills": ["Giving Opinions On", "Comparing", "Solving", "Describing", "Reviewing"],
        "contexts": [
            "School Rules", "Online Habits", "Community Events", "Travel Choices", "Healthy Living",
            "Team Projects", "Personal Goals", "Local Problems", "Photo Stories", "PET Communication",
        ],
    },
    "ielts_foundation": {
        "skills": ["Building Ideas For", "Giving Reasons For", "Adding Examples About", "Speaking About", "Reviewing"],
        "contexts": [
            "Work and Study", "Hometown Topics", "Health and Sport", "Technology Use", "Family Life",
            "Education Topics", "Travel Topics", "Environment Topics", "Culture Topics", "IELTS Foundation",
        ],
    },
    "ielts_50": {
        "skills": ["Developing", "Linking", "Explaining", "Improving", "Reviewing"],
        "contexts": [
            "Opinion Essays", "Chart Reports", "Problem Solutions", "Discussion Essays", "Speaking Part 2",
            "Speaking Part 3", "Task 1 Overviews", "Examples and Support", "Grammar Range", "IELTS 5 Skills",
        ],
    },
    "ielts_65": {
        "skills": ["Refining", "Balancing", "Evaluating", "Upgrading", "Reviewing"],
        "contexts": [
            "Academic Arguments", "Complex Data", "Policy Topics", "Abstract Ideas", "Cohesion",
            "Lexical Precision", "Advanced Speaking", "Error Control", "Formal Tone", "IELTS 6.5 Skills",
        ],
    },
    "business": {
        "skills": ["Discussing", "Writing About", "Following Up On", "Negotiating", "Reviewing"],
        "contexts": [
            "Meetings", "Client Emails", "Project Updates", "Budget Issues", "Team Feedback",
            "Deadlines", "Presentations", "Contracts", "Remote Work", "Business Communication",
        ],
    },
    "sales": {
        "skills": ["Opening", "Explaining", "Handling", "Closing", "Reviewing"],
        "contexts": [
            "Customer Calls", "Product Benefits", "Price Objections", "Package Comparisons", "Follow-up Messages",
            "Demo Bookings", "Discount Requests", "Renewals", "Complaints", "Sales Conversations",
        ],
    },
    "cafe": {
        "skills": ["Taking", "Explaining", "Handling", "Recommending", "Reviewing"],
        "contexts": [
            "Drink Orders", "Food Allergies", "Payment Problems", "Busy Queues", "Menu Questions",
            "Takeaway Orders", "Table Service", "Customer Complaints", "Shift Handover", "Cafe Service",
        ],
    },
    "factory": {
        "skills": ["Reporting", "Checking", "Explaining", "Following", "Reviewing"],
        "contexts": [
            "Safety Rules", "Machine Issues", "Quality Problems", "Shift Changes", "Tool Requests",
            "Warehouse Tasks", "Production Targets", "Maintenance Calls", "Emergency Steps", "Factory Communication",
        ],
    },
}


def _advanced_topic_series(level_id, limit=50):
    blueprint = ADVANCED_EXPANSION_BLUEPRINTS[level_id]
    topics = []
    for context in blueprint["contexts"]:
        for skill in blueprint["skills"]:
            topics.append(f"{skill} {context}")
            if len(topics) >= limit:
                return topics
    return topics


for _level_id in ADVANCED_EXPANSION_BLUEPRINTS:
    ADVANCED_LEVEL_TOPICS[_level_id] += _advanced_topic_series(_level_id)


ADVANCED_EXTRA_CONTEXTS = {
    "ket": ["Community Centre", "Simple Travel Plan", "Everyday Shopping", "Short Email Practice", "KET Final Skills"],
    "pet": ["Teenage Life", "School Events", "Local Services", "Personal Experiences", "PET Final Skills"],
    "ielts_foundation": ["Everyday Topics", "Basic Essay Ideas", "Speaking Warmups", "Simple Task Practice", "IELTS Foundation Final"],
    "ielts_50": ["Task 2 Planning", "Task 1 Accuracy", "Speaking Expansion", "Vocabulary Control", "IELTS 5 Final Skills"],
    "ielts_65": ["Advanced Essay Control", "High Band Task 1", "Critical Thinking", "Natural Fluency", "IELTS 6.5 Final Skills"],
    "business": ["Workplace Requests", "Client Communication", "Team Decisions", "Presentation Practice", "Business Final Skills"],
    "sales": ["Lead Qualification", "Customer Trust", "Package Offers", "Service Follow-up", "Sales Final Skills"],
    "cafe": ["Counter Service", "Menu Advice", "Guest Problems", "Shift Communication", "Cafe Final Skills"],
    "factory": ["Daily Operations", "Safety Communication", "Production Issues", "Supervisor Updates", "Factory Final Skills"],
}


for _level_id, _contexts in ADVANCED_EXTRA_CONTEXTS.items():
    _skills = ADVANCED_EXPANSION_BLUEPRINTS[_level_id]["skills"]
    ADVANCED_LEVEL_TOPICS[_level_id] += [
        f"{skill} {context}"
        for context in _contexts
        for skill in _skills
    ]


ADVANCED_DEEP_CONTEXTS = {
    "ket": [
        "Daily Routines", "Travel Information", "Shopping Help", "School Messages", "Health Questions",
        "Public Notices", "Weekend Plans", "Transport Problems", "Booking Details", "Local Services",
        "Simple Emails", "Phone Messages", "Town Facilities", "Invitations", "Lost Property",
        "Ticket Changes", "Food Orders", "Weather Plans", "Short Forms", "KET Listening Skills",
        "KET Reading Skills", "KET Writing Skills", "KET Speaking Skills", "KET Review Tasks", "KET Final Practice",
    ],
    "pet": [
        "Personal Opinions", "School Life", "Travel Experiences", "Healthy Choices", "Online Communication",
        "Community Problems", "Photo Descriptions", "Story Development", "Advice Messages", "Reviews",
        "Future Plans", "Past Events", "Comparing Options", "Making Suggestions", "Polite Disagreement",
        "Environmental Issues", "Volunteer Projects", "Teenage Problems", "Study Skills", "PET Listening Skills",
        "PET Reading Skills", "PET Writing Skills", "PET Speaking Skills", "PET Review Tasks", "PET Final Practice",
    ],
    "ielts_foundation": [
        "People Topics", "Place Topics", "Object Topics", "Habit Topics", "Study Topics",
        "Work Topics", "Technology Topics", "Health Topics", "Sport Topics", "Culture Topics",
        "Travel Topics", "Environment Topics", "Money Topics", "Media Topics", "Family Topics",
        "Simple Opinion Essays", "Simple Task 1 Reports", "Speaking Part 1", "Speaking Part 2", "Speaking Part 3",
        "Vocabulary Review", "Grammar Review", "Pronunciation Review", "Writing Review", "Foundation Final Practice",
    ],
    "ielts_50": [
        "Opinion Paragraphs", "Discussion Essays", "Problem Solution Essays", "Advantages Essays", "Cause Effect Essays",
        "Line Graphs", "Bar Charts", "Pie Charts", "Tables", "Maps",
        "Processes", "Overview Sentences", "Trend Language", "Comparison Language", "Example Support",
        "Speaking Part 1", "Speaking Part 2", "Speaking Part 3", "Fluency Control", "Grammar Control",
        "Vocabulary Control", "Coherence Control", "Task Response", "Timing Strategy", "IELTS 5 Final Practice",
    ],
    "ielts_65": [
        "Advanced Arguments", "Balanced Views", "Concession Clauses", "Evidence Evaluation", "Policy Topics",
        "Social Issues", "Technology Ethics", "Education Reform", "Environmental Policy", "Work Trends",
        "Complex Charts", "Mixed Data", "Process Reports", "Map Reports", "Precise Overviews",
        "Advanced Paraphrasing", "Cohesion Devices", "Lexical Precision", "Complex Grammar", "Natural Fluency",
        "Pronunciation Control", "Speaking Nuance", "Writing Review", "Speaking Review", "IELTS 6.5 Final Practice",
    ],
    "business": [
        "Meeting Preparation", "Meeting Follow-up", "Client Updates", "Project Deadlines", "Budget Discussions",
        "Proposal Writing", "Contract Questions", "Supplier Messages", "Team Feedback", "Performance Reviews",
        "Remote Meetings", "Presentation Openings", "Presentation Q and A", "Negotiation Points", "Decision Emails",
        "Status Reports", "Risk Reports", "Apology Emails", "Polite Reminders", "Action Items",
        "Manager Check-ins", "Customer Updates", "Training Sessions", "Business Review", "Business Final Practice",
    ],
    "sales": [
        "Customer Greetings", "Need Discovery", "Budget Questions", "Product Benefits", "Package Comparison",
        "Price Objections", "Discount Negotiation", "Trust Building", "Demo Booking", "Follow-up Calls",
        "Closing Questions", "Payment Terms", "Delivery Details", "Warranty Questions", "Complaint Recovery",
        "Renewal Offers", "Upsell Offers", "Referral Requests", "Sales Emails", "Phone Sales",
        "Objection Review", "Value Review", "Customer Service", "Sales Review", "Sales Final Practice",
    ],
    "cafe": [
        "Guest Greetings", "Menu Explanations", "Drink Recommendations", "Milk Options", "Sugar Options",
        "Allergy Questions", "Takeaway Orders", "Table Service", "Queue Handling", "Payment Problems",
        "Refund Requests", "Wrong Orders", "Late Orders", "Customer Apologies", "Dessert Offers",
        "Daily Specials", "Stock Problems", "Large Orders", "Phone Orders", "Delivery Orders",
        "Shift Handover", "Staff Training", "Customer Feedback", "Cafe Review", "Cafe Final Practice",
    ],
    "factory": [
        "Safety Briefings", "PPE Checks", "Machine Start-up", "Machine Problems", "Quality Defects",
        "Material Shortage", "Tool Requests", "Warehouse Tasks", "Shift Handover", "Overtime Requests",
        "Supervisor Updates", "Production Targets", "Maintenance Calls", "Incident Reports", "First Aid Requests",
        "Fire Drill Steps", "Packing Instructions", "Loading Area Tasks", "Delivery Delays", "Training Checklists",
        "Noise Warnings", "Temperature Checks", "Team Briefings", "Factory Review", "Factory Final Practice",
    ],
}


for _level_id, _contexts in ADVANCED_DEEP_CONTEXTS.items():
    _skills = ADVANCED_EXPANSION_BLUEPRINTS[_level_id]["skills"]
    ADVANCED_LEVEL_TOPICS[_level_id] += [
        f"{skill} {context}"
        for context in _contexts
        for skill in _skills
    ]


LEVEL_CONTENT_PROFILES = {
    "ket": {
        "words": [("schedule", "lich trinh"), ("ticket", "ve"), ("notice", "thong bao"), ("form", "mau don"), ("station", "nha ga"), ("appointment", "cuoc hen"), ("message", "tin nhan"), ("direction", "chi duong")],
        "patterns": ["I need information about {topic}.", "Could you tell me the time?", "I would like to change my plan."],
        "grammar": ["Use polite requests with could/would.", "Use present simple for timetables and routines."],
        "dialogue": [("A", "Excuse me, I need information about {topic}."), ("B", "Sure. What would you like to know?"), ("A", "Could you tell me the time and place?")],
        "speaking": ["I need information about {topic}.", "Could you tell me the time?", "I would like to change my plan."],
        "quiz": ("Choose the polite request.", "Could you tell me the time?"),
    },
    "pet": {
        "words": [("opinion", "y kien"), ("reason", "ly do"), ("experience", "kinh nghiem"), ("suggestion", "goi y"), ("choice", "lua chon"), ("improve", "cai thien"), ("compare", "so sanh"), ("explain", "giai thich")],
        "patterns": ["In my opinion, {topic} is important.", "The main reason is clear.", "I suggest we try another option."],
        "grammar": ["Use past simple for finished experiences.", "Use because/so to connect reasons and results."],
        "dialogue": [("A", "What do you think about {topic}?"), ("B", "In my opinion, it is a useful idea."), ("A", "Can you explain your reason?")],
        "speaking": ["In my opinion, {topic} is important.", "The main reason is clear.", "I suggest we try another option."],
        "quiz": ("Choose an opinion phrase.", "In my opinion"),
    },
    "ielts_foundation": {
        "words": [("topic", "chu de"), ("example", "vi du"), ("reason", "ly do"), ("opinion", "y kien"), ("habit", "thoi quen"), ("benefit", "loi ich"), ("problem", "van de"), ("answer", "cau tra loi")],
        "patterns": ["I usually talk about {topic} in simple words.", "One reason is that it is useful.", "For example, people can learn faster."],
        "grammar": ["Use simple present for habits and general facts.", "Use one clear example after each reason."],
        "dialogue": [("A", "Let's practise an IELTS topic: {topic}."), ("B", "I can give one simple reason."), ("A", "Good. Add one example.")],
        "speaking": ["I usually talk about {topic} in simple words.", "One reason is that it is useful.", "For example, people can learn faster."],
        "quiz": ("Choose a phrase for examples.", "For example"),
    },
    "ielts_50": {
        "words": [("overview", "tong quan"), ("trend", "xu huong"), ("support", "ung ho"), ("contrast", "tuong phan"), ("cause", "nguyen nhan"), ("effect", "ket qua"), ("solution", "giai phap"), ("conclusion", "ket luan")],
        "patterns": ["The main point about {topic} is clear.", "This example supports my opinion.", "However, there is another side."],
        "grammar": ["Use linking words to connect ideas.", "Use topic sentence plus support for each paragraph."],
        "dialogue": [("A", "What is your main point about {topic}?"), ("B", "The main point is clear."), ("A", "Now add a supporting example.")],
        "speaking": ["The main point about {topic} is clear.", "This example supports my opinion.", "However, there is another side."],
        "quiz": ("Choose a contrast linker.", "However"),
    },
    "ielts_65": {
        "words": [("nuance", "sac thai"), ("evidence", "bang chung"), ("coherence", "mach lac"), ("concession", "nhuong bo"), ("argument", "lap luan"), ("emphasis", "nhan manh"), ("precise", "chinh xac"), ("perspective", "goc nhin")],
        "patterns": ["Although {topic} has benefits, there are limits.", "From a broader perspective, this issue is complex.", "The evidence suggests a balanced answer."],
        "grammar": ["Use although/while to show contrast.", "Use precise academic vocabulary instead of general words."],
        "dialogue": [("A", "How can we make this answer more advanced?"), ("B", "We can add contrast and evidence."), ("A", "Good. Keep the argument balanced.")],
        "speaking": ["Although {topic} has benefits, there are limits.", "From a broader perspective, this issue is complex.", "The evidence suggests a balanced answer."],
        "quiz": ("Choose a concession linker.", "Although"),
    },
    "business": {
        "words": [("agenda", "chuong trinh hop"), ("deadline", "han chot"), ("client", "khach hang"), ("proposal", "de xuat"), ("budget", "ngan sach"), ("update", "cap nhat"), ("action item", "viec can lam"), ("decision", "quyet dinh")],
        "patterns": ["Could we discuss {topic} today?", "I will send a follow-up email.", "The deadline is tight but possible."],
        "grammar": ["Use could/would for polite workplace requests.", "Use future forms for plans and commitments."],
        "dialogue": [("A", "Could we discuss {topic} today?"), ("B", "Yes. Please give me a quick update."), ("A", "I will send the action items after the meeting.")],
        "speaking": ["Could we discuss {topic} today?", "I will send a follow-up email.", "The deadline is tight but possible."],
        "quiz": ("Choose a workplace request.", "Could we discuss this today?"),
    },
    "sales": {
        "words": [("customer", "khach hang"), ("need", "nhu cau"), ("benefit", "loi ich"), ("price", "gia"), ("discount", "giam gia"), ("objection", "phan doi"), ("value", "gia tri"), ("follow-up", "theo doi")],
        "patterns": ["What are you looking for today?", "This option gives you better value.", "Would you like me to prepare a quote?"],
        "grammar": ["Use open questions to find customer needs.", "Use comparatives to explain product value."],
        "dialogue": [("A", "What are you looking for today?"), ("B", "I need something reliable and affordable."), ("A", "This option gives you better value.")],
        "speaking": ["What are you looking for today?", "This option gives you better value.", "Would you like me to prepare a quote?"],
        "quiz": ("Choose an open sales question.", "What are you looking for today?"),
    },
    "cafe": {
        "words": [("order", "goi mon"), ("recommend", "goi y"), ("takeaway", "mang di"), ("receipt", "hoa don"), ("sugar", "duong"), ("allergy", "di ung"), ("combo", "combo"), ("counter", "quay")],
        "patterns": ["What would you like to order?", "Would you like it hot or iced?", "I'm sorry about the wait."],
        "grammar": ["Use would like for polite orders.", "Use apologies plus a solution for service problems."],
        "dialogue": [("A", "What would you like to order?"), ("B", "A latte with less sugar, please."), ("A", "Sure. Would you like it hot or iced?")],
        "speaking": ["What would you like to order?", "Would you like it hot or iced?", "I'm sorry about the wait."],
        "quiz": ("Choose a polite cafe question.", "What would you like to order?"),
    },
    "factory": {
        "words": [("safety", "an toan"), ("shift", "ca lam"), ("machine", "may moc"), ("supervisor", "giam sat"), ("helmet", "mu bao ho"), ("checklist", "danh sach kiem tra"), ("defect", "loi san pham"), ("warehouse", "kho")],
        "patterns": ["Please wear your safety equipment.", "The machine stopped during my shift.", "I need to report a problem."],
        "grammar": ["Use clear instructions for safety.", "Use past simple to report what happened."],
        "dialogue": [("A", "I need to report a problem."), ("B", "What happened during your shift?"), ("A", "The machine stopped after the quality check.")],
        "speaking": ["Please wear your safety equipment.", "The machine stopped during my shift.", "I need to report a problem."],
        "quiz": ("Choose a safety instruction.", "Please wear your safety equipment."),
    },
}


ADVANCED_WORD_EXAMPLES = {
    "schedule": ("Please check the schedule before class.", "Hãy kiểm tra lịch trình trước giờ học."),
    "ticket": ("I bought a train ticket this morning.", "Sáng nay tôi đã mua một vé tàu."),
    "notice": ("Please read the notice on the board.", "Hãy đọc thông báo trên bảng."),
    "form": ("Please fill out this form.", "Vui lòng điền vào mẫu đơn này."),
    "station": ("The station is near the city center.", "Nhà ga ở gần trung tâm thành phố."),
    "appointment": ("I have an appointment at three o'clock.", "Tôi có một cuộc hẹn lúc ba giờ."),
    "message": ("I sent a short message to my teacher.", "Tôi đã gửi một tin nhắn ngắn cho giáo viên."),
    "direction": ("Can you give me directions to the station?", "Bạn có thể chỉ đường đến nhà ga cho tôi không?"),
    "opinion": ("In my opinion, this plan is useful.", "Theo ý kiến của tôi, kế hoạch này hữu ích."),
    "reason": ("The main reason is easy to understand.", "Lý do chính rất dễ hiểu."),
    "experience": ("This experience helped me learn faster.", "Kinh nghiệm này giúp tôi học nhanh hơn."),
    "suggestion": ("Thank you for your helpful suggestion.", "Cảm ơn bạn vì lời gợi ý hữu ích."),
    "choice": ("This choice is better for beginners.", "Lựa chọn này tốt hơn cho người mới bắt đầu."),
    "improve": ("I want to improve my speaking every day.", "Tôi muốn cải thiện kỹ năng nói mỗi ngày."),
    "compare": ("Compare the two answers before you choose.", "Hãy so sánh hai câu trả lời trước khi chọn."),
    "explain": ("Can you explain your answer?", "Bạn có thể giải thích câu trả lời của mình không?"),
    "topic": ("This topic is about daily life.", "Chủ đề này nói về đời sống hằng ngày."),
    "example": ("This example makes the idea clearer.", "Ví dụ này làm cho ý tưởng rõ hơn."),
    "habit": ("Reading every day is a good habit.", "Đọc mỗi ngày là một thói quen tốt."),
    "benefit": ("One benefit is better pronunciation.", "Một lợi ích là phát âm tốt hơn."),
    "problem": ("We should solve this problem step by step.", "Chúng ta nên giải quyết vấn đề này từng bước."),
    "answer": ("Please write your answer clearly.", "Hãy viết câu trả lời của bạn thật rõ ràng."),
    "overview": ("The overview shows the main trend.", "Phần tổng quan cho thấy xu hướng chính."),
    "trend": ("The trend increased slowly last year.", "Xu hướng đã tăng chậm vào năm ngoái."),
    "support": ("This detail can support your opinion.", "Chi tiết này có thể hỗ trợ ý kiến của bạn."),
    "contrast": ("Use contrast to show a different idea.", "Hãy dùng sự tương phản để thể hiện một ý khác."),
    "cause": ("The cause of the problem is clear.", "Nguyên nhân của vấn đề rất rõ."),
    "effect": ("The effect can be seen quickly.", "Kết quả có thể được nhìn thấy nhanh chóng."),
    "solution": ("This solution is simple and practical.", "Giải pháp này đơn giản và thực tế."),
    "conclusion": ("The conclusion should answer the question.", "Kết luận nên trả lời đúng câu hỏi."),
    "nuance": ("This word has a small nuance in meaning.", "Từ này có một sắc thái nghĩa nhỏ."),
    "evidence": ("Strong evidence makes your argument better.", "Bằng chứng mạnh làm lập luận tốt hơn."),
    "coherence": ("Coherence helps the reader follow your ideas.", "Sự mạch lạc giúp người đọc theo dõi ý của bạn."),
    "concession": ("A concession shows that you understand both sides.", "Sự nhượng bộ cho thấy bạn hiểu cả hai phía."),
    "argument": ("Your argument needs clear evidence.", "Lập luận của bạn cần bằng chứng rõ ràng."),
    "emphasis": ("Use emphasis for the most important idea.", "Hãy nhấn mạnh ý quan trọng nhất."),
    "precise": ("A precise word makes your answer stronger.", "Một từ chính xác làm câu trả lời mạnh hơn."),
    "perspective": ("This perspective is useful for the essay.", "Góc nhìn này hữu ích cho bài luận."),
    "agenda": ("The meeting agenda has three items.", "Chương trình họp có ba mục."),
    "deadline": ("The deadline is Friday afternoon.", "Hạn chót là chiều thứ Sáu."),
    "client": ("The client asked for a quick update.", "Khách hàng yêu cầu cập nhật nhanh."),
    "proposal": ("I will send the proposal today.", "Tôi sẽ gửi đề xuất hôm nay."),
    "budget": ("The budget is limited this month.", "Ngân sách tháng này bị giới hạn."),
    "update": ("Please send me an update after lunch.", "Vui lòng gửi cho tôi bản cập nhật sau bữa trưa."),
    "action item": ("Each action item needs an owner.", "Mỗi việc cần làm cần có người phụ trách."),
    "decision": ("We need a decision before Monday.", "Chúng ta cần quyết định trước thứ Hai."),
    "customer": ("The customer needs more information.", "Khách hàng cần thêm thông tin."),
    "need": ("Ask about the customer's need first.", "Hãy hỏi về nhu cầu của khách hàng trước."),
    "price": ("The price is clear on the label.", "Giá được ghi rõ trên nhãn."),
    "discount": ("This discount is available today.", "Giảm giá này có hiệu lực hôm nay."),
    "objection": ("Listen carefully to the customer's objection.", "Hãy lắng nghe kỹ sự phản đối của khách hàng."),
    "value": ("This product gives good value.", "Sản phẩm này mang lại giá trị tốt."),
    "follow-up": ("I will send a follow-up message tomorrow.", "Tôi sẽ gửi tin nhắn theo dõi vào ngày mai."),
    "order": ("I would like to place an order.", "Tôi muốn đặt món/đặt hàng."),
    "recommend": ("Can you recommend a cold drink?", "Bạn có thể gợi ý một món uống lạnh không?"),
    "takeaway": ("This coffee is for takeaway.", "Ly cà phê này mang đi."),
    "receipt": ("Can I have a receipt, please?", "Cho tôi xin hóa đơn được không?"),
    "sugar": ("I would like less sugar, please.", "Tôi muốn ít đường hơn."),
    "allergy": ("Do you have any food allergy?", "Bạn có bị dị ứng thực phẩm nào không?"),
    "combo": ("The lunch combo is cheaper.", "Combo bữa trưa rẻ hơn."),
    "counter": ("Please pay at the counter.", "Vui lòng thanh toán tại quầy."),
    "safety": ("Safety comes first in the factory.", "An toàn là ưu tiên hàng đầu trong nhà máy."),
    "shift": ("My shift starts at eight o'clock.", "Ca làm của tôi bắt đầu lúc tám giờ."),
    "machine": ("The machine needs a quick check.", "Máy móc cần được kiểm tra nhanh."),
    "supervisor": ("Please tell your supervisor about the issue.", "Hãy báo cho giám sát của bạn về vấn đề này."),
    "helmet": ("Please wear your helmet in this area.", "Vui lòng đội mũ bảo hộ trong khu vực này."),
    "checklist": ("Use the checklist before you start.", "Hãy dùng danh sách kiểm tra trước khi bắt đầu."),
    "defect": ("This product has a small defect.", "Sản phẩm này có một lỗi nhỏ."),
    "warehouse": ("The boxes are in the warehouse.", "Các thùng hàng ở trong kho."),
}


def _advanced_vocab_example(word, meaning, topic_key, skill="vocabulary"):
    clean_word = str(word or "").strip()
    clean_topic = str(topic_key or "").strip()
    if clean_word == clean_topic:
        if skill == "grammar":
            return (
                f"We will use grammar to talk about {clean_topic}.",
                f"Chúng ta sẽ dùng ngữ pháp để nói về {meaning}.",
            )
        if skill == "listening":
            return (
                f"Listen for the main idea about {clean_topic}.",
                f"Hãy nghe để nắm ý chính về {meaning}.",
            )
        if skill == "reading":
            return (
                f"Read the text and find information about {clean_topic}.",
                f"Đọc bài và tìm thông tin về {meaning}.",
            )
        if skill == "writing":
            return (
                f"Write a short paragraph about {clean_topic}.",
                f"Viết một đoạn ngắn về {meaning}.",
            )
        return (
            f"This lesson is about {clean_topic}.",
            f"Bài này nói về {meaning}.",
        )
    if skill == "vocabulary" and clean_word in ADVANCED_WORD_EXAMPLES:
        return ADVANCED_WORD_EXAMPLES[clean_word]
    skill_templates = {
        "grammar": (
            f"Use '{clean_word}' in one clear grammar sentence.",
            f"Dùng '{clean_word}' trong một câu ngữ pháp rõ ràng về {meaning}.",
        ),
        "listening": (
            f"Listen carefully when you hear the word '{clean_word}'.",
            f"Hãy nghe kỹ khi bạn nghe thấy từ '{clean_word}' ({meaning}).",
        ),
        "reading": (
            f"Find the word '{clean_word}' in the reading text.",
            f"Tìm từ '{clean_word}' ({meaning}) trong bài đọc.",
        ),
        "writing": (
            f"Use '{clean_word}' in your writing task.",
            f"Dùng '{clean_word}' ({meaning}) trong bài viết của bạn.",
        ),
    }
    if skill in skill_templates:
        return skill_templates[skill]
    return (
        f"We use '{clean_word}' when we talk about {clean_topic}.",
        f"Chúng ta dùng '{clean_word}' khi nói về {meaning}.",
    )


ADVANCED_TOPIC_VI_OVERRIDES = {
    "daily schedule": "lịch trình hằng ngày",
    "buying a ticket": "mua vé",
    "writing a note": "viết ghi chú",
    "asking for directions": "hỏi đường",
    "making an appointment": "đặt lịch hẹn",
    "lost property": "đồ bị thất lạc",
    "weekend activities": "hoạt động cuối tuần",
    "simple email": "email đơn giản",
    "public transport": "phương tiện công cộng",
    "at the doctor": "đi khám bác sĩ",
}


ADVANCED_TOPIC_WORD_VI = {
    "abstract": "trừu tượng",
    "account": "tài khoản",
    "activity": "hoạt động",
    "advice": "lời khuyên",
    "allergy": "dị ứng",
    "appointment": "lịch hẹn",
    "argument": "lập luận",
    "article": "bài viết",
    "asking": "hỏi",
    "bar": "biểu đồ cột",
    "booking": "đặt chỗ",
    "budget": "ngân sách",
    "business": "kinh doanh",
    "cafe": "quán cà phê",
    "card": "thẻ",
    "career": "nghề nghiệp",
    "chart": "biểu đồ",
    "class": "lớp học",
    "client": "khách hàng",
    "clothes": "quần áo",
    "club": "câu lạc bộ",
    "coffee": "cà phê",
    "complaint": "khiếu nại",
    "contract": "hợp đồng",
    "course": "khóa học",
    "customer": "khách hàng",
    "daily": "hằng ngày",
    "deadline": "hạn chót",
    "decision": "quyết định",
    "directions": "đường đi",
    "doctor": "bác sĩ",
    "email": "email",
    "essay": "bài luận",
    "factory": "nhà máy",
    "family": "gia đình",
    "food": "đồ ăn",
    "friend": "bạn bè",
    "graph": "biểu đồ",
    "health": "sức khỏe",
    "hotel": "khách sạn",
    "invitation": "lời mời",
    "invoice": "hóa đơn",
    "job": "công việc",
    "key": "chìa khóa",
    "library": "thư viện",
    "meeting": "cuộc họp",
    "message": "tin nhắn",
    "notice": "thông báo",
    "office": "văn phòng",
    "opinion": "ý kiến",
    "order": "đơn hàng",
    "payment": "thanh toán",
    "phone": "điện thoại",
    "plan": "kế hoạch",
    "presentation": "thuyết trình",
    "price": "giá",
    "problem": "vấn đề",
    "project": "dự án",
    "question": "câu hỏi",
    "review": "ôn tập",
    "sales": "bán hàng",
    "schedule": "lịch trình",
    "school": "trường học",
    "shopping": "mua sắm",
    "speaking": "nói",
    "sports": "thể thao",
    "station": "nhà ga",
    "story": "câu chuyện",
    "teacher": "giáo viên",
    "ticket": "vé",
    "timetable": "thời khóa biểu",
    "topic": "chủ đề",
    "transport": "giao thông",
    "travel": "du lịch",
    "visitor": "khách tham quan",
    "weather": "thời tiết",
    "work": "công việc",
    "workplace": "nơi làm việc",
    "writing": "viết",
}


def _advanced_topic_vi(topic):
    topic_key = str(topic or "").strip().lower()
    if topic_key in ADVANCED_TOPIC_VI_OVERRIDES:
        return ADVANCED_TOPIC_VI_OVERRIDES[topic_key]
    words = []
    for raw in topic_key.replace("-", " ").replace("/", " ").split():
        words.append(ADVANCED_TOPIC_WORD_VI.get(raw, raw))
    return " ".join(words).strip() or topic_key

ADVANCED_LESSON_MODES = [
    {
        "skill": "vocabulary",
        "suffix": "Vocabulary Builder",
        "wordOffsets": list(range(8)),
        "patterns": [
            ("I use {word1} when I talk about {topic}.", "Tôi dùng {word1} khi nói về {topic}."),
            ("The word {word2} is useful in this lesson.", "Từ {word2} rất hữu ích trong bài này."),
            ("Please make one sentence with {word3}.", "Hãy đặt một câu với {word3}."),
        ],
        "grammar": [
            ("Learn the meaning first, then read the example sentence.", "Học nghĩa trước, sau đó đọc câu ví dụ."),
            ("Use each new word in one short sentence.", "Dùng mỗi từ mới trong một câu ngắn."),
        ],
        "dialogue": [
            ("A", "Which word is new for you in {topic}?", "Từ nào mới với bạn trong chủ đề {topic}?"),
            ("B", "The word {word1} is new for me.", "Từ {word1} mới với tôi."),
            ("A", "Good. Make one sentence with it.", "Tốt. Hãy đặt một câu với từ đó."),
        ],
        "speaking": [
            ("I can say {word1} clearly.", "Tôi có thể nói rõ từ {word1}."),
            ("I can use {word2} in a sentence.", "Tôi có thể dùng {word2} trong một câu."),
        ],
        "quiz": ("Choose the word from this vocabulary lesson.", "{word1}"),
    },
    {
        "skill": "grammar",
        "suffix": "Grammar Focus",
        "wordOffsets": [0, 2, 4, 6],
        "patterns": [
            ("Could you help me with {topic}?", "Bạn có thể giúp tôi về {topic} không?"),
            ("I need to check {word1} before I answer.", "Tôi cần kiểm tra {word1} trước khi trả lời."),
            ("Please explain {word2} one more time.", "Vui lòng giải thích {word2} thêm một lần nữa."),
        ],
        "grammar": [
            ("Use could you + base verb for polite questions.", "Dùng could you + động từ nguyên mẫu để hỏi lịch sự."),
            ("Use need to + verb when something is necessary.", "Dùng need to + động từ khi việc gì đó cần thiết."),
            ("Use before/after to show order of actions.", "Dùng before/after để nói thứ tự hành động."),
        ],
        "dialogue": [
            ("A", "Could you explain {topic}?", "Bạn có thể giải thích {topic} không?"),
            ("B", "Sure. First, check {word1}.", "Được. Trước tiên, hãy kiểm tra {word1}."),
            ("A", "Then I can answer clearly.", "Sau đó tôi có thể trả lời rõ ràng."),
        ],
        "speaking": [
            ("Could you help me with {topic}?", "Bạn có thể giúp tôi về {topic} không?"),
            ("I need to check {word1} before I answer.", "Tôi cần kiểm tra {word1} trước khi trả lời."),
        ],
        "quiz": ("Complete: Could you ___ me?", "help"),
    },
    {
        "skill": "listening",
        "suffix": "Listening Practice",
        "wordOffsets": [1, 3, 5, 7],
        "patterns": [
            ("Listen for the main idea about {topic}.", "Nghe để nắm ý chính về {topic}."),
            ("Write down the detail about {word1}.", "Ghi lại chi tiết về {word1}."),
            ("Listen again and check your answer.", "Nghe lại và kiểm tra câu trả lời."),
        ],
        "grammar": [
            ("When listening, catch names, numbers, places, and actions first.", "Khi nghe, bắt tên, số, nơi chốn và hành động trước."),
            ("Do not translate every word; listen for the task answer.", "Không cần dịch từng từ; hãy nghe để trả lời nhiệm vụ."),
        ],
        "dialogue": [
            ("A", "I need help with {topic}.", "Tôi cần giúp về {topic}."),
            ("B", "Please listen carefully. The first detail is {word1}.", "Hãy nghe kỹ. Chi tiết đầu tiên là {word1}."),
            ("A", "I heard {word1}, but I need to check {word2}.", "Tôi nghe được {word1}, nhưng cần kiểm tra {word2}."),
            ("B", "Listen again. The answer is in the last sentence.", "Nghe lại nhé. Câu trả lời nằm ở câu cuối."),
        ],
        "speaking": [
            ("I heard the main idea about {topic}.", "Tôi đã nghe được ý chính về {topic}."),
            ("The important detail is {word1}.", "Chi tiết quan trọng là {word1}."),
        ],
        "quiz": ("What should you listen for first?", "main idea"),
    },
    {
        "skill": "reading",
        "suffix": "Reading Practice",
        "wordOffsets": [2, 4, 6, 0],
        "patterns": [
            ("Read the short text about {topic}.", "Đọc đoạn văn ngắn về {topic}."),
            ("Underline the sentence with {word1}.", "Gạch dưới câu có {word1}."),
            ("Choose the best answer from the text.", "Chọn câu trả lời đúng nhất từ bài đọc."),
        ],
        "grammar": [
            ("Read the title first to predict the topic.", "Đọc tiêu đề trước để đoán chủ đề."),
            ("Look for repeated words because they often show the main idea.", "Tìm từ lặp lại vì chúng thường cho biết ý chính."),
        ],
        "dialogue": [
            ("A", "What is this text about?", "Đoạn văn này nói về gì?"),
            ("B", "It is about {topic}.", "Nó nói về {topic}."),
            ("A", "Which detail supports your answer?", "Chi tiết nào chứng minh câu trả lời của bạn?"),
        ],
        "speaking": [
            ("This text is about {topic}.", "Đoạn văn này nói về {topic}."),
            ("The detail about {word1} is important.", "Chi tiết về {word1} rất quan trọng."),
        ],
        "quiz": ("What should you read first?", "title"),
    },
    {
        "skill": "writing",
        "suffix": "Writing Task",
        "wordOffsets": [3, 5, 7, 1],
        "patterns": [
            ("I will write about {topic}.", "Tôi sẽ viết về {topic}."),
            ("My first sentence will mention {word1}.", "Câu đầu tiên của tôi sẽ nhắc đến {word1}."),
            ("I will finish with one clear idea.", "Tôi sẽ kết thúc bằng một ý rõ ràng."),
        ],
        "grammar": [
            ("Write one topic sentence, two details, and one final sentence.", "Viết một câu chủ đề, hai chi tiết và một câu kết."),
            ("Keep sentences short and clear at this level.", "Ở trình độ này, hãy viết câu ngắn và rõ."),
        ],
        "dialogue": [
            ("A", "What will you write about?", "Bạn sẽ viết về điều gì?"),
            ("B", "I will write about {topic}.", "Tôi sẽ viết về {topic}."),
            ("A", "Good. Use {word1} in your first sentence.", "Tốt. Hãy dùng {word1} trong câu đầu."),
        ],
        "speaking": [
            ("I will write about {topic}.", "Tôi sẽ viết về {topic}."),
            ("My first sentence will mention {word1}.", "Câu đầu tiên của tôi sẽ nhắc đến {word1}."),
        ],
        "quiz": ("What should a short paragraph start with?", "topic sentence"),
    },
]


def _advanced_lesson_title(topic, mode):
    suffix = mode.get("suffix", "")
    return topic if not suffix else f"{topic} {suffix}"


def _advanced_mode_words(pool, idx):
    mode = ADVANCED_LESSON_MODES[idx % len(ADVANCED_LESSON_MODES)]
    unit_shift = (idx // len(ADVANCED_LESSON_MODES)) % max(len(pool), 1)
    return [pool[(unit_shift + offset) % len(pool)] for offset in mode["wordOffsets"]]


def _advanced_secondary_count(skill, section):
    counts = {
        "vocabulary": {"patterns": 3, "grammar": 2, "dialogue": 3, "speaking": 2, "words": 9},
        "grammar": {"patterns": 2, "grammar": 5, "dialogue": 2, "speaking": 1, "words": 4},
        "listening": {"patterns": 1, "grammar": 1, "dialogue": 4, "speaking": 1, "words": 4},
        "reading": {"patterns": 1, "grammar": 1, "dialogue": 2, "speaking": 1, "words": 4},
        "writing": {"patterns": 2, "grammar": 1, "dialogue": 2, "speaking": 1, "words": 4},
    }
    return counts.get(skill, {}).get(section, 2)


def _take_primary_sized(items, skill, section):
    return list(items)[:_advanced_secondary_count(skill, section)]


def _advanced_format_lines(lines, topic_key, words, topic_vi=None):
    word_map = {f"word{pos + 1}": word for pos, (word, _meaning) in enumerate(words)}
    translation_map = dict(word_map)
    translation_map["topic"] = topic_vi or topic_key
    formatted = []
    for item in lines:
        if isinstance(item, tuple):
            text, translation = item
            formatted.append({
                "text": text.format(topic=topic_key, **word_map),
                "translation": translation.format(**translation_map),
            })
        else:
            formatted.append(item.format(topic=topic_key, **word_map))
    return formatted


def _advanced_format_dialogue(lines, topic_key, words, topic_vi=None):
    word_map = {f"word{pos + 1}": word for pos, (word, _meaning) in enumerate(words)}
    translation_map = dict(word_map)
    translation_map["topic"] = topic_vi or topic_key
    formatted = []
    for item in lines:
        speaker, text, translation = item
        formatted.append({
            "speaker": speaker,
            "text": text.format(topic=topic_key, **word_map),
            "translation": translation.format(**translation_map),
        })
    return formatted


def _advanced_format_rules(lines, topic_key, words, topic_vi=None):
    return _advanced_format_lines(lines, topic_key, words, topic_vi)


def _advanced_expand_grammar_rules(skill, topic_key, words, topic_vi=None):
    if skill != "grammar":
        return []
    word_map = {f"word{pos + 1}": word for pos, (word, _meaning) in enumerate(words)}
    translation_map = dict(word_map)
    translation_map["topic"] = topic_vi or topic_key
    extra_rules = [
        ("Pattern: Could you + verb + ...?", "Mẫu câu: Could you + động từ + ...?"),
        ("Example: Could you check {word1}?", "Ví dụ: Bạn có thể kiểm tra {word1} không?"),
        ("Pattern: I need to + verb + ...", "Mẫu câu: I need to + động từ + ..."),
        ("Example: I need to check {word2}.", "Ví dụ: Tôi cần kiểm tra {word2}."),
    ]
    return [
        {"text": text.format(topic=topic_key, **word_map), "translation": translation.format(**translation_map)}
        for text, translation in extra_rules
    ]


def _advanced_long_listening_passage(topic_key, display_topic, word_map):
    passage_lines = [
        "Today, a learner is practising English for {topic}.",
        "The learner opens the lesson and listens to the teacher carefully.",
        "The first important word in the lesson is {word1}.",
        "The teacher gives a short example with {word1}.",
        "Then the learner hears another useful word: {word2}.",
        "The learner writes {word2} in a notebook.",
        "After that, the teacher explains a detail about {word3}.",
        "The learner listens again because the sentence is a little fast.",
        "The teacher says that clear listening is more important than perfect translation.",
        "The learner checks the main idea before answering the questions.",
        "At the end, the learner repeats one sentence aloud.",
        "This helps the learner remember the words and speak with more confidence.",
    ]
    translation_lines = [
        "Hôm nay, một học viên luyện tiếng Anh về {topic}.",
        "Học viên mở bài học và nghe giáo viên thật kỹ.",
        "Từ quan trọng đầu tiên trong bài là {word1}.",
        "Giáo viên đưa ra một ví dụ ngắn với {word1}.",
        "Sau đó học viên nghe một từ hữu ích khác: {word2}.",
        "Học viên viết {word2} vào vở.",
        "Tiếp theo, giáo viên giải thích một chi tiết về {word3}.",
        "Học viên nghe lại vì câu đó hơi nhanh.",
        "Giáo viên nói rằng nghe được ý chính quan trọng hơn dịch hoàn hảo.",
        "Học viên kiểm tra ý chính trước khi trả lời câu hỏi.",
        "Cuối bài, học viên lặp lại một câu thành tiếng.",
        "Điều này giúp học viên nhớ từ và nói tự tin hơn.",
    ]
    format_en = {"topic": topic_key, **word_map}
    format_vi = {"topic": display_topic, **word_map}
    return (
        " ".join(line.format(**format_en) for line in passage_lines),
        " ".join(line.format(**format_vi) for line in translation_lines),
    )


def _advanced_long_reading_passage(topic_key, display_topic, word_map):
    passage_lines = [
        "{topic} is a useful topic for daily communication.",
        "Many learners meet this situation at school, at work, or when they travel.",
        "Before reading, it is helpful to look at the title.",
        "The title tells the learner what the text is mainly about.",
        "In this text, the learner should notice the word {word1}.",
        "The word {word1} often gives an important clue.",
        "The learner should also find the word {word2}.",
        "This word may appear near a key detail.",
        "If the text has dates, places, or numbers, the learner should underline them.",
        "The learner does not need to translate every sentence.",
        "A good reader looks for the main idea first.",
        "After that, the learner reads the questions and returns to the text for evidence.",
        "This habit makes reading faster and more accurate.",
    ]
    translation_lines = [
        "{topic} là một chủ đề hữu ích trong giao tiếp hằng ngày.",
        "Nhiều người học gặp tình huống này ở trường, nơi làm việc hoặc khi đi du lịch.",
        "Trước khi đọc, người học nên nhìn tiêu đề.",
        "Tiêu đề cho biết bài đọc chủ yếu nói về điều gì.",
        "Trong bài này, người học nên chú ý từ {word1}.",
        "Từ {word1} thường cho một gợi ý quan trọng.",
        "Người học cũng nên tìm từ {word2}.",
        "Từ này có thể xuất hiện gần một chi tiết chính.",
        "Nếu bài có ngày tháng, địa điểm hoặc con số, người học nên gạch dưới.",
        "Người học không cần dịch từng câu.",
        "Một người đọc tốt tìm ý chính trước.",
        "Sau đó, người học đọc câu hỏi và quay lại bài để tìm bằng chứng.",
        "Thói quen này giúp đọc nhanh và chính xác hơn.",
    ]
    format_en = {"topic": topic_key, **word_map}
    format_vi = {"topic": display_topic, **word_map}
    return (
        " ".join(line.format(**format_en) for line in passage_lines),
        " ".join(line.format(**format_vi) for line in translation_lines),
    )


def _advanced_writing_sentence_bank(topic_key, display_topic, word_map):
    starters = [
        ("I want to write about {topic}.", "Tôi muốn viết về {topic}."),
        ("This topic is useful for my daily English.", "Chủ đề này hữu ích cho tiếng Anh hằng ngày của tôi."),
        ("The first important word is {word1}.", "Từ quan trọng đầu tiên là {word1}."),
        ("I can use {word1} in a simple sentence.", "Tôi có thể dùng {word1} trong một câu đơn giản."),
        ("Another useful word is {word2}.", "Một từ hữu ích khác là {word2}."),
        ("For example, I need to check {word2}.", "Ví dụ, tôi cần kiểm tra {word2}."),
        ("I also want to remember {word3}.", "Tôi cũng muốn nhớ {word3}."),
        ("This will help me speak more clearly.", "Điều này sẽ giúp tôi nói rõ hơn."),
        ("Next time, I will practise this topic again.", "Lần sau, tôi sẽ luyện lại chủ đề này."),
        ("In short, {topic} is important for me.", "Tóm lại, {topic} quan trọng với tôi."),
    ]
    format_en = {"topic": topic_key, **word_map}
    format_vi = {"topic": display_topic, **word_map}
    return [
        {"text": text.format(**format_en), "translation": translation.format(**format_vi)}
        for text, translation in starters
    ]


def _advanced_skill_extra(mode, topic_key, words, topic_vi=None):
    word_map = {f"word{pos + 1}": word for pos, (word, _meaning) in enumerate(words)}
    display_topic = topic_vi or topic_key
    skill = mode.get("skill")
    if skill == "grammar":
        return {
            "skillFocus": "grammar",
            "grammarPractice": {
                "title": "Grammar practice",
                "translation": "Luyện ngữ pháp",
                "examples": _advanced_format_lines([
                    ("Could you help me with {topic}?", "Bạn có thể giúp tôi về {topic} không?"),
                    ("I need to check {word1} before I answer.", "Tôi cần kiểm tra {word1} trước khi trả lời."),
                ], topic_key, words, display_topic),
                "tasks": [
                    "Fill in the blank: Could you ___ me?",
                    "Rewrite the sentence with 'need to'.",
                    "Say one polite question about this topic.",
                    "Make one sentence with 'before'.",
                    "Make one sentence with 'after'.",
                ],
            },
        }
    if skill == "listening":
        passage, passage_translation = _advanced_long_listening_passage(topic_key, display_topic, word_map)
        return {
            "skillFocus": "listening",
            "listeningTask": {
                "title": "Long listening",
                "translation": "Bài nghe dài",
                "passage": passage,
                "passageTranslation": passage_translation,
                "questions": [
                    {"question": "What is the listening mainly about?", "translation": "Bài nghe chủ yếu nói về gì?", "answer": topic_key},
                    {"question": "Which detail is mentioned first?", "translation": "Chi tiết nào được nhắc đến đầu tiên?", "answer": word_map.get("word1", "")},
                    {"question": "What does the student need to check?", "translation": "Học viên cần kiểm tra điều gì?", "answer": word_map.get("word2", "")},
                    {"question": "What should the student do at the end?", "translation": "Cuối cùng học viên nên làm gì?", "answer": "listen again"},
                    {"question": "What is more important than perfect translation?", "translation": "Điều gì quan trọng hơn dịch hoàn hảo?", "answer": "clear listening"},
                ],
            },
        }
    if skill == "reading":
        passage, passage_translation = _advanced_long_reading_passage(topic_key, display_topic, word_map)
        return {
            "skillFocus": "reading",
            "readingTask": {
                "title": "Reading text",
                "translation": "Bài đọc",
                "passage": passage,
                "passageTranslation": passage_translation,
                "questions": [
                    {"question": "What should the learner read first?", "translation": "Người học nên đọc gì trước?", "answer": "the title"},
                    {"question": "Name one key word from the text.", "translation": "Nêu một từ khóa trong bài đọc.", "answer": word_map.get("word1", "")},
                    {"question": "Why are repeated words useful?", "translation": "Vì sao từ lặp lại hữu ích?", "answer": "They show the main idea."},
                    {"question": "Should the learner translate every word?", "translation": "Người học có nên dịch từng từ không?", "answer": "No"},
                    {"question": "What should the learner return to the text for?", "translation": "Người học quay lại bài đọc để tìm gì?", "answer": "evidence"},
                ],
            },
        }
    if skill == "writing":
        return {
            "skillFocus": "writing",
            "writingTask": {
                "title": "Writing guide",
                "translation": "Gợi ý viết",
                "prompt": "Write 4 short sentences about {topic}. Use {word1} and {word2}.".format(topic=topic_key, **word_map),
                "promptTranslation": "Viết 4 câu ngắn về {topic}. Dùng {word1} và {word2}.".format(topic=display_topic, **word_map),
                "outline": [
                    "Sentence 1: introduce the topic.",
                    "Sentence 2: add one detail.",
                    "Sentence 3: add one example.",
                    "Sentence 4: finish with your opinion or plan.",
                ],
                "outlineTranslation": [
                    "Câu 1: giới thiệu chủ đề.",
                    "Câu 2: thêm một chi tiết.",
                    "Câu 3: thêm một ví dụ.",
                    "Câu 4: kết thúc bằng ý kiến hoặc kế hoạch của bạn.",
                ],
                "sample": "I want to improve my English for {topic}. First, I will learn the word {word1}. Then I will use {word2} in one sentence. I will practise again tomorrow.".format(topic=topic_key, **word_map),
                "sampleTranslation": "Tôi muốn cải thiện tiếng Anh cho chủ đề {topic}. Đầu tiên, tôi sẽ học từ {word1}. Sau đó tôi sẽ dùng {word2} trong một câu. Tôi sẽ luyện lại vào ngày mai.".format(topic=display_topic, **word_map),
                "sentenceStarters": _advanced_writing_sentence_bank(topic_key, display_topic, word_map),
                "checklist": [
                    "I wrote 4 short sentences.",
                    "I used 2 words from this lesson.",
                    "I checked capital letters and periods.",
                ],
                "checklistTranslation": [
                    "Tôi đã viết 4 câu ngắn.",
                    "Tôi đã dùng 2 từ trong bài này.",
                    "Tôi đã kiểm tra chữ hoa và dấu chấm.",
                ],
            },
        }
    return {"skillFocus": skill or "vocabulary"}


def _advanced_topic_spec(level_id, topic, idx):
    profile = LEVEL_CONTENT_PROFILES[level_id]
    topic_key = topic.lower()
    topic_vi = _advanced_topic_vi(topic)
    pool = profile["words"]
    mode = ADVANCED_LESSON_MODES[idx % len(ADVANCED_LESSON_MODES)]
    skill = mode.get("skill", "vocabulary")
    mode_words = _advanced_mode_words(pool, idx)
    primary_word_limit = max(_advanced_secondary_count(skill, "words") - 1, 1)
    selected_words = [(topic_key, topic_vi)] + mode_words[:primary_word_limit]
    words = []
    for word, meaning in selected_words:
        example, example_translation = _advanced_vocab_example(word, meaning, topic_key, skill)
        words.append((word, meaning, example, "", meaning, "", example_translation))
    patterns = _advanced_format_lines(_take_primary_sized(mode["patterns"], skill, "patterns"), topic_key, mode_words, topic_vi)
    grammar = _advanced_format_rules(_take_primary_sized(mode["grammar"], skill, "grammar"), topic_key, mode_words, topic_vi)
    grammar += _advanced_expand_grammar_rules(skill, topic_key, mode_words, topic_vi)
    grammar = grammar[:_advanced_secondary_count(skill, "grammar")]
    dialogue = _advanced_format_dialogue(_take_primary_sized(mode["dialogue"], skill, "dialogue"), topic_key, mode_words, topic_vi)
    speaking = _advanced_format_lines(_take_primary_sized(mode["speaking"], skill, "speaking"), topic_key, mode_words, topic_vi)
    quiz_prompt_template, quiz_answer_template = mode["quiz"]
    word_map = {f"word{pos + 1}": word for pos, (word, _meaning) in enumerate(mode_words)}
    quiz_prompt = quiz_prompt_template.format(topic=topic_key, **word_map)
    quiz_answer = quiz_answer_template.format(topic=topic_key, **word_map)
    title = _advanced_lesson_title(topic, mode)
    extra_content = _advanced_skill_extra(mode, topic_key, mode_words, topic_vi)
    return (topic, title, words, patterns, grammar, dialogue, speaking, f"{quiz_prompt}||{quiz_answer}", extra_content)


for level in ROADMAP_LEVELS:
    if level["id"] not in {"starter", "flyer"} and level["id"] in ADVANCED_LEVEL_TOPICS:
        specs = []
        for topic_idx, topic in enumerate(ADVANCED_LEVEL_TOPICS.get(level["id"], [])):
            base_idx = topic_idx * len(ADVANCED_LESSON_MODES)
            for mode_idx in range(len(ADVANCED_LESSON_MODES)):
                specs.append(_advanced_topic_spec(level["id"], topic, base_idx + mode_idx))
        ROADMAP_UNITS += _build_units(level["id"], level["title"], specs)


JAPANESE_LEVEL_TOPICS = {
    "jp_intro": [
        "Hiragana A Line", "Hiragana K Line", "Hiragana S Line", "Hiragana T Line", "Hiragana N Line",
        "Hiragana H Line", "Hiragana M Line", "Hiragana Y Line", "Hiragana R Line", "Hiragana W Line",
        "Dakuten G and Z Sounds", "Dakuten D B P Sounds", "Small Ya Yu Yo Sounds",
        "Numbers 0 to 10", "Numbers 11 to 100", "Days of Week", "Months of Year", "Dates and Calendar",
        "Daily Greetings", "Thank You and Sorry", "Simple Self Introduction", "Classroom Survival", "Starter Review",
    ],
    "jp_n5": [
        "Greetings", "Self Introduction", "Numbers 1 to 100", "Family", "Time and Days",
        "Classroom Objects", "Food and Drinks", "Shopping Basics", "Places in Town", "Daily Routine",
        "Particles wa and ga", "Particle o", "Particle ni", "I Like It", "Simple Questions",
        "There Is", "Adjectives i", "Adjectives na", "Past Tense Basics", "N5 Review",
    ],
    "jp_n4": [
        "Te Form", "Requests", "Permission", "Prohibition", "Experience",
        "Plans", "Reasons with kara", "Comparisons", "Want To Do", "Giving Advice",
        "Weather Talk", "Travel Plan", "Lost Item", "Phone Message", "Doctor Visit",
        "School Rules", "Part-time Job", "Hobby Details", "Going to Japan", "Simple Email",
        "Potential Form", "Before and After", "Because and Although", "Listening Practice", "N4 Review",
    ],
    "jp_n3": [
        "Giving Opinions", "Explaining Reasons", "Workplace Basics", "School Discussion", "Making Complaints",
        "Apologizing Naturally", "Asking for Help", "News Topic", "Health Habits", "Travel Trouble",
        "Indirect Speech", "Trying To Do", "Seems Like", "Must Do", "May Happen",
        "Respectful Speech Basics", "Casual Conversation", "Storytelling", "Comparing Choices", "Making Suggestions",
        "Reading Short Article", "Speaking Fluency", "Grammar Review", "Vocabulary Review", "N3 Review",
    ],
    "jp_n2": [
        "Business Greeting", "Meeting Update", "Keigo Requests", "Customer Support", "Explaining Data",
        "Social Issue", "News Summary", "Agreeing Politely", "Disagreeing Softly", "Presentation Opening",
        "Formal Email", "Job Interview", "Problem Solving", "Cause and Effect", "Nuance Practice",
        "Reading Essay", "Listening News", "Work Report", "Negotiation Basics", "Giving Feedback",
        "Advanced Particles", "Sentence Connectors", "Natural Fillers", "Kanji in Context", "N2 Review",
    ],
    "jp_n1": [
        "Abstract Opinion", "Economic Topic", "Cultural Debate", "Academic Reading", "Executive Summary",
        "Advanced Keigo", "Formal Apology", "Persuasive Speaking", "Policy Discussion", "Risk Explanation",
        "Subtle Emotion", "Literary Expression", "Idioms", "Advanced Connectors", "Precise Vocabulary",
        "Negotiation Strategy", "Presentation Q and A", "Critical Reading", "Long Listening", "Natural Conversation",
        "Writing Argument", "Summarizing Article", "High-level Interview", "Final Speaking", "N1 Review",
    ],
}


JAPANESE_CONTENT_PROFILES = {
    "jp_n5": {
        "words": [("わたし", "watashi - toi", "わたしはアンです。"), ("せんせい", "sensei - giao vien", "せんせいはやさしいです。"), ("がっこう", "gakkou - truong hoc", "がっこうへいきます。"), ("みず", "mizu - nuoc", "みずをのみます。"), ("ともだち", "tomodachi - ban be", "ともだちにあいます。"), ("えき", "eki - nha ga", "えきはどこですか。"), ("いくら", "ikura - bao nhieu tien", "これはいくらですか。"), ("すき", "suki - thich", "すしがすきです。")],
        "patterns": ["わたしは {topic} をべんきょうします。", "{topic} はやさしいです。", "{topic} はどこですか。"],
        "grammar": ["Use は to mark the topic.", "Use です for simple polite sentences.", "Use を before the object of an action."],
        "dialogue": [("A", "こんにちは。"), ("B", "こんにちは。{topic} をべんきょうしています。"), ("A", "いいですね。")],
        "speaking": ["わたしは {topic} をべんきょうします。", "{topic} はやさしいです。", "もういちどおねがいします。"],
        "quiz": ("Choose the polite ending for a simple sentence.", "です"),
    },
    "jp_n4": {
        "words": [("よてい", "yotei - ke hoach", "あしたのよていがあります。"), ("りゆう", "riyuu - ly do", "りゆうをせつめいします。"), ("てつだう", "tetsudau - giup do", "ともだちをてつだいます。"), ("けいけん", "keiken - kinh nghiem", "日本へいったことがあります。"), ("しゅみ", "shumi - so thich", "しゅみはりょうりです。"), ("びょういん", "byouin - benh vien", "びょういんへいきます。"), ("ゆるす", "yurusu - cho phep", "ここでしゃしんをとってもいいです。"), ("れんらく", "renraku - lien lac", "あとでれんらくします。")],
        "patterns": ["{topic} についてはなしたいです。", "{topic} してもいいですか。", "{topic} したことがあります。"],
        "grammar": ["Use て form for requests and permission.", "Use たことがあります for experience.", "Use から to give a reason."],
        "dialogue": [("A", "{topic} してもいいですか。"), ("B", "はい、いいですよ。"), ("A", "ありがとうございます。")],
        "speaking": ["{topic} してもいいですか。", "{topic} したことがあります。", "どうしてですか。"],
        "quiz": ("Choose the pattern for experience.", "たことがあります"),
    },
    "jp_n3": {
        "words": [("いけん", "iken - y kien", "わたしのいけんをいいます。"), ("せつめい", "setsumei - giai thich", "理由をせつめいします。"), ("しょくば", "shokuba - noi lam viec", "しょくばで話します。"), ("もんだい", "mondai - van de", "もんだいがあります。"), ("ていあん", "teian - de xuat", "新しいていあんです。"), ("れんしゅう", "renshuu - luyen tap", "毎日れんしゅうします。"), ("きもち", "kimochi - cam xuc", "きもちを伝えます。"), ("じょうきょう", "joukyou - tinh hinh", "じょうきょうを説明します。")],
        "patterns": ["{topic} についてどう思いますか。", "{topic} と思います。", "{topic} かもしれません。"],
        "grammar": ["Use と思います to give an opinion.", "Use かもしれません for possibility.", "Use ようです for 'it seems'."],
        "dialogue": [("A", "{topic} についてどう思いますか。"), ("B", "大切だと思います。"), ("A", "どうしてですか。")],
        "speaking": ["{topic} についてどう思いますか。", "大切だと思います。", "もう少し説明します。"],
        "quiz": ("Choose the phrase for giving an opinion.", "と思います"),
    },
    "jp_n2": {
        "words": [("かいぎ", "kaigi - cuoc hop", "会議で報告します。"), ("ほうこく", "houkoku - bao cao", "結果を報告します。"), ("お客様", "okyakusama - khach hang", "お客様に説明します。"), ("課題", "kadai - van de/can lam", "課題を整理します。"), ("提案", "teian - de xuat", "提案をまとめます。"), ("影響", "eikyou - anh huong", "影響があります。"), ("対応", "taiou - xu ly", "すぐ対応します。"), ("確認", "kakunin - xac nhan", "内容を確認します。")],
        "patterns": ["{topic} についてご説明します。", "{topic} による影響があります。", "{topic} を確認していただけますか。"],
        "grammar": ["Use keigo for polite workplace requests.", "Use による for cause or basis.", "Use いただけますか for polite requests."],
        "dialogue": [("A", "{topic} についてご説明します。"), ("B", "お願いします。"), ("A", "まず、課題を確認します。")],
        "speaking": ["{topic} についてご説明します。", "確認していただけますか。", "すぐ対応いたします。"],
        "quiz": ("Choose a polite request pattern.", "いただけますか"),
    },
    "jp_n1": {
        "words": [("観点", "kanten - goc nhin", "別の観点から考えます。"), ("傾向", "keikou - xu huong", "新しい傾向が見られます。"), ("根拠", "konkyo - can cu", "根拠を示します。"), ("妥当", "datou - thoa dang", "妥当な判断です。"), ("推測", "suisoku - suy doan", "結果を推測します。"), ("課題解決", "kadai kaiketsu - giai quyet van de", "課題解決が必要です。"), ("多様性", "tayousei - da dang", "多様性を尊重します。"), ("持続可能", "jizoku kanou - ben vung", "持続可能な方法です。")],
        "patterns": ["{topic} という観点から考える必要があります。", "{topic} には一定の根拠があります。", "{topic} とは言い切れません。"],
        "grammar": ["Use abstract nouns to make arguments precise.", "Use とは言い切れません to avoid overstatement.", "Use という観点から for perspective."],
        "dialogue": [("A", "{topic} についてどう評価しますか。"), ("B", "別の観点から考える必要があります。"), ("A", "根拠を教えてください。")],
        "speaking": ["{topic} という観点から考えます。", "根拠を示す必要があります。", "一概には言えません。"],
        "quiz": ("Choose the phrase for 'from the perspective of'.", "という観点から"),
    },
}


JAPANESE_PATTERN_SUPPORT = {
    "jp_n5": [
        ("わたしは このテーマ を べんきょうします。", "Tôi học chủ đề này."),
        ("このテーマ は やさしいです。", "Chủ đề này dễ."),
        ("このテーマ は どこですか。", "Chủ đề này ở đâu?"),
    ],
    "jp_n4": [
        ("このテーマ について はなしたいです。", "Tôi muốn nói về chủ đề này."),
        ("このテーマ してもいいですか。", "Tôi có thể làm việc này không?"),
        ("このテーマ したことがあります。", "Tôi đã từng làm việc này."),
    ],
    "jp_n3": [
        ("このテーマ について どうおもいますか。", "Bạn nghĩ gì về chủ đề này?"),
        ("このテーマ だとおもいます。", "Tôi nghĩ là chủ đề này."),
        ("このテーマ かもしれません。", "Có thể là chủ đề này."),
    ],
    "jp_n2": [
        ("このテーマ について ごせつめいします。", "Tôi xin giải thích về chủ đề này."),
        ("このテーマ による えいきょうがあります。", "Có ảnh hưởng do chủ đề này."),
        ("このテーマ を かくにんしていただけますか。", "Bạn có thể xác nhận chủ đề này giúp tôi không?"),
    ],
    "jp_n1": [
        ("このテーマ という かんてんから かんがえる ひつようがあります。", "Cần suy nghĩ từ góc nhìn của chủ đề này."),
        ("このテーマ には いっていの こんきょがあります。", "Chủ đề này có căn cứ nhất định."),
        ("このテーマ とは いいきれません。", "Không thể nói chắc là chủ đề này."),
    ],
}


JAPANESE_DIALOGUE_SUPPORT = {
    "jp_n5": [("こんにちは。", "Xin chào."), ("こんにちは。このテーマをべんきょうしています。", "Xin chào. Tôi đang học chủ đề này."), ("いいですね。", "Hay quá.")],
    "jp_n4": [("このテーマしてもいいですか。", "Tôi có thể làm việc này không?"), ("はい、いいですよ。", "Vâng, được."), ("ありがとうございます。", "Cảm ơn.")],
    "jp_n3": [("このテーマについてどうおもいますか。", "Bạn nghĩ gì về chủ đề này?"), ("たいせつだとおもいます。", "Tôi nghĩ là quan trọng."), ("どうしてですか。", "Tại sao vậy?")],
    "jp_n2": [("このテーマについてごせつめいします。", "Tôi xin giải thích về chủ đề này."), ("おねがいします。", "Vâng, nhờ bạn."), ("まず、かだいをかくにんします。", "Trước hết, tôi xác nhận vấn đề.")],
    "jp_n1": [("このテーマについてどうひょうかしますか。", "Bạn đánh giá chủ đề này như thế nào?"), ("べつのかんてんからかんがえるひつようがあります。", "Cần suy nghĩ từ góc nhìn khác."), ("こんきょをおしえてください。", "Hãy cho tôi biết căn cứ.")],
}


JAPANESE_SPEAKING_SUPPORT = {
    "jp_n5": [("わたしは このテーマ を べんきょうします。", "Tôi học chủ đề này."), ("このテーマ は やさしいです。", "Chủ đề này dễ."), ("もういちど おねがいします。", "Làm ơn nói lại một lần nữa.")],
    "jp_n4": [("このテーマ してもいいですか。", "Tôi có thể làm việc này không?"), ("このテーマ したことがあります。", "Tôi đã từng làm việc này."), ("どうしてですか。", "Tại sao vậy?")],
    "jp_n3": [("このテーマ について どうおもいますか。", "Bạn nghĩ gì về chủ đề này?"), ("たいせつだとおもいます。", "Tôi nghĩ là quan trọng."), ("もうすこし せつめいします。", "Tôi sẽ giải thích thêm một chút.")],
    "jp_n2": [("このテーマ について ごせつめいします。", "Tôi xin giải thích về chủ đề này."), ("かくにんしていただけますか。", "Bạn có thể xác nhận giúp tôi không?"), ("すぐ たいおういたします。", "Tôi sẽ xử lý ngay.")],
    "jp_n1": [("このテーマ という かんてんから かんがえます。", "Tôi suy nghĩ từ góc nhìn của chủ đề này."), ("こんきょを しめす ひつようがあります。", "Cần đưa ra căn cứ."), ("いちがいには いえません。", "Không thể nói một cách tuyệt đối.")],
}


JAPANESE_GRAMMAR_SUPPORT = {
    "jp_n5": [
        "は (wa): dung de danh dau chu de trong cau. Vi du: わたしはアンです。",
        "です (desu): ket thuc cau lich su, nghia gan voi 'la'.",
        "を (o): dung truoc tan ngu cua hanh dong. Vi du: みずをのみます。",
    ],
    "jp_n4": [
        "The て form: dung khi xin phep, nho giup hoac noi cac hanh dong noi tiep.",
        "たことがあります: noi ve trai nghiem da tung lam.",
        "から: dung de neu ly do, giong 'vi/bởi vi' trong tieng Viet.",
    ],
    "jp_n3": [
        "とおもいます: dung de dua ra y kien ca nhan.",
        "かもしれません: dien ta kha nang 'co the'.",
        "ようです: dien ta 'co ve nhu / duong nhu'.",
    ],
    "jp_n2": [
        "Keigo: cach noi lich su trong cong viec, voi khach hang va nguoi tren.",
        "による: noi nguyen nhan, co so hoac tac nhan gay anh huong.",
        "いただけますか: mau cau nho/yeu cau rat lich su.",
    ],
    "jp_n1": [
        "という観点から: noi 'tu goc nhin / theo quan diem'.",
        "とは言い切れません: tranh noi qua chac chan, nghia la 'khong the noi chac rang'.",
        "抽象名詞: danh tu truu tuong giup lap luan chinh xac hon.",
    ],
}


def _split_japanese_meaning(value):
    text = str(value or "")
    if " - " in text:
        reading, vietnamese = text.split(" - ", 1)
        return reading.strip(), vietnamese.strip()
    return "", text.strip()


def _japanese_word_payload(item):
    if isinstance(item, dict):
        return item
    reading, vietnamese = _split_japanese_meaning(item[1])
    return {
        "word": item[0],
        "reading": reading,
        "meaning": vietnamese,
        "translation": vietnamese,
        "example": item[2],
        "exampleReading": item[2],
        "exampleTranslation": f"Câu ví dụ với từ '{vietnamese or item[0]}'.",
    }


JAPANESE_HIRAGANA_LINES = {
    "Hiragana A Line": [
        ("あ", "a", "âm a", "あさ", "asa", "buổi sáng"),
        ("い", "i", "âm i", "いす", "isu", "cái ghế"),
        ("う", "u", "âm u", "うみ", "umi", "biển"),
        ("え", "e", "âm e", "えき", "eki", "nhà ga"),
        ("お", "o", "âm o", "おかね", "okane", "tiền"),
    ],
    "Hiragana K Line": [
        ("か", "ka", "âm ka", "かさ", "kasa", "cái ô"),
        ("き", "ki", "âm ki", "き", "ki", "cây"),
        ("く", "ku", "âm ku", "くつ", "kutsu", "giày"),
        ("け", "ke", "âm ke", "けさ", "kesa", "sáng nay"),
        ("こ", "ko", "âm ko", "こえ", "koe", "giọng nói"),
    ],
    "Hiragana S Line": [
        ("さ", "sa", "âm sa", "さかな", "sakana", "cá"),
        ("し", "shi", "âm shi", "しお", "shio", "muối"),
        ("す", "su", "âm su", "すし", "sushi", "sushi"),
        ("せ", "se", "âm se", "せんせい", "sensei", "giáo viên"),
        ("そ", "so", "âm so", "そら", "sora", "bầu trời"),
    ],
    "Hiragana T Line": [
        ("た", "ta", "âm ta", "たべる", "taberu", "ăn"),
        ("ち", "chi", "âm chi", "ちず", "chizu", "bản đồ"),
        ("つ", "tsu", "âm tsu", "つき", "tsuki", "mặt trăng"),
        ("て", "te", "âm te", "て", "te", "tay"),
        ("と", "to", "âm to", "ともだち", "tomodachi", "bạn bè"),
    ],
    "Hiragana N Line": [
        ("な", "na", "âm na", "なまえ", "namae", "tên"),
        ("に", "ni", "âm ni", "にほん", "nihon", "Nhật Bản"),
        ("ぬ", "nu", "âm nu", "ぬの", "nuno", "vải"),
        ("ね", "ne", "âm ne", "ねこ", "neko", "mèo"),
        ("の", "no", "âm no", "のむ", "nomu", "uống"),
    ],
    "Hiragana H Line": [
        ("は", "ha", "âm ha", "はな", "hana", "hoa"),
        ("ひ", "hi", "âm hi", "ひと", "hito", "người"),
        ("ふ", "fu", "âm fu", "ふね", "fune", "thuyền"),
        ("へ", "he", "âm he", "へや", "heya", "phòng"),
        ("ほ", "ho", "âm ho", "ほん", "hon", "sách"),
    ],
    "Hiragana M Line": [
        ("ま", "ma", "âm ma", "まち", "machi", "thị trấn"),
        ("み", "mi", "âm mi", "みず", "mizu", "nước"),
        ("む", "mu", "âm mu", "むし", "mushi", "côn trùng"),
        ("め", "me", "âm me", "め", "me", "mắt"),
        ("も", "mo", "âm mo", "もの", "mono", "đồ vật"),
    ],
    "Hiragana Y Line": [
        ("や", "ya", "âm ya", "やま", "yama", "núi"),
        ("ゆ", "yu", "âm yu", "ゆき", "yuki", "tuyết"),
        ("よ", "yo", "âm yo", "よる", "yoru", "buổi tối"),
    ],
    "Hiragana R Line": [
        ("ら", "ra", "âm ra", "らいねん", "rainen", "năm sau"),
        ("り", "ri", "âm ri", "りんご", "ringo", "táo"),
        ("る", "ru", "âm ru", "るす", "rusu", "vắng nhà"),
        ("れ", "re", "âm re", "れい", "rei", "ví dụ"),
        ("ろ", "ro", "âm ro", "ろく", "roku", "số sáu"),
    ],
    "Hiragana W Line": [
        ("わ", "wa", "âm wa", "わたし", "watashi", "tôi"),
        ("を", "o", "trợ từ o", "みずをのむ", "mizu o nomu", "uống nước"),
        ("ん", "n", "âm n", "ほん", "hon", "sách"),
    ],
}

HIRAGANA_STROKE_STEPS = {
    "あ": ["Nét 1: ngang ngắn từ trái sang phải.", "Nét 2: kéo dọc xuống rồi cong nhẹ sang trái.", "Nét 3: vòng cong lớn, kết thúc ở dưới bên phải."],
    "い": ["Nét 1: kéo cong xuống bên trái.", "Nét 2: kéo cong xuống bên phải, ngắn hơn nét 1."],
    "う": ["Nét 1: chấm/ngang ngắn ở trên.", "Nét 2: kéo cong từ trái sang phải rồi hạ xuống."],
    "え": ["Nét 1: chấm/ngang ngắn ở trên.", "Nét 2: ngang ngắn, gập xuống rồi kéo sang phải."],
    "お": ["Nét 1: ngang từ trái sang phải.", "Nét 2: kéo dọc xuống, cong vòng sang trái rồi qua phải.", "Nét 3: chấm nhỏ bên phải."],
    "か": ["Nét 1: ngang rồi kéo xuống cong sang trái.", "Nét 2: phẩy chéo từ trên phải xuống dưới trái.", "Nét 3: chấm nhỏ bên phải."],
    "き": ["Nét 1: ngang trên từ trái sang phải.", "Nét 2: ngang dưới từ trái sang phải.", "Nét 3: kéo chéo xuống rồi cong nhẹ."],
    "く": ["Nét 1: một nét gấp khúc từ trên xuống dưới, mở sang trái."],
    "け": ["Nét 1: kéo dọc bên trái.", "Nét 2: ngang ngắn bên phải.", "Nét 3: kéo dọc xuống rồi cong nhẹ."],
    "こ": ["Nét 1: ngang trên hơi cong.", "Nét 2: ngang dưới hơi cong."],
    "さ": ["Nét 1: ngang trên từ trái sang phải.", "Nét 2: kéo chéo xuống.", "Nét 3: nét cong ngắn ở dưới."],
    "し": ["Nét 1: kéo cong từ trên xuống dưới rồi hất nhẹ sang phải."],
    "す": ["Nét 1: ngang từ trái sang phải.", "Nét 2: kéo xuống qua giữa, tạo vòng nhỏ rồi cong xuống."],
    "せ": ["Nét 1: ngang dài từ trái sang phải.", "Nét 2: dọc ngắn bên trái.", "Nét 3: dọc bên phải rồi cong nhẹ."],
    "そ": ["Nét 1: một nét liền: ngang, gập chéo xuống rồi cong sang phải."],
    "た": ["Nét 1: ngang trên.", "Nét 2: kéo dọc xuống cắt nét 1.", "Nét 3: ngang nhỏ bên phải.", "Nét 4: cong dưới bên phải."],
    "ち": ["Nét 1: ngang từ trái sang phải.", "Nét 2: kéo dọc xuống rồi cong lớn sang phải."],
    "つ": ["Nét 1: cong dài từ trái sang phải, hạ xuống nhẹ."],
    "て": ["Nét 1: ngang ngắn rồi kéo cong xuống sang trái."],
    "と": ["Nét 1: nét ngắn chéo xuống.", "Nét 2: cong dài từ trái sang phải."],
    "な": ["Nét 1: ngang trên.", "Nét 2: dọc xuống cắt nét 1.", "Nét 3: chấm nhỏ bên phải.", "Nét 4: cong dưới tạo đuôi."],
    "に": ["Nét 1: kéo dọc bên trái.", "Nét 2: ngang ngắn bên phải.", "Nét 3: ngang dưới bên phải."],
    "ぬ": ["Nét 1: cong từ trên trái xuống rồi vòng sang phải.", "Nét 2: vòng nhỏ ở giữa, kết thúc hất nhẹ."],
    "ね": ["Nét 1: dọc bên trái, có móc nhẹ.", "Nét 2: từ giữa kéo sang phải, vòng xuống rồi hất lên."],
    "の": ["Nét 1: một vòng cong từ trên phải xuống trái rồi quay sang phải."],
    "は": ["Nét 1: kéo dọc bên trái.", "Nét 2: ngang ngắn bên phải.", "Nét 3: dọc xuống rồi cong tạo vòng nhỏ."],
    "ひ": ["Nét 1: cong dài từ trên trái xuống rồi lên nhẹ bên phải."],
    "ふ": ["Nét 1: chấm/ngắn ở trên.", "Nét 2: cong chính ở giữa.", "Nét 3: chấm nhỏ bên trái.", "Nét 4: chấm nhỏ bên phải."],
    "へ": ["Nét 1: gấp khúc một nét, lên nhẹ rồi xuống sang phải."],
    "ほ": ["Nét 1: kéo dọc bên trái.", "Nét 2: ngang trên bên phải.", "Nét 3: ngang giữa bên phải.", "Nét 4: dọc xuống rồi cong tạo vòng."],
    "ま": ["Nét 1: ngang trên.", "Nét 2: ngang dưới.", "Nét 3: dọc xuống rồi vòng cong ở dưới."],
    "み": ["Nét 1: cong từ trái xuống rồi vòng lên.", "Nét 2: nét nhỏ kéo xuống bên phải."],
    "む": ["Nét 1: ngang ngắn.", "Nét 2: dọc xuống rồi vòng lớn.", "Nét 3: chấm nhỏ bên phải."],
    "め": ["Nét 1: cong từ trên trái xuống.", "Nét 2: vòng lớn từ phải sang trái rồi kết thúc bên phải."],
    "も": ["Nét 1: dọc cong xuống.", "Nét 2: ngang trên.", "Nét 3: ngang dưới."],
    "や": ["Nét 1: cong chéo từ trái sang phải.", "Nét 2: nét ngắn chéo ở trên.", "Nét 3: dọc xuống qua giữa."],
    "ゆ": ["Nét 1: cong lớn từ trái xuống và vòng lại.", "Nét 2: dọc cong bên phải."],
    "よ": ["Nét 1: ngang ngắn trên.", "Nét 2: dọc xuống rồi vòng sang phải."],
    "ら": ["Nét 1: ngang ngắn trên.", "Nét 2: cong xuống rồi vòng sang phải."],
    "り": ["Nét 1: kéo dọc cong bên trái.", "Nét 2: kéo dọc cong bên phải, dài hơn."],
    "る": ["Nét 1: một nét cong xuống, vòng nhỏ ở cuối."],
    "れ": ["Nét 1: dọc bên trái có móc nhẹ.", "Nét 2: kéo sang phải rồi cong xuống."],
    "ろ": ["Nét 1: một nét cong xuống rồi vòng ngang ở dưới."],
    "わ": ["Nét 1: dọc bên trái có móc nhẹ.", "Nét 2: kéo sang phải rồi vòng xuống."],
    "を": ["Nét 1: ngang trên.", "Nét 2: kéo dọc xuống rồi cong.", "Nét 3: cong dài phía dưới sang phải."],
    "ん": ["Nét 1: một nét cong từ trên trái xuống rồi hất sang phải."],
}


def _hiragana_stroke_steps(kana):
    return HIRAGANA_STROKE_STEPS.get(kana, ["Viết theo mẫu từ trên xuống dưới, trái sang phải."])


def _japanese_alphabet_spec(topic):
    cards = JAPANESE_HIRAGANA_LINES.get(topic)
    if not cards:
        return None
    words = [
        {
            "word": kana,
            "reading": f"{kana} / {romaji}",
            "meaning": vietnamese,
            "translation": vietnamese,
            "example": example,
            "exampleReading": f"{example} / {example_romaji}",
            "exampleTranslation": example_vi,
        }
        for kana, romaji, vietnamese, example, example_romaji, example_vi in cards
    ]
    first = words[0]
    second = words[1] if len(words) > 1 else first
    patterns = [
        {"text": f"{first['word']} は {first['word']} と よみます。", "reading": f"{cards[0][1]} wa {cards[0][1]} to yomimasu", "translation": f"Chữ {first['word']} đọc là {cards[0][1]}."},
        {"text": f"{second['word']} を さんかい かきます。", "reading": f"{cards[1][1] if len(cards) > 1 else cards[0][1]} o san-kai kakimasu", "translation": f"Viết chữ {second['word']} 3 lần."},
        {"text": "みて、 よんで、 かきます。", "reading": "mite yonde kakimasu", "translation": "Nhìn, đọc rồi viết."},
    ]
    grammar = [
        "Bước 1: nhìn chữ Hiragana và đọc to romaji.",
        "Bước 2: che romaji, nhìn chữ và tự đọc lại.",
        "Bước 3: viết mỗi chữ 3 lần theo thứ tự từ trên xuống, trái sang phải.",
        "Mục tiêu bài này: nhận mặt chữ nhanh, chưa cần dùng AI.",
    ]
    dialogue = [
        {"speaker": "Ms. Sakura", "text": "いっしょに ひらがなを よみましょう。", "reading": "issho-ni hiragana-o yomimashou", "translation": "Mình cùng đọc Hiragana nhé."},
        {"speaker": "You", "text": f"{first['word']} は {first['word']} です。", "reading": f"{cards[0][1]} wa {cards[0][1]} desu", "translation": f"Chữ {first['word']} là âm {cards[0][1]}."},
        {"speaker": "Ms. Sakura", "text": "いいですね。 つぎは かきましょう。", "reading": "ii-desu-ne tsugi-wa kakimashou", "translation": "Tốt lắm. Tiếp theo mình viết nhé."},
    ]
    speaking = [
        {"text": kana, "reading": f"{kana} / {romaji}", "translation": f"Đọc âm {romaji}"}
        for kana, romaji, *_ in cards[:3]
    ]
    choices = [card[1] for card in cards]
    game_prompts = []
    for kana, romaji, vietnamese, *_ in cards:
        wrong_choices = [choice for choice in choices if choice != romaji][:2]
        game_prompts.append({
            "kana": kana,
            "answer": romaji,
            "choices": [romaji] + wrong_choices,
            "hint": vietnamese,
        })
    extra_content = {
        "alphabetPractice": {
            "title": topic,
            "script": "hiragana",
            "cards": [
                {
                    "kana": kana,
                    "romaji": romaji,
                    "vietnamese": vietnamese,
                    "example": example,
                    "exampleReading": example_romaji,
                    "exampleTranslation": example_vi,
                    "strokeSteps": _hiragana_stroke_steps(kana),
                    "strokeCount": len(_hiragana_stroke_steps(kana)),
                    "strokeHint": "Viết chậm 3 lần, đọc thành tiếng sau mỗi lần viết.",
                }
                for kana, romaji, vietnamese, example, example_romaji, example_vi in cards
            ],
            "gamePrompts": game_prompts,
            "writingTips": [
                "Nhìn chữ 2 giây rồi che lại để viết từ trí nhớ.",
                "Đọc to romaji trước khi viết để não nối âm với mặt chữ.",
                "Nếu sai, viết lại ngay 1 lần, không cần dùng AI.",
            ],
        }
    }
    return (topic, f"{topic} - Read and Write", words, patterns, grammar, dialogue, speaking, f"How do you read {first['word']}?||{cards[0][1]}", extra_content)


JAPANESE_INTRO_LESSONS = {
    "Dakuten G and Z Sounds": {
        "title": "Dakuten: G and Z Sounds",
        "words": [
            ("が", "ga", "âm ga", "がくせいです。", "gakusei desu", "Tôi là học sinh/sinh viên."),
            ("ぎ", "gi", "âm gi", "ぎんこうです。", "ginkou desu", "Đó là ngân hàng."),
            ("ぐ", "gu", "âm gu", "ぐあいが いいです。", "guai ga ii desu", "Tình trạng/cảm giác ổn."),
            ("げ", "ge", "âm ge", "げんきです。", "genki desu", "Tôi khỏe."),
            ("ご", "go", "âm go / số 5", "ごです。", "go desu", "Đây là số 5."),
            ("ざ", "za", "âm za", "ざっしです。", "zasshi desu", "Đó là tạp chí."),
            ("じ", "ji", "âm ji", "じかんです。", "jikan desu", "Đó là thời gian."),
            ("ず", "zu", "âm zu", "ずっとです。", "zutto desu", "Liên tục/mãi."),
            ("ぜ", "ze", "âm ze", "ぜんぶです。", "zenbu desu", "Là tất cả."),
            ("ぞ", "zo", "âm zo", "どうぞ。", "douzo", "Xin mời."),
        ],
        "patterns": [
            ("か に てんてん で が。", "ka ni ten-ten de ga", "Thêm dấu ten-ten vào か thành が."),
            ("ご は ご と よみます。", "go wa go to yomimasu", "Chữ ご đọc là go."),
            ("どうぞ。", "douzo", "Xin mời."),
        ],
    },
    "Dakuten D B P Sounds": {
        "title": "Dakuten: D, B and P Sounds",
        "words": [
            ("だ", "da", "âm da", "だいじょうぶです。", "daijoubu desu", "Không sao / ổn ạ."),
            ("ぢ", "ji", "âm ji hiếm", "ぢ は じ に にています。", "ji wa ji ni niteimasu", "ぢ giống âm じ."),
            ("づ", "zu", "âm zu hiếm", "づ は ず に にています。", "zu wa zu ni niteimasu", "づ giống âm ず."),
            ("で", "de", "âm de", "でんしゃです。", "densha desu", "Đó là tàu điện."),
            ("ど", "do", "âm do", "どうぞ。", "douzo", "Xin mời."),
            ("ば", "ba", "âm ba", "ばんごうです。", "bangou desu", "Đó là số."),
            ("び", "bi", "âm bi", "びょういんです。", "byouin desu", "Đó là bệnh viện."),
            ("ぶ", "bu", "âm bu", "ぶんです。", "bun desu", "Đó là câu."),
            ("べ", "be", "âm be", "べんきょうします。", "benkyou shimasu", "Tôi học."),
            ("ぼ", "bo", "âm bo", "ぼうしです。", "boushi desu", "Đó là cái mũ."),
            ("ぱ", "pa", "âm pa", "パンです。", "pan desu", "Đó là bánh mì."),
            ("ぴ", "pi", "âm pi", "ピンクです。", "pinku desu", "Màu hồng."),
            ("ぷ", "pu", "âm pu", "プールです。", "puuru desu", "Đó là hồ bơi."),
            ("ぺ", "pe", "âm pe", "ペンです。", "pen desu", "Đó là cây bút."),
            ("ぽ", "po", "âm po", "ポケットです。", "poketto desu", "Đó là túi áo/quần."),
        ],
        "patterns": [
            ("た に てんてん で だ。", "ta ni ten-ten de da", "Thêm ten-ten vào た thành だ."),
            ("は に てんてん で ば。", "ha ni ten-ten de ba", "Thêm ten-ten vào は thành ば."),
            ("は に まる で ぱ。", "ha ni maru de pa", "Thêm dấu tròn vào は thành ぱ."),
        ],
    },
    "Small Ya Yu Yo Sounds": {
        "title": "Small や・ゆ・よ Combinations",
        "words": [
            ("きゃ", "kya", "âm kya", "きゃくです。", "kyaku desu", "Đó là khách."),
            ("きゅ", "kyu", "âm kyu", "きゅうです。", "kyuu desu", "Đó là số 9."),
            ("きょ", "kyo", "âm kyo", "きょうです。", "kyou desu", "Hôm nay."),
            ("しゃ", "sha", "âm sha", "しゃしんです。", "shashin desu", "Đó là ảnh."),
            ("しゅ", "shu", "âm shu", "しゅくだいです。", "shukudai desu", "Đó là bài tập về nhà."),
            ("しょ", "sho", "âm sho", "しょくどうです。", "shokudou desu", "Đó là nhà ăn."),
            ("ちゃ", "cha", "âm cha", "おちゃです。", "ocha desu", "Đó là trà."),
            ("ちゅ", "chu", "âm chu", "ちゅういです。", "chuui desu", "Chú ý."),
            ("ちょ", "cho", "âm cho", "ちょっと。", "chotto", "Một chút / chờ chút."),
            ("にゃ", "nya", "âm nya", "にゃ と よみます。", "nya to yomimasu", "Đọc là nya."),
            ("りゃ", "rya", "âm rya", "りゃ と よみます。", "rya to yomimasu", "Đọc là rya."),
            ("りょ", "ryo", "âm ryo", "りょうりです。", "ryouri desu", "Đó là món ăn/nấu ăn."),
        ],
        "patterns": [
            ("き + や nhỏ = きゃ。", "ki + small ya = kya", "き ghép ゃ nhỏ thành きゃ."),
            ("し + ゆ nhỏ = しゅ。", "shi + small yu = shu", "し ghép ゅ nhỏ thành しゅ."),
            ("ちょっと まってください。", "chotto matte kudasai", "Xin chờ một chút."),
        ],
    },
    "Numbers 0 to 10": {
        "title": "Numbers 0-10",
        "words": [
            ("ゼロ", "zero", "số 0", "ゼロです。", "zero desu", "Đây là số 0."),
            ("いち", "ichi", "số 1", "いちです。", "ichi desu", "Đây là số 1."),
            ("に", "ni", "số 2", "にです。", "ni desu", "Đây là số 2."),
            ("さん", "san", "số 3", "さんです。", "san desu", "Đây là số 3."),
            ("よん", "yon", "số 4", "よんです。", "yon desu", "Đây là số 4."),
            ("ご", "go", "số 5", "ごです。", "go desu", "Đây là số 5."),
            ("ろく", "roku", "số 6", "ろくです。", "roku desu", "Đây là số 6."),
            ("なな", "nana", "số 7", "ななです。", "nana desu", "Đây là số 7."),
            ("はち", "hachi", "số 8", "はちです。", "hachi desu", "Đây là số 8."),
            ("きゅう", "kyuu", "số 9", "きゅうです。", "kyuu desu", "Đây là số 9."),
            ("じゅう", "juu", "số 10", "じゅうです。", "juu desu", "Đây là số 10."),
        ],
        "patterns": [
            ("いち、に、さん。", "ichi, ni, san", "Một, hai, ba."),
            ("これは ご です。", "kore wa go desu", "Đây là số 5."),
            ("もういちど おねがいします。", "mou ichido onegaishimasu", "Làm ơn nói lại một lần nữa."),
        ],
    },
    "Numbers 11 to 100": {
        "title": "Numbers 11-100",
        "words": [
            ("じゅういち", "juu-ichi", "số 11", "じゅういちです。", "juu-ichi desu", "Đây là số 11."),
            ("じゅうに", "juu-ni", "số 12", "じゅうにです。", "juu-ni desu", "Đây là số 12."),
            ("にじゅう", "ni-juu", "số 20", "にじゅうです。", "ni-juu desu", "Đây là số 20."),
            ("さんじゅう", "san-juu", "số 30", "さんじゅうです。", "san-juu desu", "Đây là số 30."),
            ("ごじゅう", "go-juu", "số 50", "ごじゅうです。", "go-juu desu", "Đây là số 50."),
            ("ひゃく", "hyaku", "số 100", "ひゃくです。", "hyaku desu", "Đây là số 100."),
        ],
        "patterns": [
            ("じゅう + いち = じゅういち。", "juu + ichi = juu-ichi", "10 + 1 = 11."),
            ("に + じゅう = にじゅう。", "ni + juu = ni-juu", "2 x 10 = 20."),
            ("これは さんじゅう です。", "kore wa san-juu desu", "Đây là số 30."),
        ],
    },
    "Days of Week": {
        "title": "Days of the Week",
        "words": [
            ("げつようび", "getsuyoubi", "thứ Hai", "げつようびに べんきょうします。", "getsuyoubi ni benkyou shimasu", "Tôi học vào thứ Hai."),
            ("かようび", "kayoubi", "thứ Ba", "かようびです。", "kayoubi desu", "Hôm nay là thứ Ba."),
            ("すいようび", "suiyoubi", "thứ Tư", "すいようびに あいます。", "suiyoubi ni aimasu", "Gặp nhau vào thứ Tư."),
            ("もくようび", "mokuyoubi", "thứ Năm", "もくようびです。", "mokuyoubi desu", "Hôm nay là thứ Năm."),
            ("きんようび", "kinyoubi", "thứ Sáu", "きんようびに いきます。", "kinyoubi ni ikimasu", "Tôi đi vào thứ Sáu."),
            ("どようび", "doyoubi", "thứ Bảy", "どようびは やすみです。", "doyoubi wa yasumi desu", "Thứ Bảy là ngày nghỉ."),
            ("にちようび", "nichiyoubi", "Chủ nhật", "にちようびは やすみです。", "nichiyoubi wa yasumi desu", "Chủ nhật là ngày nghỉ."),
        ],
        "patterns": [
            ("きょうは げつようび です。", "kyou wa getsuyoubi desu", "Hôm nay là thứ Hai."),
            ("にちようびは やすみです。", "nichiyoubi wa yasumi desu", "Chủ nhật là ngày nghỉ."),
            ("なんようび ですか。", "nan-youbi desu ka", "Hôm nay là thứ mấy?"),
        ],
    },
    "Months of Year": {
        "title": "Months of the Year",
        "words": [
            ("いちがつ", "ichigatsu", "tháng 1", "いちがつです。", "ichigatsu desu", "Là tháng 1."),
            ("にがつ", "nigatsu", "tháng 2", "にがつです。", "nigatsu desu", "Là tháng 2."),
            ("さんがつ", "sangatsu", "tháng 3", "さんがつです。", "sangatsu desu", "Là tháng 3."),
            ("しがつ", "shigatsu", "tháng 4", "しがつです。", "shigatsu desu", "Là tháng 4."),
            ("ごがつ", "gogatsu", "tháng 5", "ごがつです。", "gogatsu desu", "Là tháng 5."),
            ("ろくがつ", "rokugatsu", "tháng 6", "ろくがつです。", "rokugatsu desu", "Là tháng 6."),
            ("しちがつ", "shichigatsu", "tháng 7", "しちがつです。", "shichigatsu desu", "Là tháng 7."),
            ("はちがつ", "hachigatsu", "tháng 8", "はちがつです。", "hachigatsu desu", "Là tháng 8."),
            ("くがつ", "kugatsu", "tháng 9", "くがつです。", "kugatsu desu", "Là tháng 9."),
            ("じゅうがつ", "juugatsu", "tháng 10", "じゅうがつです。", "juugatsu desu", "Là tháng 10."),
            ("じゅういちがつ", "juuichigatsu", "tháng 11", "じゅういちがつです。", "juuichigatsu desu", "Là tháng 11."),
            ("じゅうにがつ", "juunigatsu", "tháng 12", "じゅうにがつです。", "juunigatsu desu", "Là tháng 12."),
        ],
        "patterns": [
            ("いまは ごがつ です。", "ima wa gogatsu desu", "Bây giờ là tháng 5."),
            ("なんがつ ですか。", "nan-gatsu desu ka", "Là tháng mấy?"),
            ("わたしの たんじょうびは しがつ です。", "watashi no tanjoubi wa shigatsu desu", "Sinh nhật của tôi vào tháng 4."),
        ],
    },
    "Dates and Calendar": {
        "title": "Dates and Calendar",
        "words": [
            ("きょう", "kyou", "hôm nay", "きょうは げつようびです。", "kyou wa getsuyoubi desu", "Hôm nay là thứ Hai."),
            ("あした", "ashita", "ngày mai", "あした あいます。", "ashita aimasu", "Ngày mai gặp nhau."),
            ("きのう", "kinou", "hôm qua", "きのう べんきょうしました。", "kinou benkyou shimashita", "Hôm qua tôi đã học."),
            ("ついたち", "tsuitachi", "ngày 1", "ついたちです。", "tsuitachi desu", "Là ngày 1."),
            ("ふつか", "futsuka", "ngày 2", "ふつかです。", "futsuka desu", "Là ngày 2."),
            ("さんにち", "san-nichi", "ngày 3", "さんにちです。", "san-nichi desu", "Là ngày 3."),
        ],
        "patterns": [
            ("きょうは なんにち ですか。", "kyou wa nan-nichi desu ka", "Hôm nay là ngày mấy?"),
            ("きょうは いつですか。", "kyou wa itsu desu ka", "Hôm nay là khi nào/ngày nào?"),
            ("あした べんきょうします。", "ashita benkyou shimasu", "Ngày mai tôi học."),
        ],
    },
    "Daily Greetings": {
        "title": "Daily Greetings",
        "words": [
            ("おはよう", "ohayou", "chào buổi sáng thân mật", "おはよう。", "ohayou", "Chào buổi sáng."),
            ("おはようございます", "ohayou gozaimasu", "chào buổi sáng lịch sự", "おはようございます。", "ohayou gozaimasu", "Chào buổi sáng ạ."),
            ("こんにちは", "konnichiwa", "xin chào", "こんにちは。", "konnichiwa", "Xin chào."),
            ("こんばんは", "konbanwa", "chào buổi tối", "こんばんは。", "konbanwa", "Chào buổi tối."),
            ("さようなら", "sayounara", "tạm biệt", "さようなら。", "sayounara", "Tạm biệt."),
        ],
        "patterns": [
            ("こんにちは。わたしは アンです。", "konnichiwa. watashi wa An desu", "Xin chào. Tôi là An."),
            ("おはようございます。", "ohayou gozaimasu", "Chào buổi sáng ạ."),
            ("また あした。", "mata ashita", "Hẹn gặp ngày mai."),
        ],
    },
    "Thank You and Sorry": {
        "title": "Thank You and Sorry",
        "words": [
            ("ありがとう", "arigatou", "cảm ơn thân mật", "ありがとう。", "arigatou", "Cảm ơn."),
            ("ありがとうございます", "arigatou gozaimasu", "cảm ơn lịch sự", "ありがとうございます。", "arigatou gozaimasu", "Cảm ơn ạ."),
            ("すみません", "sumimasen", "xin lỗi / làm phiền", "すみません。", "sumimasen", "Xin lỗi / cho tôi hỏi."),
            ("ごめんなさい", "gomen nasai", "xin lỗi", "ごめんなさい。", "gomen nasai", "Tôi xin lỗi."),
            ("だいじょうぶ", "daijoubu", "không sao / ổn", "だいじょうぶです。", "daijoubu desu", "Không sao / ổn ạ."),
        ],
        "patterns": [
            ("ありがとうございます。", "arigatou gozaimasu", "Cảm ơn ạ."),
            ("すみません、もういちど。", "sumimasen, mou ichido", "Xin lỗi, nói lại một lần nữa."),
            ("だいじょうぶです。", "daijoubu desu", "Không sao ạ."),
        ],
    },
    "Simple Self Introduction": {
        "title": "Simple Self Introduction",
        "words": [
            ("わたし", "watashi", "tôi", "わたしは アンです。", "watashi wa An desu", "Tôi là An."),
            ("なまえ", "namae", "tên", "なまえは アンです。", "namae wa An desu", "Tên tôi là An."),
            ("ベトナム", "betonamu", "Việt Nam", "ベトナムから きました。", "betonamu kara kimashita", "Tôi đến từ Việt Nam."),
            ("よろしく", "yoroshiku", "mong được giúp đỡ", "よろしく おねがいします。", "yoroshiku onegaishimasu", "Rất mong được giúp đỡ."),
            ("がくせい", "gakusei", "học sinh/sinh viên", "がくせいです。", "gakusei desu", "Tôi là học sinh/sinh viên."),
        ],
        "patterns": [
            ("わたしは アンです。", "watashi wa An desu", "Tôi là An."),
            ("ベトナムから きました。", "betonamu kara kimashita", "Tôi đến từ Việt Nam."),
            ("よろしく おねがいします。", "yoroshiku onegaishimasu", "Rất mong được giúp đỡ."),
        ],
    },
    "Classroom Survival": {
        "title": "Classroom Survival",
        "words": [
            ("もういちど", "mou ichido", "một lần nữa", "もういちど おねがいします。", "mou ichido onegaishimasu", "Làm ơn nói lại một lần nữa."),
            ("ゆっくり", "yukkuri", "chậm", "ゆっくり おねがいします。", "yukkuri onegaishimasu", "Làm ơn nói chậm lại."),
            ("わかります", "wakarimasu", "hiểu", "わかります。", "wakarimasu", "Tôi hiểu."),
            ("わかりません", "wakarimasen", "không hiểu", "わかりません。", "wakarimasen", "Tôi không hiểu."),
            ("これは なんですか", "kore wa nan desu ka", "đây là gì?", "これは なんですか。", "kore wa nan desu ka", "Đây là gì?"),
        ],
        "patterns": [
            ("ゆっくり おねがいします。", "yukkuri onegaishimasu", "Làm ơn nói chậm lại."),
            ("わかりません。", "wakarimasen", "Tôi không hiểu."),
            ("これは なんですか。", "kore wa nan desu ka", "Đây là gì?"),
        ],
    },
    "Starter Review": {
        "title": "Japanese Starter Review",
        "words": [
            ("ひらがな", "hiragana", "bảng chữ Hiragana", "ひらがなを よみます。", "hiragana o yomimasu", "Tôi đọc Hiragana."),
            ("すうじ", "suuji", "số", "すうじを よみます。", "suuji o yomimasu", "Tôi đọc số."),
            ("ようび", "youbi", "thứ trong tuần", "なんようびですか。", "nan-youbi desu ka", "Hôm nay là thứ mấy?"),
            ("あいさつ", "aisatsu", "chào hỏi", "あいさつを します。", "aisatsu o shimasu", "Tôi chào hỏi."),
            ("れんしゅう", "renshuu", "luyện tập", "まいにち れんしゅうします。", "mainichi renshuu shimasu", "Tôi luyện tập mỗi ngày."),
        ],
        "patterns": [
            ("ひらがなを よみます。", "hiragana o yomimasu", "Tôi đọc Hiragana."),
            ("すうじを いいます。", "suuji o iimasu", "Tôi nói số."),
            ("まいにち れんしゅうします。", "mainichi renshuu shimasu", "Tôi luyện tập mỗi ngày."),
        ],
    },
}


def _japanese_intro_spec(topic):
    data = JAPANESE_INTRO_LESSONS.get(topic)
    if not data:
        return None
    words = [
        {
            "word": word,
            "reading": f"{word} / {reading}",
            "meaning": meaning,
            "translation": meaning,
            "example": example,
            "exampleReading": f"{example} / {example_reading}",
            "exampleTranslation": example_translation,
        }
        for word, reading, meaning, example, example_reading, example_translation in data["words"]
    ]
    patterns = [
        {"text": text, "reading": reading, "translation": translation}
        for text, reading, translation in data["patterns"]
    ]
    grammar = [
        "Nghe - nhìn chữ - đọc romaji - nói lại. Phần này ưu tiên ghi nhớ, không cần AI.",
        "Học theo cụm ngắn trước, sau đó mới ghép câu dài.",
        "Mỗi bài chỉ cần nhớ chắc 3-5 mẫu dùng hằng ngày.",
    ]
    dialogue = [
        {"speaker": "Ms. Sakura", "text": "いっしょに れんしゅうしましょう。", "reading": "issho ni renshuu shimashou", "translation": "Mình cùng luyện nhé."},
        {"speaker": "You", "text": patterns[0]["text"], "reading": patterns[0]["reading"], "translation": patterns[0]["translation"]},
        {"speaker": "Ms. Sakura", "text": "いいですね。もういちど。", "reading": "ii desu ne. mou ichido", "translation": "Tốt lắm. Thêm một lần nữa nhé."},
    ]
    speaking = patterns[:3]
    extra_content = {
        "alphabetPractice": {
            "title": data["title"],
            "script": "intro",
            "cards": [
                {
                    "kana": item["word"],
                    "romaji": item["reading"].split(" / ", 1)[-1],
                    "vietnamese": item["meaning"],
                    "example": item["example"],
                    "exampleReading": item["exampleReading"].split(" / ", 1)[-1],
                    "exampleTranslation": item["exampleTranslation"],
                    "strokeHint": "Nhìn - đọc - che lại - nói lại 3 lần.",
                }
                for item in words[:6]
            ],
            "gamePrompts": [
                {
                    "kana": item["word"],
                    "answer": item["reading"].split(" / ", 1)[-1],
                    "choices": [item["reading"].split(" / ", 1)[-1]] + [
                        other["reading"].split(" / ", 1)[-1] for other in words[:6] if other["word"] != item["word"]
                    ][:2],
                    "hint": item["meaning"],
                }
                for item in words[:6]
            ],
            "writingTips": [
                "Chơi game chọn đáp án trước để nhớ mặt chữ/cụm.",
                "Sau đó đọc to ví dụ tiếng Nhật và nhìn nghĩa tiếng Việt.",
                "Không dùng AI cho bước ghi nhớ cơ bản này.",
            ],
        }
    }
    return (topic, data["title"], words[:6], patterns, grammar, dialogue, speaking, f"How do you say '{words[0]['meaning']}'?||{words[0]['word']}", extra_content)


def _japanese_topic_spec(level_id, topic, idx):
    alphabet_spec = _japanese_alphabet_spec(topic)
    if alphabet_spec:
        return alphabet_spec
    if level_id == "jp_intro":
        intro_spec = _japanese_intro_spec(topic)
        if intro_spec:
            return intro_spec
    profile = JAPANESE_CONTENT_PROFILES[level_id]
    pool = profile["words"]
    topic_word = {
        "word": "テーマ",
        "reading": "てーま / teema",
        "meaning": f"chu de: {topic}",
        "translation": f"chu de: {topic}",
        "example": "このテーマをべんきょうします。",
        "exampleReading": "このテーマをべんきょうします。 / kono teema o benkyou shimasu",
        "exampleTranslation": f"Toi hoc chu de {topic}.",
    }
    words = [topic_word] + [
        _japanese_word_payload(pool[(idx + offset) % len(pool)])
        for offset in range(4)
    ]
    pattern_support = JAPANESE_PATTERN_SUPPORT.get(level_id, [])
    patterns = []
    for pattern_idx, pattern in enumerate(profile["patterns"]):
        reading, translation = pattern_support[pattern_idx] if pattern_idx < len(pattern_support) else ("", "")
        patterns.append({
            "text": pattern.format(topic="このテーマ"),
            "reading": reading,
            "translation": translation,
        })
    grammar = JAPANESE_GRAMMAR_SUPPORT.get(level_id, list(profile["grammar"]))
    dialogue_support = JAPANESE_DIALOGUE_SUPPORT.get(level_id, [])
    dialogue = []
    for line_idx, (speaker, text) in enumerate(profile["dialogue"]):
        reading, translation = dialogue_support[line_idx] if line_idx < len(dialogue_support) else ("", "")
        dialogue.append({
            "speaker": speaker,
            "text": text.format(topic="このテーマ"),
            "reading": reading,
            "translation": translation,
        })
    speaking_support = JAPANESE_SPEAKING_SUPPORT.get(level_id, [])
    speaking = []
    for speech_idx, text in enumerate(profile["speaking"]):
        reading, translation = speaking_support[speech_idx] if speech_idx < len(speaking_support) else ("", "")
        speaking.append({
            "text": text.format(topic="このテーマ"),
            "reading": reading,
            "translation": translation,
        })
    quiz_prompt, quiz_answer = profile["quiz"]
    return (topic, topic, words, patterns, grammar, dialogue, speaking, f"{quiz_prompt}||{quiz_answer}")


for level_id, topics in JAPANESE_LEVEL_TOPICS.items():
    level_title = next((level["title"] for level in ROADMAP_LEVELS if level["id"] == level_id), level_id.upper())
    ROADMAP_UNITS += _build_units(level_id, level_title, [
        _japanese_topic_spec(level_id, topic, idx)
        for idx, topic in enumerate(topics)
    ])


SKILL_SEQUENCE = ["vocabulary", "grammar", "listening", "reading", "writing"]


def _entry_text(entry, *keys, fallback=""):
    if isinstance(entry, dict):
        for key in keys:
            value = entry.get(key)
            if value:
                return str(value)
        return fallback
    if isinstance(entry, (list, tuple)) and entry:
        return str(entry[0])
    return str(entry or fallback)


def _lesson_words_for_skill(content, topic):
    vocab = content.get("vocabulary") or []
    words = []
    for item in vocab[:5]:
        word = _entry_text(item, "word", "text", fallback=topic)
        meaning = _entry_text(item, "meaning", "translation", fallback=word)
        words.append((word, meaning))
    while len(words) < 3:
        words.append((topic, topic))
    return words[:5]


def _lesson_topic_vi(content, topic):
    vocab = content.get("vocabulary") or []
    if vocab:
        return _entry_text(vocab[0], "meaning", "translation", fallback=topic)
    return topic


def _merge_missing_skill_extra(content, extra):
    for key, value in extra.items():
        if key == "skillFocus":
            content[key] = value
        elif not content.get(key):
            content[key] = value


def _english_skill_extra(skill, lesson, content):
    if skill == "vocabulary":
        return {"skillFocus": "vocabulary"}
    topic = str(lesson.get("topic") or lesson.get("title") or "this topic").lower()
    topic_vi = _lesson_topic_vi(content, topic)
    words = _lesson_words_for_skill(content, topic)
    return _advanced_skill_extra({"skill": skill}, topic, words, topic_vi)


def _jp_reading(item, fallback=""):
    if isinstance(item, dict):
        return item.get("reading") or item.get("exampleReading") or item.get("romaji") or fallback
    if isinstance(item, (list, tuple)) and len(item) > 3:
        return item[3]
    return fallback


def _japanese_skill_extra(skill, lesson, content):
    topic = str(lesson.get("topic") or lesson.get("title") or "Japanese")
    vocab = content.get("vocabulary") or []
    primary = vocab[0] if vocab else {"word": topic, "meaning": topic, "reading": topic}
    second = vocab[1] if len(vocab) > 1 else primary
    third = vocab[2] if len(vocab) > 2 else second

    word1 = _entry_text(primary, "word", "text", fallback=topic)
    word2 = _entry_text(second, "word", "text", fallback=topic)
    word3 = _entry_text(third, "word", "text", fallback=topic)
    read1 = _jp_reading(primary, word1)
    read2 = _jp_reading(second, word2)
    read3 = _jp_reading(third, word3)
    mean1 = _entry_text(primary, "meaning", "translation", fallback=word1)
    mean2 = _entry_text(second, "meaning", "translation", fallback=word2)
    mean3 = _entry_text(third, "meaning", "translation", fallback=word3)

    if skill == "vocabulary":
        return {"skillFocus": "vocabulary"}

    if skill == "grammar":
        return {
            "skillFocus": "grammar",
            "grammarPractice": {
                "title": "Grammar practice",
                "translation": "Luyện mẫu câu tiếng Nhật",
                "examples": [
                    {"text": f"{word1} を よみます。", "translation": f"Tôi đọc {mean1}."},
                    {"text": f"{word2} を かきます。", "translation": f"Tôi viết {mean2}."},
                    {"text": f"{word3} を べんきょうします。", "translation": f"Tôi học {mean3}."},
                ],
                "tasks": [
                    "Đọc mẫu câu, sau đó thay bằng một từ mới trong bài.",
                    "Viết lại câu với từ vựng thứ hai.",
                    "Nói chậm từng cụm: từ vựng + を + động từ.",
                    "Tự tạo một câu ngắn với từ em nhớ nhất.",
                ],
            },
        }

    jp_lines = [
        f"きょうは {topic} を べんきょうします。",
        f"さいしょに {word1} を よみます。",
        f"{word1} の よみかたは {read1} です。",
        f"つぎに {word2} を ききます。",
        f"{word2} の いみは {mean2} です。",
        f"それから {word3} を かきます。",
        f"{word3} を こえに だして よみます。",
        "ゆっくり よむと おぼえやすいです。",
        "まちがえても だいじょうぶです。",
        "もういちど きいて まねします。",
        "さいごに みじかい ぶんを つくります。",
        "まいにち すこしずつ れんしゅうします。",
    ]
    vi_lines = [
        f"Hôm nay mình học chủ đề {topic}.",
        f"Đầu tiên mình đọc {mean1}.",
        f"Cách đọc của {word1} là {read1}.",
        f"Tiếp theo mình nghe {mean2}.",
        f"Nghĩa của {word2} là {mean2}.",
        f"Sau đó mình viết {mean3}.",
        f"Mình đọc to {word3}.",
        "Đọc chậm sẽ dễ nhớ hơn.",
        "Sai cũng không sao.",
        "Mình nghe lại và nói theo.",
        "Cuối cùng mình tạo một câu ngắn.",
        "Mỗi ngày luyện một chút.",
    ]

    if skill == "listening":
        return {
            "skillFocus": "listening",
            "listeningTask": {
                "title": "Japanese listening",
                "translation": "Bài nghe tiếng Nhật",
                "passage": " ".join(jp_lines),
                "passageTranslation": " ".join(vi_lines),
                "questions": [
                    {"question": "What is today's topic?", "translation": "Hôm nay học chủ đề gì?", "answer": topic},
                    {"question": "Which word is read first?", "translation": "Từ nào được đọc đầu tiên?", "answer": word1},
                    {"question": "What should you do after listening?", "translation": "Sau khi nghe nên làm gì?", "answer": "listen again and repeat"},
                    {"question": "Is making mistakes okay?", "translation": "Nói sai có sao không?", "answer": "No"},
                ],
            },
        }

    if skill == "reading":
        return {
            "skillFocus": "reading",
            "readingTask": {
                "title": "Japanese reading",
                "translation": "Bài đọc tiếng Nhật",
                "passage": " ".join(jp_lines),
                "passageTranslation": " ".join(vi_lines),
                "questions": [
                    {"question": "Find the word for the first vocabulary item.", "translation": "Tìm từ vựng đầu tiên trong bài.", "answer": word1},
                    {"question": "Find one action word.", "translation": "Tìm một động từ/hành động.", "answer": "よみます"},
                    {"question": "What helps memory?", "translation": "Điều gì giúp dễ nhớ?", "answer": "reading slowly"},
                    {"question": "What should you make at the end?", "translation": "Cuối bài nên tạo gì?", "answer": "a short sentence"},
                ],
            },
        }

    if skill == "writing":
        return {
            "skillFocus": "writing",
            "writingTask": {
                "title": "Writing guide",
                "translation": "Gợi ý viết tiếng Nhật",
                "prompt": f"Write 4 short Japanese sentences about {topic}. Use {word1}, {word2}, and {word3}.",
                "promptTranslation": f"Viết 4 câu tiếng Nhật ngắn về {topic}. Dùng {mean1}, {mean2}, và {mean3}.",
                "outline": [
                    "Sentence 1: write what you study today.",
                    "Sentence 2: write one word you can read.",
                    "Sentence 3: write one word you can listen to.",
                    "Sentence 4: write what you will practise again.",
                ],
                "outlineTranslation": [
                    "Câu 1: viết hôm nay em học gì.",
                    "Câu 2: viết một từ em đọc được.",
                    "Câu 3: viết một từ em nghe được.",
                    "Câu 4: viết em sẽ luyện lại điều gì.",
                ],
                "sentenceStarters": [
                    {"text": f"きょうは {topic} を べんきょうします。", "translation": f"Hôm nay tôi học {topic}."},
                    {"text": f"{word1} を よみます。", "translation": f"Tôi đọc {mean1}."},
                    {"text": f"{word2} を ききます。", "translation": f"Tôi nghe {mean2}."},
                    {"text": f"{word3} を かきます。", "translation": f"Tôi viết {mean3}."},
                    {"text": "もういちど れんしゅうします。", "translation": "Tôi sẽ luyện lại một lần nữa."},
                    {"text": "ゆっくり よみます。", "translation": "Tôi đọc chậm."},
                    {"text": "まいにち すこし れんしゅうします。", "translation": "Mỗi ngày tôi luyện một chút."},
                    {"text": "これは だいじです。", "translation": "Điều này quan trọng."},
                ],
                "sample": f"きょうは {topic} を べんきょうします。 {word1} を よみます。 {word2} を ききます。 もういちど れんしゅうします。",
                "sampleTranslation": f"Hôm nay tôi học {topic}. Tôi đọc {mean1}. Tôi nghe {mean2}. Tôi luyện lại một lần nữa.",
                "checklist": [
                    "I wrote 4 short sentences.",
                    "I used at least 2 lesson words.",
                    "I read each sentence aloud.",
                ],
                "checklistTranslation": [
                    "Tôi đã viết 4 câu ngắn.",
                    "Tôi đã dùng ít nhất 2 từ trong bài.",
                    "Tôi đã đọc to từng câu.",
                ],
            },
        }

    return {"skillFocus": skill}


def _enrich_skill_lessons_for_all_units():
    for unit in ROADMAP_UNITS:
        for index, lesson in enumerate(unit.get("lessons", [])):
            if lesson.get("type") != "integrated":
                continue
            content = lesson.setdefault("content", {})
            skill = content.get("skillFocus") or SKILL_SEQUENCE[index % len(SKILL_SEQUENCE)]
            if lesson.get("levelId", "").startswith("jp_"):
                extra = _japanese_skill_extra(skill, lesson, content)
            else:
                extra = _english_skill_extra(skill, lesson, content)
            _merge_missing_skill_extra(content, extra)


_enrich_skill_lessons_for_all_units()


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
