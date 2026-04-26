#!/usr/bin/env python
"""
Test script cho public deployment
Kiểm tra API endpoints và CORS
"""
import requests
import sys
import time

BASE_URL = "http://localhost:5000"

def test_endpoint(endpoint, method="GET", data=None, description=""):
    """Test một API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        else:
            response = requests.post(url, json=data, timeout=10)
        
        status = "✅" if response.status_code == 200 else "⚠️"
        print(f"  {status} {description}: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"  ❌ {description}: {str(e)[:50]}")
        return False

def main():
    print("=" * 60)
    print("🧪 Testing Ms. Smile English - Public Deployment")
    print("=" * 60)
    print()
    
    # Đợi server khởi động
    print("⏳ Đợi server khởi động...")
    time.sleep(2)
    
    results = {}
    
    # Test 1: Trang chủ
    print("\n📄 Test Trang chủ:")
    results['home'] = test_endpoint("/", "GET", description="Home page")
    
    # Test 2: API Health
    print("\n💓 Test API Health:")
    results['chat'] = test_endpoint("/api/chat", "POST", 
                                   {"message": "Hello", "mode": "conversation"},
                                   "Chat API")
    
    # Test 3: Roleplay API
    print("\n🎭 Test Roleplay:")
    results['roleplay_greeting'] = test_endpoint("/api/roleplay/greeting", "POST",
                                                  {"role": "waiter", "situation": "take_order"},
                                                  "Roleplay Greeting")
    results['roles'] = test_endpoint("/api/roleplay/roles", "GET", description="Get Roles")
    
    # Test 4: Situation API
    print("\n🆘 Test Situation Advisor:")
    results['situation'] = test_endpoint("/api/situation/analyze", "POST",
                                        {"situation": "Xin lỗi khách hàng", "profile": {"level": "beginner"}},
                                        "Situation Analyze")
    
    # Test 5: User Auth API
    print("\n👤 Test User Auth:")
    results['login'] = test_endpoint("/api/auth/login", "POST",
                                    {"email": "test@test.com", "password": "123456"},
                                    "Login API")
    results['progress'] = test_endpoint("/api/user/progress?user_id=1", "GET", description="Progress API")
    
    # Tổng kết
    print("\n" + "=" * 60)
    print("📊 TỔNG KẾT:")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"  {status}: {name}")
    
    print()
    print(f"  Kết quả: {passed}/{total} test passed")
    print()
    
    if passed == total:
        print("🎉 Tất cả API hoạt động tốt!")
        print("   Sẵn sàng cho public deployment!")
    else:
        print("⚠️ Có API bị lỗi, kiểm tra lại server")
    
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
