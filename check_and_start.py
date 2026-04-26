#!/usr/bin/env python
"""Check dependencies and start server"""
import sys
import subprocess

print("="*60)
print("Checking dependencies...")
print("="*60)

# Check flask_sqlalchemy
try:
    import flask_sqlalchemy
    print(f"✅ flask-sqlalchemy: {flask_sqlalchemy.__version__}")
except ImportError:
    print("❌ flask-sqlalchemy not found, installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask-sqlalchemy", "-q"])
    import flask_sqlalchemy
    print(f"✅ flask-sqlalchemy installed: {flask_sqlalchemy.__version__}")

# Check werkzeug
try:
    import werkzeug
    print(f"✅ werkzeug: {werkzeug.__version__}")
except ImportError:
    print("❌ werkzeug not found, installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "werkzeug", "-q"])
    import werkzeug
    print(f"✅ werkzeug installed: {werkzeug.__version__}")

# Check other imports
print("\nChecking other imports...")
try:
    from models import db, User
    print("✅ models imported")
except Exception as e:
    print(f"❌ models error: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("Starting server...")
print("="*60)

# Start the app
import app
app.app.run(host='0.0.0.0', port=5000, debug=True)
