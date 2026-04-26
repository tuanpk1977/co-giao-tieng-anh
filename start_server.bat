@echo off
cd /d "d:\CO GIAO TIENG ANH"
echo Installing dependencies...
pip install flask-sqlalchemy werkzeug -q
echo Starting server...
python app.py
pause
