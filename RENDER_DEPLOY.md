# 🚀 Deploy Ms. Smile English lên Render (Free)

Hướng dẫn chi tiết deploy Flask app lên Render để có link public cố định.

---

## 📋 Yêu cầu trước khi deploy

- Tài khoản GitHub (miễn phí)
- Tài khoản Render (miễn phí): https://render.com
- Project Ms. Smile English đã push lên GitHub

---

## 📝 Bước 1: Chuẩn bị code trên local

### Kiểm tra các file cần thiết:

```bash
# Trong thư mục d:\CO GIAO TIENG ANH
dir
```

Đảm bảo có các file:
- ✅ `app.py` - Flask app chính
- ✅ `requirements.txt` - Dependencies
- ✅ `Procfile` - Render start command
- ✅ `templates/` - HTML templates
- ✅ `static/` - CSS, JS, images
- ✅ `models.py` - Database models
- ✅ `services/` - Business logic
- ✅ `config.py` - Configuration

### Kiểm tra requirements.txt:

```txt
flask==3.0.3
flask-cors==4.0.1
flask-sqlalchemy==3.1.1
werkzeug==3.0.3
gunicorn==21.2.0
openai==1.35.0
requests==2.32.3
google-generativeai==0.7.2
python-dotenv==1.0.1
```

### Kiểm tra Procfile:

```
web: gunicorn app:app
```

---

## 🔧 Bước 2: Push code lên GitHub

### Nếu chưa có repo GitHub:

```bash
# Trong thư mục project
cd "d:\CO GIAO TIENG ANH"

# Khởi tạo git
git init

# Thêm tất cả file
git add .

# Commit
git commit -m "Initial commit - Ms Smile English ready for Render"

# Tạo repo trên GitHub trước, sau đó:
git remote add origin https://github.com/YOUR_USERNAME/ms-smile-english.git
git branch -M main
git push -u origin main
```

### Nếu đã có repo:

```bash
cd "d:\CO GIAO TIENG ANH"
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

---

## 🌐 Bước 3: Deploy lên Render

### 1. Đăng nhập Render

- Truy cập: https://dashboard.render.com
- Đăng nhập bằng GitHub account

### 2. Tạo New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect GitHub repository:
   - Chọn repo `ms-smile-english`
   - Click **"Connect"**

### 3. Cấu hình Web Service

| Setting | Value |
|---------|-------|
| **Name** | `ms-smile-english` (hoặc tên bạn muốn) |
| **Environment** | Python 3 |
| **Region** | Singapore (gần VN nhất) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Plan** | Free |

Click **"Create Web Service"**

### 4. Thêm Environment Variables

Vào tab **"Environment"** và thêm các biến:

#### BẮT BUỘC:

```
OPENAI_API_KEY=sk-your-openai-api-key-here
AI_PROVIDER=openai
SECRET_KEY=your-secret-key-here-random-string
DATABASE_URL=sqlite:///ms_smile.db
```

#### TÙY CHỌN (cho email reminders):

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
FROM_EMAIL=ms.smile.english@gmail.com
```

#### Cách lấy các key:

**OPENAI_API_KEY:**
- Vào https://platform.openai.com/api-keys
- Tạo new secret key
- Copy và paste vào Render

**SECRET_KEY:**
- Tạo random string, ví dụ: `ms_smile_2024_secret_key_xyz123`

**SMTP_PASS (nếu dùng Gmail):**
- Vào Google Account → Security
- Bật 2-Step Verification
- Tạo App Password
- Copy 16 ký tự và paste vào

### 5. Deploy

- Click **"Save Changes"**
- Render sẽ tự động build và deploy
- Đợi 2-3 phút

---

## ✅ Bước 4: Kiểm tra sau deploy

### 1. Test Health Check

Truy cập:
```
https://your-app-name.onrender.com/health
```

Kết quả mong đợi:
```json
{
  "app": "Ms. Smile English",
  "status": "ok",
  "version": "1.0.0"
}
```

### 2. Test App chính

Truy cập:
```
https://your-app-name.onrender.com
```

Test các chức năng:
- [ ] Chat với AI
- [ ] Voice input (microphone)
- [ ] AI Text-to-Speech
- [ ] Roleplay modes
- [ ] Situation Advisor
- [ ] Đăng ký/Đăng nhập user
- [ ] Dashboard tiến độ

### 3. Test trên mobile

- Mở link trên điện thoại
- Cho phép microphone khi được hỏi
- Test voice input

---

## 🔍 Troubleshooting

### Lỗi: "Build failed"

**Kiểm tra:**
1. `requirements.txt` có đầy đủ dependencies?
2. Procfile có đúng format?
3. Git push thành công chưa?

**Cách fix:**
```bash
# Local test trước
pip install -r requirements.txt
python app.py
```

### Lỗi: "Application Error"

**Kiểm tra logs trong Render Dashboard:**
- Vào tab **"Logs"**
- Xem lỗi cụ thể

**Thường gặp:**
- Thiếu environment variable
- Lỗi import module
- Database connection error

### Lỗi: "Module not found"

**Kiểm tra requirements.txt có thư viện đó không**

Thêm vào rồi push lại:
```bash
git add requirements.txt
git commit -m "Add missing dependency"
git push origin main
```

### Lỗi: "CORS error"

**Kiểm tra:**
- `flask-cors` đã install chưa
- Trong `app.py` có `CORS(app)` chưa

### Lỗi Database

**SQLite trên Render:**
- Render Free: Disk ephemeral (mất dữ liệu khi restart/deploy)
- Cách giải quyết:
  - Dùng cho demo/test OK
  - Bản production: Chuyển PostgreSQL (Render PostgreSQL free tier)

**Thêm PostgreSQL (nâng cao):**
```
1. Trong Render Dashboard → New PostgreSQL
2. Copy Internal Database URL
3. Thêm vào Environment Variables: DATABASE_URL=postgresql://...
```

---

## 📱 URL Sau Deploy

**Link cố định của bạn:**
```
https://your-app-name.onrender.com
```

**Gửi cho bạn bè:**
- Dùng ngay trên điện thoại
- Không cần cài đặt gì
- Không cần ngrok
- Link không đổi (trừ khi bạn đổi tên app)

---

## ⚡ Cập nhật code sau này

Mỗi khi sửa code:

```bash
cd "d:\CO GIAO TIENG ANH"
git add .
git commit -m "Update feature XYZ"
git push origin main
```

Render sẽ **tự động deploy** lại!

---

## 🎁 Tính năng Render Free

| Feature | Giới hạn |
|---------|----------|
| **Web Services** | 1 instance |
| **Bandwidth** | 100GB/tháng |
| **Build time** | 15 phút/build |
| **Disk** | 0.5GB (ephemeral) |
| **Sleep** | Sleep sau 15 phút không active |
| **Wake up** | 30 giây để wake up |

**Lưu ý:** App sẽ "sleep" khi không có traffic. Lần đầu truy cập sau sleep sẽ chậm ~30 giây để wake up.

---

## 🔒 Bảo mật

**KHÔNG commit các file sau lên GitHub:**
```
.env
*.db
__pycache__/
*.pyc
.DS_Store
```

**Đã có trong .gitignore chưa?**

Nếu chưa, tạo file `.gitignore`:
```
.env
*.db
__pycache__/
*.pyc
.DS_Store
*.log
```

---

## ✅ Checklist trước khi deploy

- [ ] Code push lên GitHub thành công
- [ ] `requirements.txt` đầy đủ dependencies
- [ ] `Procfile` đúng format
- [ ] `app.py` có health check route
- [ ] Environment variables đã thêm trên Render
- [ ] Test local trước: `python app.py`
- [ ] Build command test: `pip install -r requirements.txt`

---

## 🎯 Kết quả mong đợi

Sau khi deploy thành công:

✅ **Link public cố định**: `https://your-app.onrender.com`  
✅ **Không cần ngrok** nữa  
✅ **Không cần máy tính bạn chạy 24/7**  
✅ **Tự động deploy** khi push code  
✅ **Dùng được trên mọi thiết bị** (mobile, tablet, desktop)  

---

## 📞 Hỗ trợ

Nếu gặp lỗi:
1. Kiểm tra Render Dashboard Logs
2. Kiểm tra GitHub repo đã push đúng chưa
3. Test local trước: `python app.py`
4. So sánh với hướng dẫn này

**Happy Deploying! 🚀**
