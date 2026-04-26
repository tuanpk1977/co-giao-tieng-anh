#!/usr/bin/env python
"""
Ms. Smile English - Public Server with ngrok
Chạy 1 lệnh → có link public để test với người khác
"""
import subprocess
import sys
import time
import os
import signal
import threading
from pathlib import Path

def print_banner():
    print("=" * 60)
    print("🌟 Ms. Smile English - Public Server")
    print("=" * 60)
    print()

def check_ngrok():
    """Kiểm tra ngrok đã cài chưa"""
    try:
        result = subprocess.run(
            ["ngrok", "version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ ngrok found: {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ ngrok not found!")
    print()
    print("📥 CÀI ĐẶT NGROK:")
    print("   1. Truy cập: https://ngrok.com/download")
    print("   2. Download và giải nén")
    print("   3. Thêm vào PATH hoặc để cùng thư mục với app")
    print()
    print("   HOẶC dùng chocolatey:")
    print("   choco install ngrok")
    print()
    print("   HOẶC dùng winget:")
    print("   winget install ngrok.ngrok")
    print()
    return False

def get_ngrok_url():
    """Lấy public URL từ ngrok API"""
    import urllib.request
    import json
    
    max_retries = 30
    for i in range(max_retries):
        try:
            # Ngrok API local
            req = urllib.request.Request(
                "http://127.0.0.1:4040/api/tunnels",
                headers={"Accept": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=2) as response:
                data = json.loads(response.read().decode())
                tunnels = data.get("tunnels", [])
                for tunnel in tunnels:
                    if tunnel.get("public_url"):
                        return tunnel["public_url"]
        except Exception:
            pass
        
        time.sleep(1)
        print(f"   ⏳ Đợi ngrok khởi động... ({i+1}/{max_retries})")
    
    return None

def run_flask():
    """Chạy Flask server"""
    print("🚀 Khởi động Flask server...")
    print("   Port: 5000")
    print("   Host: 0.0.0.0 (public)")
    print()
    
    env = os.environ.copy()
    env["FLASK_ENV"] = "production"
    env["PYTHONUNBUFFERED"] = "1"
    
    # Chạy Flask trong thread riêng
    def flask_thread():
        subprocess.run(
            [sys.executable, "app.py"],
            env=env,
            cwd=str(Path(__file__).parent)
        )
    
    thread = threading.Thread(target=flask_thread, daemon=True)
    thread.start()
    
    # Đợi Flask khởi động
    time.sleep(3)
    print("   ✅ Flask server đang chạy")
    print()
    return thread

def run_ngrok():
    """Chạy ngrok"""
    print("🌐 Khởi động ngrok tunnel...")
    print("   Port: 5000")
    print()
    
    # Chạy ngrok
    process = subprocess.Popen(
        ["ngrok", "http", "5000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(Path(__file__).parent)
    )
    
    # Đợi ngrok tạo tunnel
    time.sleep(3)
    
    # Lấy public URL
    public_url = get_ngrok_url()
    
    if public_url:
        print()
        print("=" * 60)
        print("🎉 PUBLIC URL CỦA BẠN:")
        print()
        print(f"   ➜ {public_url}")
        print()
        print("📱 Gửi link này cho người khác!")
        print("   Họ có thể dùng ngay trên điện thoại hoặc máy tính")
        print("   Không cần cài đặt gì cả!")
        print()
        print("⚠️  Lưu ý:")
        print("   - Link chỉ hoạt động khi server đang chạy")
        print("   - Mỗi lần chạy lại có thể có link mới")
        print("   - Dùng Ctrl+C để dừng server")
        print("=" * 60)
        print()
        
        # Lưu URL vào file để tiện copy
        with open("public_url.txt", "w") as f:
            f.write(public_url)
        print("   💾 URL đã lưu vào: public_url.txt")
        print()
    else:
        print("   ⚠️ Không lấy được public URL")
        print("   Thử truy cập: http://127.0.0.1:4040 để xem tunnels")
    
    return process, public_url

def main():
    print_banner()
    
    # Kiểm tra ngrok
    if not check_ngrok():
        sys.exit(1)
    
    print("📝 Kiểm tra authtoken...")
    result = subprocess.run(
        ["ngrok", "config", "check"],
        capture_output=True,
        text=True
    )
    if "valid" in result.stdout.lower() or result.returncode == 0:
        print("   ✅ ngrok authtoken OK")
    else:
        print("   ⚠️ Chưa có authtoken hoặc không cần (free tier)")
    print()
    
    try:
        # Chạy Flask
        flask_thread = run_flask()
        
        # Chạy ngrok
        ngrok_process, public_url = run_ngrok()
        
        print("💡 CÁCH DÙNG:")
        print("   1. Copy link public ở trên")
        print("   2. Gửi cho bạn bè qua Zalo/Facebook/Email")
        print("   3. Họ mở link trên điện thoại → dùng ngay!")
        print()
        print("🧪 TEST CÁC CHỨC NĂNG:")
        print("   ✓ Chat với AI")
        print("   ✓ Roleplay (Lễ tân, Bán hàng...)")
        print("   ✓ Situation Advisor (Tình huống khó)")
        print("   ✓ Voice input (microphone)")
        print("   ✓ Text-to-Speech (AI nói)")
        print()
        print("⏳ Server đang chạy... Nhấn Ctrl+C để dừng")
        print()
        
        # Giữ chương trình chạy
        while True:
            try:
                # Kiểm tra ngrok còn chạy không
                if ngrok_process.poll() is not None:
                    print("   ⚠️ ngrok đã dừng")
                    break
                time.sleep(1)
            except KeyboardInterrupt:
                print()
                print()
                print("🛑 Đang dừng server...")
                break
    
    except KeyboardInterrupt:
        print()
        print("🛑 Đang dừng server...")
    
    finally:
        # Dọn dẹp
        print()
        print("🧹 Dọn dẹp...")
        try:
            ngrok_process.terminate()
            ngrok_process.wait(timeout=2)
        except:
            try:
                ngrok_process.kill()
            except:
                pass
        
        print("   ✅ Đã dừng ngrok")
        print("   ✅ Đã dừng Flask")
        print()
        print("👋 Tạm biệt! Hẹn gặp lại!")

if __name__ == "__main__":
    main()
