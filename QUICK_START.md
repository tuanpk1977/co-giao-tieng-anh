# 🚀 Ms. Smile English - Quick Start Guide

Chạy app public bằng ngrok để test với người khác (không cần cài gì).

---

## 📋 Yêu cầu

- Python 3.8+ đã cài
- Ngrok (free tier OK)

---

## 🛠️ Bước 1: Cài đặt ngrok (chỉ 1 lần)

### Cách 1: Download trực tiếp (Windows)

1. Truy cập: https://ngrok.com/download
2. Download Windows (64-bit)
3. Giải nén file `ngrok.exe`
4. Copy `ngrok.exe` vào thư mục `d:\CO GIAO TIENG ANH\`

### Cách 2: Dùng package manager

**Chocolatey:**
```powershell
choco install ngrok
```

**Winget:**
```powershell
winget install ngrok.ngrok
```

### Cách 3: macOS / Linux

```bash
# macOS with Homebrew
brew install ngrok

# Linux
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok
```

---

## 🔑 Bước 2: Đăng ký ngrok (free, không bắt buộc nhưng nên có)

1. Truy cập: https://dashboard.ngrok.com/signup
2. Đăng ký tài khoản (dùng email)
3. Vào "Your Authtoken" → Copy token
4. Chạy lệnh:

```bash
ngrok config add-authtoken YOUR_TOKEN_HERE
```

> 💡 **Lưu ý:** Free tier cho phép 1 tunnel, đủ để test. Không cần authtoken cũng chạy được nhưng có giới hạn.

---

## 🚀 Bước 3: Chạy server (chỉ 1 lệnh!)

### Cách đơn giản nhất:

```bash
cd "d:\CO GIAO TIENG ANH"
python run_public.py
```

Script sẽ:
- ✅ Kiểm tra ngrok
- ✅ Chạy Flask server (host=0.0.0.0)
- ✅ Mở ngrok tunnel
- ✅ Hiển thị public URL

### Output khi chạy thành công:

```
============================================================
🌟 Ms. Smile English - Public Server
============================================================

✅ ngrok found: 3.x.x
📝 Kiểm tra authtoken...
   ✅ ngrok authtoken OK

🚀 Khởi động Flask server...
   Port: 5000
   Host: 0.0.0.0 (public)

🌐 Khởi động ngrok tunnel...
   Port: 5000

============================================================
🎉 PUBLIC URL CỦA BẠN:

   ➜ https://xxxx.ngrok.io

📱 Gửi link này cho người khác!
   Họ có thể dùng ngay trên điện thoại hoặc máy tính
   Không cần cài đặt gì cả!

============================================================
```

---

## 📱 Bước 4: Gửi link cho người khác

1. **Copy link** public (ví dụ: `https://xxxx.ngrok.io`)
2. **Gửi qua:**
   - Zalo
   - Facebook Messenger
   - Email
   - SMS
   - Bất kỳ đâu!

3. **Người nhận:**
   - Click link → Dùng ngay
   - Không cần cài Python, thư viện hay gì cả
   - Chạy trên điện thoại, tablet, máy tính đều OK

---

## 🧪 Bước 5: Test các chức năng

### Desktop:
1. Mở link trên Chrome/Firefox/Edge
2. Test chat với AI
3. Test voice input (microphone)

### Mobile:
1. Mở link trên Safari/Chrome mobile
2. Cho phép microphone khi được hỏi
3. Test voice input trên điện thoại

### Test checklist:
- [ ] Chat với AI (text)
- [ ] Voice input (microphone)
- [ ] AI Text-to-Speech (AI nói)
- [ ] Roleplay mode (Lễ tân, Bán hàng...)
- [ ] Situation Advisor (Tình huống khó)
- [ ] UI responsive trên mobile

---

## 🔧 Chạy thủ công (không dùng script)

Nếu muốn kiểm soát riêng:

**Terminal 1 - Chạy Flask:**
```bash
cd "d:\CO GIAO TIENG ANH"
python app.py
```

**Terminal 2 - Chạy ngrok:**
```bash
ngrok http 5000
```

**Xem public URL:**
- Truy cập: http://127.0.0.1:4040
- Hoặc nhìn trong terminal ngrok

---

## ⚠️ Lưu ý quan trọng

### 1. Link tạm thời
- Mỗi lần chạy lại ngrok → link mới
- Link cũ hết hiệu lực khi dừng server
- Free tier: 1 tunnel, 40 connections/minute

### 2. Tốc độ
- Tùy thuộc mạng của bạn
- Ngrok có thể chậm hơn local
- Không dùng cho production/production server

### 3. Bảo mật
- Link public → ai cũng truy cập được
- Không dùng cho dữ liệu nhạy cảm
- Chỉ dùng để demo/test

### 4. Mobile limitations
- iOS Safari có thể cần user interaction trước khi phát audio
- Voice input cần HTTPS (ngrok OK)
- Test trên cả WiFi và 4G

---

## 🐛 Troubleshooting

### Lỗi: "ngrok not found"
**Giải pháp:**
```bash
# Thêm ngrok vào PATH hoặc
copy ngrok.exe vào thư mục d:\CO GIAO TIENG ANH\
```

### Lỗi: "Cannot connect to server"
**Giải pháp:**
1. Kiểm tra firewall (cho phép port 5000)
2. Kiểm tra antivirus
3. Thử chạy lại ngrok

### Lỗi: "ngrok tunnel not found"
**Giải pháp:**
1. Đợi thêm 5-10 giây
2. Kiểm tra ngrok tại: http://127.0.0.1:4040
3. Restart script

### Lỗi: "CORS error"
**Giải pháp:**
App đã cấu hình Flask-CORS, nếu vẫn lỗi:
- Kiểm tra `flask-cors` đã cài: `pip install flask-cors`
- Restart server

### Mobile không phát được audio
**Giải pháp:**
- iOS: Cần user click/tap trước khi phát audio
- Android: Cho phép autoplay trong settings
- Test trên Chrome mobile

---

## 📝 Log và Debug

### Xem ngrok status:
- Truy cập: http://127.0.0.1:4040

### Xem Flask logs:
```bash
cd "d:\CO GIAO TIENG ANH"
python app.py
```

### Kiểm tra public URL:
```bash
curl http://127.0.0.1:4040/api/tunnels
```

---

## 🎯 Kết quả mong đợi

Sau khi chạy `python run_public.py`:

✅ Flask server chạy trên port 5000  
✅ Ngrok tunnel hoạt động  
✅ Public URL hiển thị  
✅ Người khác dùng được trên mobile/4G  
✅ Tất cả chức năng hoạt động  

---

## 📞 Hỗ trợ

Nếu gặp lỗi:
1. Kiểm tra ngrok: `ngrok version`
2. Kiểm tra Python: `python --version`
3. Kiểm tra Flask: `python -c "import flask; print(flask.__version__)"`
4. Xem log chi tiết trong terminal

---

**Sẵn sàng demo cho bạn bè! 🎉**
