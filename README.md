# Ms. Smile English 🌸

**Cô Giáo Tiếng Anh AI Dễ Thương** - Ứng dụng học tiếng Anh giao tiếp cho người mới bắt đầu, giải thích bằng tiếng Việt.

![Ms. Smile](https://img.shields.io/badge/Ms.-Smile%20English-FF6B9D?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask)

## ✨ Tính năng chính

- 💬 **Chat với cô giáo AI** - Thân thiện, kiên nhẫn, sửa lỗi nhẹ nhàng
- 👩‍🏫 **Avatar cô giáo dễ thương** - Giao diện đẹp mắt, dễ sử dụng
- 📝 **Bài học hàng ngày** - 5 từ vựng, 3 mẫu câu, 1 đoạn hội thoại
- 🔊 **Phát âm thanh** - Nghe cô đọc tiếng Anh chuẩn
- 🎤 **Ghi âm & Speech-to-Text** - Luyện nói và nhận diện giọng nói
- 🎯 **AI đánh giá phát âm** - Nhận xét đúng/sai, gợi ý cải thiện
- 📊 **Lịch sử học tập** - Theo dõi tiến độ, thống kê lỗi thường gặp

## 🚀 Cài đặt & Chạy

### 1. Clone hoặc tải project

```bash
cd "CO GIAO TIENG ANH"
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình API Key

Mở file `config.py` và thêm API key:

```python
# Chọn model AI: "openai", "qwen", hoặc "gemini"
AI_PROVIDER = "openai"

# Thêm API key (hoặc dùng environment variables)
OPENAI_API_KEY = "your-openai-api-key-here"
# QWEN_API_KEY = "your-qwen-api-key"
# GEMINI_API_KEY = "your-gemini-api-key"
```

**Lấy API key:**
- **OpenAI**: https://platform.openai.com/api-keys
- **Qwen (Alibaba)**: https://dashscope.aliyun.com/
- **Google Gemini**: https://makersuite.google.com/app/apikey

### 4. Chạy ứng dụng

```bash
python app.py
```

Mở trình duyệt: **http://localhost:5000**

## 📁 Cấu trúc project

```
CO GIAO TIENG ANH/
├── app.py                 # Flask backend chính
├── config.py              # Cấu hình API keys, model
├── requirements.txt       # Dependencies
├── README.md             # Hướng dẫn này
│
├── services/             # Module AI service
│   ├── __init__.py
│   └── ai_service.py     # OpenAI, Qwen, Gemini APIs
│
├── utils/                # Tiện ích
│   ├── __init__.py
│   └── history.py        # Quản lý lịch sử học tập
│
├── templates/            # HTML templates
│   └── index.html        # Giao diện chính
│
├── static/               # Assets
│   ├── css/
│   │   └── style.css     # Styles chính
│   └── js/
│       └── app.js        # JavaScript frontend
│
└── data/                 # Dữ liệu lưu trữ
    └── learning_history.json
```

## 🎨 Giao diện

- **Màu chủ đạo**: Hồng dễ thương (#FF6B9D)
- **Responsive**: Hoạt động tốt trên desktop và mobile
- **Animation**: Avatar cô giáo có hiệu ứng mắt chớp, mỉm cười

## 🔧 Cấu hình Model AI

Chỉnh sửa `config.py`:

| Provider | Model mặc định | Đặc điểm |
|----------|---------------|----------|
| OpenAI | gpt-4o-mini | Ổn định, chất lượng cao |
| Qwen | qwen-max | Tốt cho tiếng Việt |
| Gemini | gemini-1.5-flash | Miễn phí, nhanh |

```python
# Ví dụ: Chuyển sang Gemini
AI_PROVIDER = "gemini"
GEMINI_API_KEY = "your-key"
```

## 📱 Sử dụng

### Chat với cô giáo
1. Nhập tin nhắn (tiếng Việt hoặc tiếng Anh)
2. Hoặc bấm 🎤 để nói
3. Nhận phản hồi và sửa lỗi từ Ms. Smile

### Bài học hôm nay
1. Bấm nút "Bài học hôm nay"
2. Học từ vựng, mẫu câu, hội thoại
3. Nghe phát âm bằng nút 🔊
4. Luyện nói với nút 🎤
5. Làm bài tập cuối bài

### Luyện nói
1. Trong bài học, bấm "Nói" ở phần luyện nói
2. Nghe cô đọc mẫu
3. Bấm giữ 🎤 và nói theo
4. Nhận đánh giá từ AI

## 🛠️ Troubleshooting

### Lỗi "API key chưa được cấu hình"
- Kiểm tra file `config.py` đã có API key chưa
- Hoặc set environment variable: `set OPENAI_API_KEY=your-key`

### Speech-to-text không hoạt động
- Cần mở bằng HTTPS hoặc localhost
- Chrome hoạt động tốt nhất
- Cho phép quyền microphone khi được hỏi

### Port 5000 bị chiếm
```bash
# Thay đổi port trong app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 📝 License

MIT License - Free to use and modify!

---

**Made with 💖 by Ms. Smile**

*"Học tiếng Anh thật vui, cùng cô Smile nhé!"* 🌸
