"""
User authentication and profile management service
"""
from datetime import datetime, date, timedelta
from typing import Dict, Optional, Tuple
from models import db, User, UserProgress, LearningSession, CommonError, UserActivity

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
            name=name or 'User'
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
        
        if not user.check_password(password):
            return False, {'error': 'Mật khẩu không đúng'}
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        return True, {'user': user.to_dict(), 'message': 'Đăng nhập thành công'}
    
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
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return User.query.get(user_id)
    
    def get_user_progress(self, user_id: int) -> Optional[UserProgress]:
        """Get user progress"""
        return UserProgress.query.filter_by(user_id=user_id).first()
    
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
