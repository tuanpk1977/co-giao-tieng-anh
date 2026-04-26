"""
Database models for user management and progress tracking
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()

class User(db.Model):
    """User account model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Profile info
    age = db.Column(db.Integer)
    job = db.Column(db.String(50))  # sales, engineer, cafe, office, student, other
    meet_foreigners = db.Column(db.Boolean, default=False)
    english_usage = db.Column(db.String(200))  # what they use English for
    goal = db.Column(db.String(50))  # daily, work, travel
    english_level = db.Column(db.String(20), default='beginner')
    
    # Relationships
    progress = db.relationship('UserProgress', backref='user', lazy=True, uselist=False)
    sessions = db.relationship('LearningSession', backref='user', lazy=True)
    errors = db.relationship('CommonError', backref='user', lazy=True)
    reminders = db.relationship('ReminderLog', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'phone': self.phone,
            'name': self.name,
            'age': self.age,
            'job': self.job,
            'meet_foreigners': self.meet_foreigners,
            'english_usage': self.english_usage,
            'goal': self.goal,
            'english_level': self.english_level,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def get_profile_for_ai(self):
        """Get profile formatted for AI personalization"""
        return {
            'level': self.english_level or 'beginner',
            'job': self.job or 'general',
            'goal': self.goal or 'communication',
            'meet_foreigners': self.meet_foreigners,
            'english_usage': self.english_usage or '',
            'age': self.age
        }


class UserProgress(db.Model):
    """User learning progress model"""
    __tablename__ = 'user_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Study stats
    total_days_studied = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_study_date = db.Column(db.Date)
    
    # Practice stats
    total_sentences_practiced = db.Column(db.Integer, default=0)
    total_situations_practiced = db.Column(db.Integer, default=0)
    
    # Average scores (0-100)
    avg_grammar_score = db.Column(db.Float, default=0.0)
    avg_natural_score = db.Column(db.Float, default=0.0)
    total_evaluations = db.Column(db.Integer, default=0)
    
    # Common errors (JSON)
    common_errors_json = db.Column(db.Text, default='[]')
    
    # Practiced situations (JSON array)
    practiced_situations_json = db.Column(db.Text, default='[]')
    
    # Corrected sentences (JSON array)
    corrected_sentences_json = db.Column(db.Text, default='[]')
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_common_errors(self):
        try:
            return json.loads(self.common_errors_json or '[]')
        except:
            return []
    
    def set_common_errors(self, errors):
        self.common_errors_json = json.dumps(errors)
    
    def get_practiced_situations(self):
        try:
            return json.loads(self.practiced_situations_json or '[]')
        except:
            return []
    
    def set_practiced_situations(self, situations):
        self.practiced_situations_json = json.dumps(situations[-100:])  # Keep last 100
    
    def get_corrected_sentences(self):
        try:
            return json.loads(self.corrected_sentences_json or '[]')
        except:
            return []
    
    def set_corrected_sentences(self, sentences):
        self.corrected_sentences_json = json.dumps(sentences[-50:])  # Keep last 50
    
    def to_dict(self):
        return {
            'total_days_studied': self.total_days_studied,
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'last_study_date': self.last_study_date.isoformat() if self.last_study_date else None,
            'total_sentences_practiced': self.total_sentences_practiced,
            'total_situations_practiced': self.total_situations_practiced,
            'avg_grammar_score': round(self.avg_grammar_score, 1),
            'avg_natural_score': round(self.avg_natural_score, 1),
            'common_errors': self.get_common_errors()[:5],  # Top 5
            'practiced_situations': self.get_practiced_situations()[-10:],  # Last 10
            'corrected_sentences': self.get_corrected_sentences()[-5:]  # Last 5
        }


class LearningSession(db.Model):
    """Record of each learning session"""
    __tablename__ = 'learning_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    duration_minutes = db.Column(db.Integer, default=0)
    sentences_practiced = db.Column(db.Integer, default=0)
    avg_grammar_score = db.Column(db.Float)
    avg_natural_score = db.Column(db.Float)
    errors_made = db.Column(db.Text, default='[]')  # JSON array
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CommonError(db.Model):
    """Track common errors per user"""
    __tablename__ = 'common_errors'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    error_type = db.Column(db.String(100))  # e.g., "very → really", "missing article"
    error_count = db.Column(db.Integer, default=1)
    example_wrong = db.Column(db.String(255))
    example_correct = db.Column(db.String(255))
    last_occurrence = db.Column(db.DateTime, default=datetime.utcnow)


class ReminderLog(db.Model):
    """Track reminder emails sent"""
    __tablename__ = 'reminder_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reminder_type = db.Column(db.String(50))  # 'daily', '3days', 'weekly'
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    opened = db.Column(db.Boolean, default=False)


class UserActivity(db.Model):
    """Track detailed user activities"""
    __tablename__ = 'user_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(50))  # 'chat', 'roleplay', 'situation', 'practice'
    content = db.Column(db.Text)
    ai_response = db.Column(db.Text)
    grammar_score = db.Column(db.Integer)
    natural_score = db.Column(db.Integer)
    errors = db.Column(db.Text, default='[]')  # JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def init_db(app):
    """Initialize database"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
