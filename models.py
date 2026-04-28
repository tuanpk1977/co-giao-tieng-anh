"""
Database models for user management and progress tracking
"""
import os
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text
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
    
    # Subscription and payment info
    role = db.Column(db.String(20), default='user')
    status = db.Column(db.String(20), default='trial')
    plan_name = db.Column(db.String(50), default='free_trial')
    plan_start = db.Column(db.DateTime)
    plan_end = db.Column(db.DateTime)
    trial_end = db.Column(db.DateTime)
    reminder_enabled = db.Column(db.Boolean, default=True)
    reminder_hour = db.Column(db.String(5), default='20:00')
    reminder_message = db.Column(db.String(255), default='Hôm nay em học 5 phút với Ms. Smile nhé 😊')
    is_locked = db.Column(db.Boolean, default=False)

    # Relationships
    progress = db.relationship('UserProgress', backref='user', lazy=True, uselist=False)
    sessions = db.relationship('LearningSession', backref='user', lazy=True)
    errors = db.relationship('CommonError', backref='user', lazy=True)
    reminders = db.relationship('ReminderLog', backref='user', lazy=True)
    usage_logs = db.relationship('UsageLog', backref='user', lazy=True)
    payment_requests = db.relationship('PaymentRequest', backref='user', lazy=True)
    payment_history = db.relationship('PaymentHistory', backref='user', lazy=True)
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)
    
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
            'role': self.role,
            'status': self.status,
            'plan_name': self.plan_name,
            'plan_start': self.plan_start.isoformat() if self.plan_start else None,
            'plan_end': self.plan_end.isoformat() if self.plan_end else None,
            'trial_end': self.trial_end.isoformat() if self.trial_end else None,
            'reminder_enabled': self.reminder_enabled,
            'reminder_hour': self.reminder_hour,
            'reminder_message': self.reminder_message,
            'is_locked': self.is_locked,
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

    @property
    def is_admin(self):
        return self.role == 'admin'

    def get_plan_info(self):
        return {
            'plan_name': self.plan_name,
            'status': self.status,
            'plan_start': self.plan_start.isoformat() if self.plan_start else None,
            'plan_end': self.plan_end.isoformat() if self.plan_end else None,
            'trial_end': self.trial_end.isoformat() if self.trial_end else None,
            'reminder_enabled': self.reminder_enabled,
            'reminder_hour': self.reminder_hour,
            'reminder_message': self.reminder_message
        }


class Plan(db.Model):
    """Subscription plan definitions"""
    __tablename__ = 'plans'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, default=0)
    currency = db.Column(db.String(10), default='VND')
    chat_limit = db.Column(db.Integer, default=10)
    lesson_limit = db.Column(db.Integer, default=1)
    can_speak = db.Column(db.Boolean, default=True)
    can_save_history = db.Column(db.Boolean, default=True)
    enabled = db.Column(db.Boolean, default=True)
    description = db.Column(db.String(255), default='')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'price': self.price,
            'currency': self.currency,
            'chat_limit': self.chat_limit,
            'lesson_limit': self.lesson_limit,
            'can_speak': self.can_speak,
            'can_save_history': self.can_save_history,
            'enabled': self.enabled,
            'description': self.description
        }


class UsageLog(db.Model):
    """Track daily usage counts and estimated AI cost"""
    __tablename__ = 'usage_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    chat_count = db.Column(db.Integer, default=0)
    lesson_count = db.Column(db.Integer, default=0)
    speaking_count = db.Column(db.Integer, default=0)
    ai_provider = db.Column(db.String(50), default='openai')
    estimated_cost = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'date': self.date.isoformat() if self.date else None,
            'chat_count': self.chat_count,
            'lesson_count': self.lesson_count,
            'speaking_count': self.speaking_count,
            'ai_provider': self.ai_provider,
            'estimated_cost': self.estimated_cost
        }


class PaymentRequest(db.Model):
    """Payment request created by users for manual payment"""
    __tablename__ = 'payment_requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_name = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(10), default='VND')
    status = db.Column(db.String(20), default='pending')
    reference_code = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_name': self.plan_name,
            'amount': self.amount,
            'currency': self.currency,
            'status': self.status,
            'reference_code': self.reference_code,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None
        }


class PaymentHistory(db.Model):
    """Store approved payment records"""
    __tablename__ = 'payment_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_name = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(10), default='VND')
    status = db.Column(db.String(20), default='approved')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_name': self.plan_name,
            'amount': self.amount,
            'currency': self.currency,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Feedback(db.Model):
    """User feedback and suggestions"""
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    category = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='new')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category': self.category,
            'content': self.content,
            'rating': self.rating,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
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


def _ensure_sqlite_columns(engine):
    inspector = inspect(engine)
    if not inspector.has_table('users'):
        return

    existing_columns = {col['name'] for col in inspector.get_columns('users')}
    alter_statements = []

    if 'role' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user'")
    if 'status' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'trial'")
    if 'plan_name' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN plan_name VARCHAR(50) DEFAULT 'free_trial'")
    if 'plan_start' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN plan_start DATETIME")
    if 'plan_end' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN plan_end DATETIME")
    if 'trial_end' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN trial_end DATETIME")
    if 'reminder_enabled' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN reminder_enabled BOOLEAN DEFAULT 1")
    if 'reminder_hour' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN reminder_hour VARCHAR(5) DEFAULT '20:00'")
    if 'reminder_message' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN reminder_message VARCHAR(255) DEFAULT 'Hôm nay em học 5 phút với Ms. Smile nhé 😊'")
    if 'is_locked' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN is_locked BOOLEAN DEFAULT 0")

    if alter_statements:
        with engine.connect() as conn:
            for statement in alter_statements:
                try:
                    conn.execute(text(statement))
                except Exception as e:
                    print(f"[DB] Failed to alter users table: {e}")


def seed_default_plans():
    try:
        from config import get_plan_definitions
        for plan in get_plan_definitions():
            existing = Plan.query.filter_by(name=plan['name']).first()
            if not existing:
                new_plan = Plan(
                    name=plan['name'],
                    title=plan['title'],
                    price=plan['price'],
                    currency=plan.get('currency', 'VND'),
                    chat_limit=plan['chat_limit'],
                    lesson_limit=plan['lesson_limit'],
                    can_speak=plan['can_speak'],
                    can_save_history=plan['can_save_history'],
                    enabled=plan['enabled'],
                    description=plan.get('description', '')
                )
                db.session.add(new_plan)
        db.session.commit()
    except Exception as e:
        print(f"[DB] Seed default plans failed: {e}")


def init_db(app):
    """Initialize database"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        engine = db.engine
        if engine.dialect.name == 'sqlite':
            _ensure_sqlite_columns(engine)
        seed_default_plans()
        seed_default_admin()


def seed_default_admin():
    try:
        default_email = os.getenv('ADMIN_EMAIL', 'admin@ms-smile.local')
        default_password = os.getenv('ADMIN_PASSWORD', 'Admin123')
        default_name = os.getenv('ADMIN_NAME', 'Ms Smile Admin')

        existing_admin = User.query.filter_by(role='admin').first()
        if not existing_admin:
            admin = User(
                email=default_email,
                name=default_name,
                role='admin',
                status='active',
                plan_name='premium',
                plan_start=datetime.utcnow(),
                plan_end=datetime.utcnow() + timedelta(days=365),
                trial_end=None,
                reminder_enabled=True,
                reminder_hour='20:00',
                reminder_message='Kiểm tra hệ thống và phản hồi người dùng.',
                is_locked=False
            )
            admin.set_password(default_password)
            db.session.add(admin)
            db.session.commit()
            print(f"[DB] Default admin created: {default_email}")
    except Exception as e:
        print(f"[DB] Failed to seed default admin: {e}")
