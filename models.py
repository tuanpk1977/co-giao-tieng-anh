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
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Fixed identifiers - NEVER change these
    user_code = db.Column(db.String(50), unique=True, nullable=False)  # pair_id
    referral_code = db.Column(db.String(50), unique=True, nullable=True)  # Agent code to share
    referred_by = db.Column(db.String(50), nullable=True)  # Who referred this user
    
    # Profile info
    age = db.Column(db.Integer)
    job = db.Column(db.String(50))  # sales, engineer, cafe, office, student, other
    meet_foreigners = db.Column(db.Boolean, default=False)
    english_usage = db.Column(db.String(200))  # what they use English for
    goal = db.Column(db.String(50))  # daily, work, travel
    english_level = db.Column(db.String(20), default='beginner')
    learning_path = db.Column(db.String(50), default='communication')
    grade_level = db.Column(db.String(50))
    
    # Subscription and payment info
    role = db.Column(db.String(20), default='user')  # user, agent, admin
    status = db.Column(db.String(20), default='trial')  # trial, active, expired, banned
    agent_status = db.Column(db.String(20), nullable=True)  # pending, approved, suspended (only if role=agent)
    plan_name = db.Column(db.String(50), default='free_trial')
    
    # Explicit subscription dates
    trial_start = db.Column(db.DateTime)
    trial_end = db.Column(db.DateTime)
    subscription_start = db.Column(db.DateTime)
    subscription_end = db.Column(db.DateTime)
    
    # Keep legacy fields for compatibility
    plan_start = db.Column(db.DateTime)
    plan_end = db.Column(db.DateTime)
    
    reminder_enabled = db.Column(db.Boolean, default=True)
    reminder_hour = db.Column(db.String(5), default='20:00')
    reminder_message = db.Column(db.String(255), default='Hôm nay em học 5 phút với Ms. Smile nhé 😊')
    is_locked = db.Column(db.Boolean, default=False)
    max_tokens_per_day_override = db.Column(db.Integer, nullable=True)
    max_tokens_per_month_override = db.Column(db.Integer, nullable=True)
    max_cost_per_day_vnd_override = db.Column(db.Float, nullable=True)

    # Relationships
    progress = db.relationship('UserProgress', backref='user', lazy=True, uselist=False)
    sessions = db.relationship('LearningSession', backref='user', lazy=True)
    errors = db.relationship('CommonError', backref='user', lazy=True)
    reminders = db.relationship('ReminderLog', backref='user', lazy=True)
    usage_logs = db.relationship('UsageLog', backref='user', lazy=True)
    payment_requests = db.relationship('PaymentRequest', backref='user', lazy=True)
    payment_history = db.relationship('PaymentHistory', backref='user', lazy=True)
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)
    affiliate_profile = db.relationship('AffiliateProfile', backref='user', lazy=True, uselist=False)
    referrals_sent = db.relationship('Referral', foreign_keys='Referral.referrer_user_id', backref='referrer', lazy=True)
    referrals_received = db.relationship('Referral', foreign_keys='Referral.referred_user_id', backref='referred', lazy=True)
    commissions = db.relationship('AffiliateCommission', foreign_keys='AffiliateCommission.affiliate_user_id', backref='affiliate', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_code': self.user_code,
            'email': self.email,
            'phone': self.phone,
            'name': self.name,
            'age': self.age,
            'job': self.job,
            'meet_foreigners': self.meet_foreigners,
            'english_usage': self.english_usage,
            'goal': self.goal,
            'english_level': self.english_level,
            'learning_path': self.learning_path,
            'grade_level': self.grade_level,
            'role': self.role,
            'status': self.status,
            'agent_status': self.agent_status,
            'plan_name': self.plan_name,
            'plan': self.plan_name,
            'trial_start': self.trial_start.isoformat() if self.trial_start else None,
            'trial_end': self.trial_end.isoformat() if self.trial_end else None,
            'subscription_start': self.subscription_start.isoformat() if self.subscription_start else None,
            'subscription_end': self.subscription_end.isoformat() if self.subscription_end else None,
            'referral_code': self.referral_code,
            'referred_by': self.referred_by,
            'reminder_enabled': self.reminder_enabled,
            'reminder_hour': self.reminder_hour,
            'reminder_message': self.reminder_message,
            'is_locked': self.is_locked,
            'max_tokens_per_day_override': self.max_tokens_per_day_override,
            'max_tokens_per_month_override': self.max_tokens_per_month_override,
            'max_cost_per_day_vnd_override': self.max_cost_per_day_vnd_override,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
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
            'age': self.age,
            'learning_path': self.learning_path or 'communication',
            'grade_level': self.grade_level or ''
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
    
    # PART 2: Quota limits for cost control
    chat_per_day = db.Column(db.Integer, default=10)
    chat_per_month = db.Column(db.Integer, default=300)
    max_tokens_per_chat = db.Column(db.Integer, default=2000)
    max_tokens_per_day = db.Column(db.Integer, default=20000)
    max_tokens_per_month = db.Column(db.Integer, default=600000)
    max_cost_per_day_vnd = db.Column(db.Float, default=0.0)  # 0 = unlimited
    max_cost_per_month_vnd = db.Column(db.Float, default=0.0)  # 0 = unlimited
    family_member_limit = db.Column(db.Integer, default=1)
    
    # NEW: Long-term subscription support
    duration_days = db.Column(db.Integer, default=30)  # 30 for monthly, 180 for 6 months, 365 for yearly
    plan_type = db.Column(db.String(20), default='monthly')  # monthly, six_months, yearly
    discount_percent = db.Column(db.Float, default=0.0)  # discount percentage (0.15 for 15% off, etc.)
    original_price = db.Column(db.Integer, default=0)  # original monthly price for calculating discounts

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
            'description': self.description,
            'chat_per_day': self.chat_per_day,
            'chat_per_month': self.chat_per_month,
            'max_tokens_per_chat': self.max_tokens_per_chat,
            'max_tokens_per_day': self.max_tokens_per_day,
            'max_tokens_per_month': self.max_tokens_per_month,
            'max_cost_per_day_vnd': self.max_cost_per_day_vnd,
            'max_cost_per_month_vnd': self.max_cost_per_month_vnd,
            'family_member_limit': self.family_member_limit,
            'duration_days': self.duration_days,
            'plan_type': self.plan_type,
            'discount_percent': self.discount_percent,
            'original_price': self.original_price
        }


class FamilyMember(db.Model):
    """Users attached to a Family plan owner."""
    __tablename__ = 'family_members'

    id = db.Column(db.Integer, primary_key=True)
    owner_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    member_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    owner = db.relationship('User', foreign_keys=[owner_user_id], lazy=True)
    member = db.relationship('User', foreign_keys=[member_user_id], lazy=True)

    def to_dict(self):
        member = self.member
        return {
            'id': self.id,
            'owner_user_id': self.owner_user_id,
            'member_user_id': self.member_user_id,
            'member_name': member.name if member else None,
            'member_email': member.email if member else None,
            'member_phone': member.phone if member else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class UsageLog(db.Model):
    """PART 1: Track AI usage and estimated costs per user interaction"""
    __tablename__ = 'usage_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Message count tracking
    message_count = db.Column(db.Integer, default=1)  # 1 for single message, 2+ for multi-turn
    chat_count = db.Column(db.Integer, default=1)
    lesson_count = db.Column(db.Integer, default=0)
    speaking_count = db.Column(db.Integer, default=0)
    
    # Token tracking
    input_tokens = db.Column(db.Integer, default=0)
    output_tokens = db.Column(db.Integer, default=0)
    estimated_tokens = db.Column(db.Integer, default=0)  # Used if no actual token count
    
    # Model used
    model = db.Column(db.String(100), default='gpt-4o-mini')
    
    # Cost tracking
    estimated_cost_usd = db.Column(db.Float, default=0.0)
    estimated_cost_vnd = db.Column(db.Float, default=0.0)
    estimated_cost = db.Column(db.Float, default=0.0)
    
    # Metadata
    ai_provider = db.Column(db.String(50), default='openai')
    date = db.Column(db.Date, default=datetime.utcnow().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'message_count': self.message_count,
            'chat_count': self.chat_count,
            'lesson_count': self.lesson_count,
            'speaking_count': self.speaking_count,
            'input_tokens': self.input_tokens,
            'output_tokens': self.output_tokens,
            'estimated_tokens': self.estimated_tokens,
            'model': self.model,
            'estimated_cost': round(self.estimated_cost, 2),
            'estimated_cost_usd': round(self.estimated_cost_usd, 6),
            'estimated_cost_vnd': round(self.estimated_cost_vnd, 0),
            'ai_provider': self.ai_provider,
            'date': self.date.isoformat() if self.date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class CostAnalytics(db.Model):
    """PART 3: Admin dashboard - cost and profitability analytics"""
    __tablename__ = 'cost_analytics'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    
    # Cost tracking
    ai_cost_vnd = db.Column(db.Float, default=0.0)
    ai_cost_usd = db.Column(db.Float, default=0.0)
    
    # Revenue tracking
    revenue_vnd = db.Column(db.Float, default=0.0)
    
    # Usage metrics
    chat_count = db.Column(db.Integer, default=0)
    total_tokens = db.Column(db.Integer, default=0)
    
    # Status
    is_profitable = db.Column(db.Boolean, default=True)
    profit_loss_vnd = db.Column(db.Float, default=0.0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat() if self.date else None,
            'ai_cost_vnd': round(self.ai_cost_vnd, 0),
            'ai_cost_usd': round(self.ai_cost_usd, 6),
            'revenue_vnd': round(self.revenue_vnd, 0),
            'chat_count': self.chat_count,
            'total_tokens': self.total_tokens,
            'is_profitable': self.is_profitable,
            'profit_loss_vnd': round(self.profit_loss_vnd, 0),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class UserUsageCost(db.Model):
    """Daily/monthly user-level profit and AI cost tracking."""
    __tablename__ = 'user_usage_costs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date, nullable=False)
    month = db.Column(db.String(7), nullable=False)
    chat_count = db.Column(db.Integer, default=0)
    lesson_count = db.Column(db.Integer, default=0)
    speaking_count = db.Column(db.Integer, default=0)
    input_tokens = db.Column(db.Integer, default=0)
    output_tokens = db.Column(db.Integer, default=0)
    total_tokens = db.Column(db.Integer, default=0)
    estimated_ai_cost_usd = db.Column(db.Float, default=0.0)
    estimated_ai_cost_vnd = db.Column(db.Float, default=0.0)
    revenue_vnd = db.Column(db.Float, default=0.0)
    gross_profit_vnd = db.Column(db.Float, default=0.0)
    profit_margin_percent = db.Column(db.Float, default=0.0)
    risk_level = db.Column(db.String(20), default='safe')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat() if self.date else None,
            'month': self.month,
            'chat_count': self.chat_count,
            'lesson_count': self.lesson_count,
            'speaking_count': self.speaking_count,
            'input_tokens': self.input_tokens,
            'output_tokens': self.output_tokens,
            'total_tokens': self.total_tokens,
            'estimated_ai_cost_usd': round(self.estimated_ai_cost_usd or 0, 6),
            'estimated_ai_cost_vnd': round(self.estimated_ai_cost_vnd or 0, 0),
            'revenue_vnd': round(self.revenue_vnd or 0, 0),
            'gross_profit_vnd': round(self.gross_profit_vnd or 0, 0),
            'profit_margin_percent': round(self.profit_margin_percent or 0, 2),
            'risk_level': self.risk_level,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class AdminAlert(db.Model):
    """Admin alerts for cost risk transitions."""
    __tablename__ = 'admin_alerts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'message': self.message,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user': self.user.to_dict() if self.user else None
        }


class AffiliateProfile(db.Model):
    """Affiliate profile for referrers"""
    __tablename__ = 'affiliate_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    affiliate_code = db.Column(db.String(50), unique=True, nullable=False)
    referral_link = db.Column(db.String(255), nullable=False)
    commission_rate = db.Column(db.Float, default=20.0)
    commission_type = db.Column(db.String(20), default='percent')
    commission_percent = db.Column(db.Float, default=20.0)
    commission_fixed_amount = db.Column(db.Integer, default=0)
    total_referrals = db.Column(db.Integer, default=0)
    total_commission = db.Column(db.Float, default=0.0)
    pending_commission = db.Column(db.Float, default=0.0)
    paid_commission = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'affiliate_code': self.affiliate_code,
            'referral_link': self.referral_link,
            'commission_rate': self.commission_rate,
            'commission_type': self.commission_type,
            'commission_percent': self.commission_percent,
            'commission_fixed_amount': self.commission_fixed_amount,
            'total_referrals': self.total_referrals,
            'total_commission': self.total_commission,
            'pending_commission': self.pending_commission,
            'paid_commission': self.paid_commission,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Referral(db.Model):
    """Referral record from a referrer to a referred user"""
    __tablename__ = 'referrals'

    id = db.Column(db.Integer, primary_key=True)
    referrer_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    referred_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    referral_code = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    first_payment_at = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')

    def to_dict(self):
        return {
            'id': self.id,
            'referrer_user_id': self.referrer_user_id,
            'referred_user_id': self.referred_user_id,
            'referral_code': self.referral_code,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'first_payment_at': self.first_payment_at.isoformat() if self.first_payment_at else None,
            'status': self.status
        }


class AffiliateCommission(db.Model):
    """Commission record generated from referred payments"""
    __tablename__ = 'affiliate_commissions'

    id = db.Column(db.Integer, primary_key=True)
    affiliate_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    referred_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    payment_id = db.Column(db.Integer, nullable=False)
    amount_vnd = db.Column(db.Float, nullable=False)
    commission_rate = db.Column(db.Float, nullable=False)
    commission_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'affiliate_user_id': self.affiliate_user_id,
            'referred_user_id': self.referred_user_id,
            'payment_id': self.payment_id,
            'amount_vnd': self.amount_vnd,
            'commission_rate': self.commission_rate,
            'commission_amount': self.commission_amount,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None
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
    transfer_note = db.Column(db.String(100))
    bank_info = db.Column(db.Text)
    screenshot = db.Column(db.String(255))
    customer_confirmed_at = db.Column(db.DateTime)
    customer_note = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)

    def to_dict(self):
        user = self.user
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': user.name if user else None,
            'user_email': user.email if user else None,
            'user_phone': user.phone if user else None,
            'plan_name': self.plan_name,
            'amount': self.amount,
            'currency': self.currency,
            'status': self.status,
            'reference_code': self.reference_code,
            'transfer_note': self.transfer_note or self.reference_code,
            'bank_info': self.bank_info,
            'screenshot': self.screenshot,
            'customer_confirmed_at': self.customer_confirmed_at.isoformat() if self.customer_confirmed_at else None,
            'customer_note': self.customer_note,
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


class UserRoadmapProgress(db.Model):
    """Progress inside the fixed Hybrid Learning Roadmap."""
    __tablename__ = 'user_roadmap_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    level_id = db.Column(db.String(80), nullable=False)
    unit_id = db.Column(db.String(80), nullable=True)
    lesson_id = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(20), default='in_progress')
    score = db.Column(db.Float, default=0.0)
    completed_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'lesson_id', name='uq_user_roadmap_lesson'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'level_id': self.level_id,
            'unit_id': self.unit_id,
            'lesson_id': self.lesson_id,
            'status': self.status,
            'score': self.score,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class AIUsageLog(db.Model):
    """Feature-level AI usage log for cost controls in the hybrid roadmap."""
    __tablename__ = 'ai_usage_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    feature_type = db.Column(db.String(50), nullable=False)
    token_used = db.Column(db.Integer, default=0)
    estimated_cost = db.Column(db.Float, default=0.0)
    plan_type = db.Column(db.String(50), default='free')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'featureType': self.feature_type,
            'tokenUsed': self.token_used,
            'estimatedCost': self.estimated_cost,
            'planType': self.plan_type,
            'createdAt': self.created_at.isoformat() if self.created_at else None
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

    # Check users table
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
    if 'max_tokens_per_day_override' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN max_tokens_per_day_override INTEGER")
    if 'max_tokens_per_month_override' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN max_tokens_per_month_override INTEGER")
    if 'max_cost_per_day_vnd_override' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN max_cost_per_day_vnd_override FLOAT")
    if 'learning_path' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN learning_path VARCHAR(50) DEFAULT 'communication'")
    if 'grade_level' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN grade_level VARCHAR(50)")
    
    # New columns for fixed account model (BenNha style)
    if 'user_code' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN user_code VARCHAR(12)")
    if 'referral_code' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN referral_code VARCHAR(50)")
    if 'referred_by' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN referred_by VARCHAR(50)")
    if 'agent_status' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN agent_status VARCHAR(20)")
    if 'trial_start' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN trial_start DATETIME")
    if 'subscription_start' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN subscription_start DATETIME")
    if 'subscription_end' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN subscription_end DATETIME")
    if 'updated_at' not in existing_columns:
        alter_statements.append("ALTER TABLE users ADD COLUMN updated_at DATETIME")
    
    if alter_statements:
        with engine.connect() as conn:
            for statement in alter_statements:
                try:
                    conn.execute(text(statement))
                    conn.commit()
                except Exception as e:
                    print(f"[DB] Failed to alter users table: {e}")
            try:
                rows = conn.execute(text("SELECT id FROM users WHERE user_code IS NULL OR user_code = ''")).fetchall()
                for row in rows:
                    conn.execute(text("UPDATE users SET user_code = :code WHERE id = :id"), {
                        "code": f"MSE{row[0]:08d}",
                        "id": row[0]
                    })
                conn.commit()
            except Exception as e:
                print(f"[DB] Failed to backfill user_code: {e}")
    
    # PART 2: Check plans table for quota columns
    if inspector.has_table('plans'):
        plan_columns = {col['name'] for col in inspector.get_columns('plans')}
        plan_alters = []
        
        if 'chat_per_day' not in plan_columns:
            plan_alters.append("ALTER TABLE plans ADD COLUMN chat_per_day INTEGER DEFAULT 10")
        if 'chat_per_month' not in plan_columns:
            plan_alters.append("ALTER TABLE plans ADD COLUMN chat_per_month INTEGER DEFAULT 300")
        if 'max_tokens_per_chat' not in plan_columns:
            plan_alters.append("ALTER TABLE plans ADD COLUMN max_tokens_per_chat INTEGER DEFAULT 2000")
        if 'max_tokens_per_day' not in plan_columns:
            plan_alters.append("ALTER TABLE plans ADD COLUMN max_tokens_per_day INTEGER DEFAULT 20000")
        if 'max_tokens_per_month' not in plan_columns:
            plan_alters.append("ALTER TABLE plans ADD COLUMN max_tokens_per_month INTEGER DEFAULT 600000")
        if 'max_cost_per_day_vnd' not in plan_columns:
            plan_alters.append("ALTER TABLE plans ADD COLUMN max_cost_per_day_vnd FLOAT DEFAULT 0.0")
        if 'max_cost_per_month_vnd' not in plan_columns:
            plan_alters.append("ALTER TABLE plans ADD COLUMN max_cost_per_month_vnd FLOAT DEFAULT 0.0")
        if 'family_member_limit' not in plan_columns:
            plan_alters.append("ALTER TABLE plans ADD COLUMN family_member_limit INTEGER DEFAULT 1")
        
        # NEW: Long-term subscription columns
        if 'duration_days' not in plan_columns:
            plan_alters.append("ALTER TABLE plans ADD COLUMN duration_days INTEGER DEFAULT 30")
        if 'plan_type' not in plan_columns:
            plan_alters.append("ALTER TABLE plans ADD COLUMN plan_type VARCHAR(20) DEFAULT 'monthly'")
        if 'discount_percent' not in plan_columns:
            plan_alters.append("ALTER TABLE plans ADD COLUMN discount_percent FLOAT DEFAULT 0.0")
        if 'original_price' not in plan_columns:
            plan_alters.append("ALTER TABLE plans ADD COLUMN original_price INTEGER DEFAULT 0")
        
        if plan_alters:
            with engine.connect() as conn:
                for statement in plan_alters:
                    try:
                        conn.execute(text(statement))
                        conn.commit()
                    except Exception as e:
                        print(f"[DB] Failed to alter plans table: {e}")

    if inspector.has_table('usage_logs'):
        usage_columns = {col['name'] for col in inspector.get_columns('usage_logs')}
        usage_alters = []
        if 'message_count' not in usage_columns:
            usage_alters.append("ALTER TABLE usage_logs ADD COLUMN message_count INTEGER DEFAULT 1")
        if 'chat_count' not in usage_columns:
            usage_alters.append("ALTER TABLE usage_logs ADD COLUMN chat_count INTEGER DEFAULT 1")
        if 'lesson_count' not in usage_columns:
            usage_alters.append("ALTER TABLE usage_logs ADD COLUMN lesson_count INTEGER DEFAULT 0")
        if 'speaking_count' not in usage_columns:
            usage_alters.append("ALTER TABLE usage_logs ADD COLUMN speaking_count INTEGER DEFAULT 0")
        if 'input_tokens' not in usage_columns:
            usage_alters.append("ALTER TABLE usage_logs ADD COLUMN input_tokens INTEGER DEFAULT 0")
        if 'output_tokens' not in usage_columns:
            usage_alters.append("ALTER TABLE usage_logs ADD COLUMN output_tokens INTEGER DEFAULT 0")
        if 'estimated_tokens' not in usage_columns:
            usage_alters.append("ALTER TABLE usage_logs ADD COLUMN estimated_tokens INTEGER DEFAULT 0")
        if 'model' not in usage_columns:
            usage_alters.append("ALTER TABLE usage_logs ADD COLUMN model VARCHAR(100) DEFAULT 'gpt-4o-mini'")
        if 'estimated_cost_usd' not in usage_columns:
            usage_alters.append("ALTER TABLE usage_logs ADD COLUMN estimated_cost_usd FLOAT DEFAULT 0.0")
        if 'estimated_cost_vnd' not in usage_columns:
            usage_alters.append("ALTER TABLE usage_logs ADD COLUMN estimated_cost_vnd FLOAT DEFAULT 0.0")
        if 'estimated_cost' not in usage_columns:
            usage_alters.append("ALTER TABLE usage_logs ADD COLUMN estimated_cost FLOAT DEFAULT 0.0")
        if 'ai_provider' not in usage_columns:
            usage_alters.append("ALTER TABLE usage_logs ADD COLUMN ai_provider VARCHAR(50) DEFAULT 'openai'")
        if 'date' not in usage_columns:
            usage_alters.append("ALTER TABLE usage_logs ADD COLUMN date DATE")
        if 'created_at' not in usage_columns:
            usage_alters.append("ALTER TABLE usage_logs ADD COLUMN created_at DATETIME")
        if usage_alters:
            with engine.connect() as conn:
                for statement in usage_alters:
                    try:
                        conn.execute(text(statement))
                    except Exception as e:
                        print(f"[DB] Failed to alter usage_logs table: {e}")
                conn.commit()

    if inspector.has_table('payment_requests'):
        payment_columns = {col['name'] for col in inspector.get_columns('payment_requests')}
        payment_alters = []
        if 'transfer_note' not in payment_columns:
            payment_alters.append("ALTER TABLE payment_requests ADD COLUMN transfer_note VARCHAR(100)")
        if 'bank_info' not in payment_columns:
            payment_alters.append("ALTER TABLE payment_requests ADD COLUMN bank_info TEXT")
        if 'screenshot' not in payment_columns:
            payment_alters.append("ALTER TABLE payment_requests ADD COLUMN screenshot VARCHAR(255)")
        if 'customer_confirmed_at' not in payment_columns:
            payment_alters.append("ALTER TABLE payment_requests ADD COLUMN customer_confirmed_at DATETIME")
        if 'customer_note' not in payment_columns:
            payment_alters.append("ALTER TABLE payment_requests ADD COLUMN customer_note VARCHAR(255)")
        if payment_alters:
            with engine.connect() as conn:
                for statement in payment_alters:
                    try:
                        conn.execute(text(statement))
                    except Exception as e:
                        print(f"[DB] Failed to alter payment_requests table: {e}")
                conn.commit()

    if inspector.has_table('affiliate_profiles'):
        affiliate_columns = {col['name'] for col in inspector.get_columns('affiliate_profiles')}
        affiliate_alters = []
        if 'commission_type' not in affiliate_columns:
            affiliate_alters.append("ALTER TABLE affiliate_profiles ADD COLUMN commission_type VARCHAR(20) DEFAULT 'percent'")
        if 'commission_percent' not in affiliate_columns:
            affiliate_alters.append("ALTER TABLE affiliate_profiles ADD COLUMN commission_percent FLOAT DEFAULT 20.0")
        if 'commission_fixed_amount' not in affiliate_columns:
            affiliate_alters.append("ALTER TABLE affiliate_profiles ADD COLUMN commission_fixed_amount INTEGER DEFAULT 0")
        if affiliate_alters:
            with engine.connect() as conn:
                for statement in affiliate_alters:
                    try:
                        conn.execute(text(statement))
                    except Exception as e:
                        print(f"[DB] Failed to alter affiliate_profiles table: {e}")
                conn.commit()


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
                    description=plan.get('description', ''),
                    chat_per_day=plan.get('chat_per_day', plan['chat_limit']),
                    chat_per_month=plan.get('chat_per_month', plan['chat_limit'] * 30),
                    max_tokens_per_chat=plan.get('max_tokens_per_chat', 2000),
                    max_tokens_per_day=plan.get('max_tokens_per_day', 20000),
                    max_tokens_per_month=plan.get('max_tokens_per_month', 600000),
                    max_cost_per_day_vnd=plan.get('max_cost_per_day_vnd', 0.0),
                    max_cost_per_month_vnd=plan.get('max_cost_per_month_vnd', 0.0),
                    family_member_limit=plan.get('family_member_limit', 1),
                    # NEW: Long-term subscription fields
                    duration_days=plan.get('duration_days', 30),
                    plan_type=plan.get('plan_type', 'monthly'),
                    discount_percent=plan.get('discount_percent', 0.0),
                    original_price=plan.get('original_price', plan['price'])
                )
                db.session.add(new_plan)
            else:
                existing.title = plan.get('title', existing.title)
                existing.price = plan.get('price', existing.price)
                existing.currency = plan.get('currency', existing.currency)
                existing.chat_limit = plan.get('chat_limit', existing.chat_limit)
                existing.lesson_limit = plan.get('lesson_limit', existing.lesson_limit)
                existing.can_speak = plan.get('can_speak', existing.can_speak)
                existing.can_save_history = plan.get('can_save_history', existing.can_save_history)
                existing.enabled = plan.get('enabled', existing.enabled)
                existing.description = plan.get('description', existing.description)
                existing.chat_per_day = plan.get('chat_per_day', existing.chat_per_day)
                existing.chat_per_month = plan.get('chat_per_month', existing.chat_per_month)
                existing.max_tokens_per_chat = plan.get('max_tokens_per_chat', existing.max_tokens_per_chat)
                existing.max_tokens_per_day = plan.get('max_tokens_per_day', existing.max_tokens_per_day)
                existing.max_tokens_per_month = plan.get('max_tokens_per_month', existing.max_tokens_per_month)
                existing.max_cost_per_day_vnd = plan.get('max_cost_per_day_vnd', existing.max_cost_per_day_vnd)
                existing.max_cost_per_month_vnd = plan.get('max_cost_per_month_vnd', existing.max_cost_per_month_vnd)
                existing.family_member_limit = plan.get('family_member_limit', existing.family_member_limit)
                # NEW: Update long-term subscription fields
                existing.duration_days = plan.get('duration_days', existing.duration_days)
                existing.plan_type = plan.get('plan_type', existing.plan_type)
                existing.discount_percent = plan.get('discount_percent', existing.discount_percent)
                existing.original_price = plan.get('original_price', existing.original_price)
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
        import config
        default_email = os.getenv('ADMIN_EMAIL', 'admin@ms-smile.local')
        default_password = os.getenv('ADMIN_PASSWORD', 'Admin123')
        default_name = os.getenv('ADMIN_NAME', 'Ms Smile Admin')
        admin_affiliate_code = config.ADMIN_AFFILIATE_CODE

        existing_admin = User.query.filter_by(role='admin').first()
        if not existing_admin:
            admin = User(
                email=default_email,
                name=default_name,
                user_code='ADMIN00000001',
                role='admin',
                status='active',
                plan_name='family',
                subscription_start=datetime.utcnow(),
                subscription_end=datetime.utcnow() + timedelta(days=365),
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
            
            # PART 3: Create affiliate profile for admin as default referrer
            referral_link = f"{config.AFFILIATE_REFERRAL_LINK_BASE}/?ref={admin_affiliate_code}"
            affiliate_profile = AffiliateProfile(
                user_id=admin.id,
                affiliate_code=admin_affiliate_code,
                referral_link=referral_link,
                commission_rate=config.AFFILIATE_COMMISSION_RATE,
                commission_type=os.getenv('AFFILIATE_COMMISSION_TYPE', 'percent'),
                commission_percent=config.AFFILIATE_COMMISSION_RATE,
                commission_fixed_amount=int(os.getenv('AFFILIATE_COMMISSION_FIXED_AMOUNT', '0')),
                status='approved'
            )
            db.session.add(affiliate_profile)
            db.session.commit()
            print(f"[DB] Admin affiliate profile created with code: {admin_affiliate_code}")
        else:
            changed = False
            if not existing_admin.user_code:
                existing_admin.user_code = 'ADMIN00000001'
                changed = True
            if existing_admin.email != default_email and default_email:
                existing_admin.email = default_email
                changed = True
            if os.getenv('ADMIN_PASSWORD'):
                existing_admin.set_password(default_password)
                changed = True
            if changed:
                db.session.commit()
    except Exception as e:
        print(f"[DB] Failed to seed default admin: {e}")
