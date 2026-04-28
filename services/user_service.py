"""
User authentication and profile management service
"""
from datetime import datetime, date, timedelta
from typing import Dict, Optional, Tuple
from models import (
    db, User, UserProgress, LearningSession, CommonError, UserActivity,
    Plan, UsageLog, PaymentRequest, PaymentHistory, Feedback
)
import config

class UserService:
    """Service for user management"""
    
    def __init__(self):
        pass
    
    def register_user(self, email: str = None, phone: str = None, 
                      password: str = None, name: str = None) -> Tuple[bool, Dict]:
        """Register new user"""
        if not email and not phone:
            return False, {'error': 'Cần email hoặc số điện thoại'}
        
        if not password or len(password) < 6:
            return False, {'error': 'Mật khẩu cần ít nhất 6 ký tự'}
        
        # Check if exists
        if email:
            existing = User.query.filter_by(email=email).first()
            if existing:
                return False, {'error': 'Email đã được sử dụng'}
        
        if phone:
            existing = User.query.filter_by(phone=phone).first()
            if existing:
                return False, {'error': 'Số điện thoại đã được sử dụng'}
        
        # Create user
        user = User(
            email=email,
            phone=phone,
            name=name or 'User',
            role='user',
            status='trial',
            plan_name='free_trial',
            plan_start=datetime.utcnow(),
            trial_end=datetime.utcnow() + timedelta(days=config.FREE_TRIAL_DAYS),
            reminder_enabled=True,
            reminder_hour='20:00',
            reminder_message='Hôm nay em học 5 phút với Ms. Smile nhé 😊',
            is_locked=False
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Create empty progress
        progress = UserProgress(user_id=user.id)
        db.session.add(progress)
        db.session.commit()
        
        return True, {'user': user.to_dict(), 'message': 'Đăng ký thành công'}
    
    def login_user(self, email: str = None, phone: str = None, 
                   password: str = None) -> Tuple[bool, Dict]:
        """Login user"""
        if email:
            user = User.query.filter_by(email=email).first()
        elif phone:
            user = User.query.filter_by(phone=phone).first()
        else:
            return False, {'error': 'Cần email hoặc số điện thoại'}
        
        if not user:
            return False, {'error': 'Tài khoản không tồn tại'}
        
        if user.is_locked or user.status == 'banned':
            return False, {'error': 'Tài khoản đã bị khóa. Liên hệ admin để mở lại.'}
        
        self._refresh_user_status(user)
        
        if not user.check_password(password):
            return False, {'error': 'Mật khẩu không đúng'}
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        return True, {'user': user.to_dict(), 'message': 'Đăng nhập thành công'}

    def _refresh_user_status(self, user: User):
        now = datetime.utcnow()
        changed = False
        if user.status == 'trial' and user.trial_end and now > user.trial_end:
            user.status = 'expired'
            changed = True
        if user.status == 'active' and user.plan_end and now > user.plan_end:
            user.status = 'expired'
            changed = True
        if changed:
            db.session.commit()
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        user = User.query.get(user_id)
        if user:
            self._refresh_user_status(user)
        return user
    
    def setup_profile(self, user_id: int, profile_data: Dict) -> Tuple[bool, Dict]:
        """Setup user profile after registration"""
        user = User.query.get(user_id)
        if not user:
            return False, {'error': 'User không tồn tại'}
        
        user.age = profile_data.get('age')
        user.job = profile_data.get('job')
        user.meet_foreigners = profile_data.get('meet_foreigners', False)
        user.english_usage = profile_data.get('english_usage')
        user.goal = profile_data.get('goal')
        user.english_level = profile_data.get('level', 'beginner')
        
        db.session.commit()
        
        return True, {'user': user.to_dict(), 'message': 'Cập nhật profile thành công'}
    
    def get_user_progress(self, user_id: int) -> Optional[UserProgress]:
        """Get user progress"""
        return UserProgress.query.filter_by(user_id=user_id).first()

    def get_all_plans(self):
        return Plan.query.filter_by(enabled=True).all()

    def get_all_users(self):
        return User.query.order_by(User.created_at.desc()).all()

    def get_plan(self, plan_name: str) -> Optional[Plan]:
        return Plan.query.filter_by(name=plan_name).first()

    def get_usage_log(self, user_id: int, date_obj=None) -> UsageLog:
        if date_obj is None:
            date_obj = datetime.utcnow().date()
        log = UsageLog.query.filter_by(user_id=user_id, date=date_obj).first()
        if not log:
            log = UsageLog(user_id=user_id, date=date_obj, ai_provider=config.AI_PROVIDER)
            db.session.add(log)
            db.session.commit()
        return log

    def increment_usage(self, user_id: int, chat_increment=0, lesson_increment=0, speaking_increment=0, estimated_cost=0.0):
        log = self.get_usage_log(user_id)
        log.chat_count += chat_increment
        log.lesson_count += lesson_increment
        log.speaking_count += speaking_increment
        log.estimated_cost += estimated_cost
        db.session.commit()
        return log

    def create_payment_request(self, user_id: int, plan_name: str):
        plan = self.get_plan(plan_name)
        if not plan:
            return False, {'error': 'Plan không tồn tại'}

        reference_code = f"MSE-{user_id}-{plan_name}-{int(datetime.utcnow().timestamp())}"
        payment_request = PaymentRequest(
            user_id=user_id,
            plan_name=plan_name,
            amount=plan.price,
            currency=plan.currency,
            status='pending',
            reference_code=reference_code
        )
        db.session.add(payment_request)
        db.session.commit()

        return True, {'payment_request': payment_request.to_dict()}

    def approve_payment(self, payment_id: int):
        payment = PaymentRequest.query.get(payment_id)
        if not payment:
            return False, {'error': 'Payment request không tồn tại'}
        if payment.status != 'pending':
            return False, {'error': 'Payment request đã xử lý'}

        user = self.get_user(payment.user_id)
        plan = self.get_plan(payment.plan_name)
        if not user or not plan:
            return False, {'error': 'User hoặc plan không hợp lệ'}

        payment.status = 'approved'
        payment.approved_at = datetime.utcnow()
        db.session.commit()

        history = PaymentHistory(
            user_id=user.id,
            plan_name=plan.name,
            amount=payment.amount,
            currency=payment.currency,
            status='approved'
        )
        db.session.add(history)

        user.plan_name = plan.name
        user.status = 'active'
        user.plan_start = datetime.utcnow()
        user.plan_end = datetime.utcnow() + timedelta(days=30)
        user.trial_end = None
        db.session.commit()

        return True, {'message': 'Payment approved and subscription activated', 'payment': payment.to_dict()}

    def get_payment_requests(self, status='pending'):
        return PaymentRequest.query.filter_by(status=status).all()

    def get_payment_history(self, user_id: int):
        return PaymentHistory.query.filter_by(user_id=user_id).all()

    def create_feedback(self, user_id: int, category: str, content: str, rating: int):
        feedback = Feedback(
            user_id=user_id,
            category=category,
            content=content,
            rating=rating,
            status='new'
        )
        db.session.add(feedback)
        db.session.commit()
        return feedback

    def get_feedbacks(self, status='new'):
        return Feedback.query.filter_by(status=status).order_by(Feedback.created_at.desc()).all()

    def update_feedback_status(self, feedback_id: int, status: str):
        feedback = Feedback.query.get(feedback_id)
        if not feedback:
            return False, {'error': 'Feedback không tồn tại'}
        feedback.status = status
        feedback.updated_at = datetime.utcnow()
        db.session.commit()
        return True, {'feedback': feedback.to_dict()}

    def get_admin_summary(self):
        total_users = User.query.count()
        trials = User.query.filter_by(status='trial').count()
        active = User.query.filter_by(status='active').count()
        expired = User.query.filter_by(status='expired').count()
        banned = User.query.filter_by(status='banned').count()
        pending_payments = PaymentRequest.query.filter_by(status='pending').count()
        new_feedback = Feedback.query.filter_by(status='new').count()
        today = datetime.utcnow().date()
        total_chat_today = UsageLog.query.filter_by(date=today).with_entities(db.func.sum(UsageLog.chat_count)).scalar() or 0
        estimated_cost = UsageLog.query.filter_by(date=today).with_entities(db.func.sum(UsageLog.estimated_cost)).scalar() or 0.0
        return {
            'total_users': total_users,
            'trial_users': trials,
            'active_users': active,
            'expired_users': expired,
            'banned_users': banned,
            'pending_payments': pending_payments,
            'new_feedback': new_feedback,
            'total_chat_today': total_chat_today,
            'estimated_cost_today': round(estimated_cost, 2)
        }
    
    def update_streak(self, user_id: int):
        """Update study streak"""
        progress = self.get_user_progress(user_id)
        if not progress:
            return
        
        today = date.today()
        
        if progress.last_study_date:
            days_diff = (today - progress.last_study_date).days
            
            if days_diff == 0:
                # Already studied today
                return
            elif days_diff == 1:
                # Consecutive day
                progress.current_streak += 1
                progress.total_days_studied += 1
            else:
                # Streak broken
                progress.current_streak = 1
                progress.total_days_studied += 1
            
            # Update longest streak
            if progress.current_streak > progress.longest_streak:
                progress.longest_streak = progress.current_streak
        else:
            # First time studying
            progress.current_streak = 1
            progress.total_days_studied = 1
        
        progress.last_study_date = today
        db.session.commit()
    
    def record_session(self, user_id: int, duration: int = 5, 
                       sentences: int = 0, grammar_score: float = None,
                       natural_score: float = None, errors: list = None):
        """Record a learning session"""
        session = LearningSession(
            user_id=user_id,
            duration_minutes=duration,
            sentences_practiced=sentences,
            avg_grammar_score=grammar_score,
            avg_natural_score=natural_score,
            errors_made=str(errors or [])
        )
        db.session.add(session)
        
        # Update progress
        progress = self.get_user_progress(user_id)
        if progress:
            progress.total_sentences_practiced += sentences
            
            # Update average scores
            if grammar_score and natural_score:
                total = progress.total_evaluations
                progress.avg_grammar_score = (
                    (progress.avg_grammar_score * total + grammar_score) / (total + 1)
                )
                progress.avg_natural_score = (
                    (progress.avg_natural_score * total + natural_score) / (total + 1)
                )
                progress.total_evaluations = total + 1
            
            progress.updated_at = datetime.utcnow()
        
        db.session.commit()
    
    def add_common_error(self, user_id: int, error_type: str, 
                         wrong: str, correct: str):
        """Track a common error"""
        existing = CommonError.query.filter_by(
            user_id=user_id, 
            error_type=error_type
        ).first()
        
        if existing:
            existing.error_count += 1
            existing.last_occurrence = datetime.utcnow()
        else:
            error = CommonError(
                user_id=user_id,
                error_type=error_type,
                example_wrong=wrong,
                example_correct=correct
            )
            db.session.add(error)
        
        db.session.commit()
    
    def get_common_errors(self, user_id: int, limit: int = 5) -> list:
        """Get user's most common errors"""
        errors = CommonError.query.filter_by(user_id=user_id)\
            .order_by(CommonError.error_count.desc())\
            .limit(limit).all()
        
        return [{
            'error_type': e.error_type,
            'count': e.error_count,
            'example_wrong': e.example_wrong,
            'example_correct': e.example_correct
        } for e in errors]
    
    def get_inactive_users(self, days: int = 1) -> list:
        """Get users who haven't studied in X days"""
        cutoff = date.today() - timedelta(days=days)
        
        users = User.query.join(UserProgress).filter(
            UserProgress.last_study_date < cutoff
        ).all()
        
        return users
    
    def record_activity(self, user_id: int, activity_type: str, 
                      content: str, ai_response: str = None,
                      grammar_score: int = None, natural_score: int = None,
                      errors: list = None):
        """Record user activity"""
        activity = UserActivity(
            user_id=user_id,
            activity_type=activity_type,
            content=content,
            ai_response=ai_response,
            grammar_score=grammar_score,
            natural_score=natural_score,
            errors=str(errors or [])
        )
        db.session.add(activity)
        db.session.commit()


# Singleton instance
_user_service = None

def get_user_service():
    global _user_service
    if _user_service is None:
        _user_service = UserService()
    return _user_service
