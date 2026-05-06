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


def _integrated_lesson(level_id, unit_id, order, title, topic, words, patterns, grammar, dialogue, speaking, quiz):
    audio_base = f"/static/audio/{level_id}/{unit_id}_l{order}"
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
        "content": {
            "vocabulary": [
                {
                    "word": item[0],
                    "meaning": item[1],
                    "example": item[2],
                    "audioUrl": f"{audio_base}_word_{idx + 1}.mp3",
                }
                for idx, item in enumerate(words)
            ],
            "sentencePatterns": patterns,
            "grammar": grammar,
            "dialogue": dialogue,
            "speaking": [
                {"text": text, "audioUrl": f"{audio_base}_speak_{idx + 1}.mp3"}
                for idx, text in enumerate(speaking)
            ],
            "quiz": quiz,
            "review": [
                f"Say 3 words about {topic}.",
                f"Make 2 sentences about {topic}.",
                f"Record yourself saying: {speaking[0] if speaking else title}.",
            ],
        },
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


def _build_units(level_id, level_title, specs):
    units = []
    for unit_idx in range(6):
        unit_id = f"{level_id}_u{unit_idx + 1}"
        group = specs[unit_idx * 5:(unit_idx + 1) * 5]
        units.append({
            "id": unit_id,
            "levelId": level_id,
            "title": f"Unit {unit_idx + 1}: {level_title} Practice {unit_idx + 1}",
            "description": f"Five real-life {level_title} lessons with vocabulary, dialogue, speaking and quiz.",
            "order": unit_idx + 1,
            "lessons": [
                _integrated_lesson(
                    level_id,
                    unit_id,
                    lesson_idx + 1,
                    title,
                    topic,
                    words,
                    patterns,
                    grammar,
                    [{"speaker": speaker, "text": text} for speaker, text in dialogue],
                    speaking,
                    _quiz(quiz_prompt, quiz_prompt.split(":")[-1].strip() if ":" in quiz_prompt else "Could you help me, please?"),
                )
                for lesson_idx, (topic, title, words, patterns, grammar, dialogue, speaking, quiz_prompt)
                in enumerate(group)
            ],
        })
    return units


ROADMAP_UNITS = (
    _build_units("starter", "Starter", STARTER_TOPICS)
    + _build_units("flyer", "Flyer", [_expand_flyer_topic(item, idx) for idx, item in enumerate(FLYER_TOPICS)])
)


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
