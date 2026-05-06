"""
User authentication and profile management service
"""
import os
import secrets
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, Optional, Tuple, List
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from models import (
    db, User, UserProgress, LearningSession, CommonError, UserActivity,
    Plan, UsageLog, PaymentRequest, PaymentHistory, Feedback,
    AffiliateProfile, Referral, AffiliateCommission, FamilyMember
)
import config

class UserService:
    """Service for user management"""
    
    def __init__(self):
        pass
    
    def _generate_user_code(self) -> str:
        """Generate unique user code (pair_id)"""
        while True:
            code = str(uuid.uuid4())[:12].upper()
            if not User.query.filter_by(user_code=code).first():
                return code
    
    def _generate_referral_code(self, user_id: int) -> str:
        """Generate unique referral code for agent"""
        user = User.query.get(user_id)
        if not user:
            return None
        
        # Use phone if available, otherwise email
        base_code = user.phone or user.email.split('@')[0]
        code = base_code[:20]
        
        # Make unique
        counter = 1
        while User.query.filter_by(referral_code=code).first():
            code = f"{base_code[:15]}{counter}"
            counter += 1
        
        return code
    
    def register_user(self, email: str = None, phone: str = None, 
                      password: str = None, name: str = None,
                      referred_by: str = None, referral_code: str = None,
                      referred_by_code: str = None) -> Tuple[bool, Dict]:
        """Register new user with fixed user_code"""
        referred_by = referred_by or referral_code or referred_by_code
        email = email.strip().lower() if email else None
        phone = phone.strip() if phone else None
        if not email and not phone:
            return False, {'error': 'Cần email hoặc số điện thoại'}

        if not password or len(password) < 6:
            return False, {'error': 'Mật khẩu cần ít nhất 6 ký tự'}
        
        # Check if exists by email or phone
        if email:
            existing = User.query.filter_by(email=email).first()
            if existing:
                # User already registered - return existing account (not error!)
                return True, {
                    'user': existing.to_dict(), 
                    'message': 'Tài khoản đã tồn tại',
                    'is_existing': True
                }
        
        if phone:
            existing = User.query.filter_by(phone=phone).first()
            if existing:
                return True, {
                    'user': existing.to_dict(), 
                    'message': 'Tài khoản đã tồn tại',
                    'is_existing': True
                }
        
        # Create new user with unique user_code
        user = User(
            email=email,
            phone=phone,
            name=name or 'User',
            user_code=self._generate_user_code(),  # Fixed identifier
            referred_by=referred_by,  # Track who referred this user
            role='user',
            status='trial',
            plan_name='free_trial',
            trial_start=datetime.utcnow(),
            trial_end=datetime.utcnow() + timedelta(days=config.FREE_TRIAL_DAYS),
            subscription_start=None,
            subscription_end=None,
            # Legacy fields
            plan_start=datetime.utcnow(),
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

        # If referred by someone, track the referral
        if referred_by:
            agent = User.query.filter_by(referral_code=referred_by).first()
            if agent:
                referral = Referral(
                    referrer_user_id=agent.id,
                    referred_user_id=user.id,
                    referral_code=referred_by
                )
                db.session.add(referral)
                profile = AffiliateProfile.query.filter_by(user_id=agent.id).first()
                if profile:
                    profile.total_referrals += 1
                db.session.commit()
        
        return True, {
            'user': user.to_dict(), 
            'message': 'Đăng ký thành công',
            'is_existing': False
        }
    
    def login_user(self, email: str = None, phone: str = None, 
                   password: str = None) -> Tuple[bool, Dict]:
        """Login user - returns EXACT same account on subsequent logins"""
        if password is None and phone is not None and email:
            password = phone
            phone = None
        email = email.strip().lower() if email else None
        phone = phone.strip() if phone else None
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
        expiry = user.subscription_end or user.plan_end
        if user.status == 'active' and expiry and now > expiry:
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
        
        if profile_data.get('name'):
            user.name = profile_data.get('name')
        age_value = str(profile_data.get('age') or '').strip()
        user.age_text = age_value or None
        user.age = int(age_value) if age_value.isdigit() else None
        user.job = profile_data.get('job')
        user.meet_foreigners = profile_data.get('meet_foreigners', False)
        user.english_usage = profile_data.get('english_usage')
        user.goal = profile_data.get('goal')
        user.english_level = profile_data.get('level', 'beginner')
        user.learning_path = profile_data.get('learning_path', 'communication')
        user.grade_level = profile_data.get('grade_level')
        if profile_data.get('selected_roadmap_level'):
            user.selected_roadmap_level = profile_data.get('selected_roadmap_level')
        
        db.session.commit()
        
        return True, {'user': user.to_dict(), 'message': 'Cập nhật profile thành công'}
    
    def get_user_progress(self, user_id: int) -> Optional[UserProgress]:
        """Get user progress"""
        return UserProgress.query.filter_by(user_id=user_id).first()

    def is_family_owner(self, user: User) -> bool:
        return bool(user and user.plan_name and 'family' in user.plan_name.lower() and user.status == 'active')

    def get_family_members(self, owner_user_id: int):
        owner = self.get_user(owner_user_id)
        if not self.is_family_owner(owner):
            return False, {'error': 'Chi chu goi Family dang active moi quan ly thanh vien'}
        rows = FamilyMember.query.filter(
            FamilyMember.owner_user_id == owner_user_id,
            FamilyMember.status != 'removed'
        ).order_by(FamilyMember.created_at.desc()).all()
        return True, {
            'owner': owner.to_dict(),
            'capacity': 5,
            'member_slots': 4,
            'used_slots': len(rows),
            'members': [row.to_dict() for row in rows],
        }

    def invite_family_member(self, owner_user_id: int, data: Dict):
        owner = self.get_user(owner_user_id)
        if not self.is_family_owner(owner):
            return False, {'error': 'Tai khoan nay chua phai chu goi Family active'}
        active_count = FamilyMember.query.filter(
            FamilyMember.owner_user_id == owner_user_id,
            FamilyMember.status != 'removed'
        ).count()
        if active_count >= 4:
            return False, {'error': 'Goi Family chi cho toi da 4 thanh vien ngoai chu goi'}

        email = (data.get('email') or '').strip().lower() or None
        phone = (data.get('phone') or '').strip() or None
        name = (data.get('name') or '').strip() or None
        if not email and not phone:
            return False, {'error': 'Can email hoac so dien thoai de moi thanh vien'}

        invite_filters = []
        user_filters = []
        if email:
            invite_filters.append(FamilyMember.email == email)
            user_filters.append(User.email == email)
        if phone:
            invite_filters.append(FamilyMember.phone == phone)
            user_filters.append(User.phone == phone)
        existing_invite = FamilyMember.query.filter(
            FamilyMember.owner_user_id == owner_user_id,
            FamilyMember.status != 'removed',
            or_(*invite_filters)
        ).first()
        if existing_invite:
            return False, {'error': 'Thanh vien nay da nam trong goi Family'}

        member_user = User.query.filter(or_(*user_filters)).first()
        row = FamilyMember(
            owner_user_id=owner_user_id,
            member_user_id=member_user.id if member_user else None,
            name=name or (member_user.name if member_user else ''),
            email=email or (member_user.email if member_user else None),
            phone=phone or (member_user.phone if member_user else None),
            status='active' if member_user else 'invited'
        )
        if member_user:
            member_user.plan_name = owner.plan_name
            member_user.status = 'active'
            member_user.plan_start = owner.plan_start
            member_user.plan_end = owner.plan_end
            member_user.subscription_start = owner.subscription_start
            member_user.subscription_end = owner.subscription_end
            member_user.trial_end = None
        db.session.add(row)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            if member_user:
                raise
            row.member_user_id = 0
            db.session.add(row)
            db.session.commit()
        return True, {'member': row.to_dict(), 'message': 'Da them thanh vien vao goi Family'}

    def remove_family_member(self, owner_user_id: int, member_id: int):
        owner = self.get_user(owner_user_id)
        if not self.is_family_owner(owner):
            return False, {'error': 'Tai khoan nay chua phai chu goi Family active'}
        row = FamilyMember.query.filter_by(id=member_id, owner_user_id=owner_user_id).first()
        if not row or row.status == 'removed':
            return False, {'error': 'Khong tim thay thanh vien'}
        row.status = 'removed'
        row.updated_at = datetime.utcnow()
        db.session.commit()
        return True, {'message': 'Da xoa thanh vien khoi goi Family'}

    def get_all_plans(self):
        return Plan.query.filter_by(enabled=True).all()

    def get_payment_info(self):
        payment_info = config.get_payment_info()
        admin = User.query.filter_by(role='admin').first()
        if admin:
            if not payment_info.get('admin_phone'):
                payment_info['admin_phone'] = admin.phone or ''
            if not payment_info.get('account_name'):
                payment_info['account_name'] = admin.name or payment_info.get('account_name') or ''
        return payment_info

    def get_plan(self, plan_name: str):
        if not plan_name:
            return None
        return Plan.query.filter_by(name=plan_name, enabled=True).first()

    def get_all_users(self):
        return User.query.order_by(User.created_at.desc()).all()

    def search_users(self, query: str = None):
        if not query:
            return self.get_all_users()
        search_term = f"%{query}%"
        return User.query.filter(
            or_(
                User.email.ilike(search_term),
                User.name.ilike(search_term),
                User.phone.ilike(search_term)
            )
        ).order_by(User.created_at.desc()).all()

    def update_user_status(self, user_id: int, status: str):
        user = self.get_user(user_id)
        if not user:
            return False, {'error': 'User không tồn tại'}
        if status not in ['trial', 'active', 'expired', 'banned']:
            return False, {'error': 'Trạng thái không hợp lệ'}
        user.status = status
        db.session.commit()
        return True, {'user': user.to_dict()}

    def extend_trial(self, user_id: int, days: int):
        user = self.get_user(user_id)
        if not user:
            return False, {'error': 'User không tồn tại'}
        if not user.trial_end or user.trial_end < datetime.utcnow():
            user.trial_end = datetime.utcnow() + timedelta(days=days)
        else:
            user.trial_end = user.trial_end + timedelta(days=days)
        user.status = 'trial'
        db.session.commit()
        return True, {'user': user.to_dict()}

    def change_user_plan(self, user_id: int, plan_name: str):
        user = self.get_user(user_id)
        if not user:
            return False, {'error': 'User không tồn tại'}
        plan = self.get_plan(plan_name)
        if not plan:
            return False, {'error': 'Plan không tồn tại'}
        user.plan_name = plan.name
        user.status = 'active'
        user.plan_start = datetime.utcnow()
        user.plan_end = datetime.utcnow() + timedelta(days=30)
        user.subscription_start = user.plan_start
        user.subscription_end = user.plan_end
        user.trial_end = None
        db.session.commit()
        return True, {'user': user.to_dict()}

    def delete_user(self, user_id: int):
        user = self.get_user(user_id)
        if not user:
            return False, {'error': 'User không tồn tại'}
        if user.role == 'admin':
            return False, {'error': 'Khong the xoa admin'}
        UserProgress.query.filter_by(user_id=user_id).delete()
        UsageLog.query.filter_by(user_id=user_id).delete()
        PaymentRequest.query.filter_by(user_id=user_id).delete()
        PaymentHistory.query.filter_by(user_id=user_id).delete()
        Feedback.query.filter_by(user_id=user_id).delete()
        AffiliateProfile.query.filter_by(user_id=user_id).delete()
        Referral.query.filter(
            or_(Referral.referrer_user_id == user_id, Referral.referred_user_id == user_id)
        ).delete(synchronize_session=False)
        AffiliateCommission.query.filter(
            or_(AffiliateCommission.affiliate_user_id == user_id, AffiliateCommission.referred_user_id == user_id)
        ).delete(synchronize_session=False)
        db.session.delete(user)
        db.session.commit()
        return True, {'message': 'User đã bị xóa'}

    def reset_user_password(self, user_id: int, temp_password: str = None):
        user = self.get_user(user_id)
        if not user:
            return False, {'error': 'User không tồn tại'}
        if not temp_password:
            temp_password = os.getenv('DEFAULT_USER_RESET_PASSWORD', 'Temp@1234')
        user.set_password(temp_password)
        db.session.commit()
        return True, {'message': 'Password đã được đặt lại', 'reset_password': temp_password}

    def create_plan(self, plan_data: Dict):
        if Plan.query.filter_by(name=plan_data.get('name')).first():
            return False, {'error': 'Tên gói đã tồn tại'}
        plan = Plan(
            name=plan_data.get('name'),
            title=plan_data.get('title'),
            price=plan_data.get('price', 0),
            currency=plan_data.get('currency', 'VND'),
            chat_limit=plan_data.get('chat_limit', 10),
            lesson_limit=plan_data.get('lesson_limit', 1),
            can_speak=plan_data.get('can_speak', True),
            can_save_history=plan_data.get('can_save_history', True),
            enabled=plan_data.get('enabled', True),
            description=plan_data.get('description', '')
        )
        db.session.add(plan)
        db.session.commit()
        return True, {'plan': plan.to_dict()}

    def update_plan(self, plan_id: int, plan_data: Dict):
        plan = Plan.query.get(plan_id)
        if not plan:
            return False, {'error': 'Plan không tồn tại'}
        plan.title = plan_data.get('title', plan.title)
        plan.price = plan_data.get('price', plan.price)
        plan.currency = plan_data.get('currency', plan.currency)
        plan.chat_limit = plan_data.get('chat_limit', plan.chat_limit)
        plan.lesson_limit = plan_data.get('lesson_limit', plan.lesson_limit)
        plan.can_speak = plan_data.get('can_speak', plan.can_speak)
        plan.can_save_history = plan_data.get('can_save_history', plan.can_save_history)
        plan.enabled = plan_data.get('enabled', plan.enabled)
        plan.description = plan_data.get('description', plan.description)
        db.session.commit()
        return True, {'plan': plan.to_dict()}

    def delete_plan(self, plan_id: int):
        plan = Plan.query.get(plan_id)
        if not plan:
            return False, {'error': 'Plan không tồn tại'}
        db.session.delete(plan)
        db.session.commit()
        return True, {'message': 'Plan đã được xóa'}

    def get_user_usage(self, user_id: int):
        return UsageLog.query.filter_by(user_id=user_id).order_by(UsageLog.date.desc()).limit(30).all()

    def get_or_create_affiliate_profile(self, user_id: int, commission_rate: float = None):
        profile = AffiliateProfile.query.filter_by(user_id=user_id).first()
        if profile:
            return profile
        code = secrets.token_hex(4).upper()
        referral_link = f"{config.AFFILIATE_REFERRAL_LINK_BASE}/?ref={code}"
        profile = AffiliateProfile(
            user_id=user_id,
            affiliate_code=code,
            referral_link=referral_link,
            commission_rate=commission_rate or config.AFFILIATE_COMMISSION_RATE,
            commission_type=getattr(config, 'AFFILIATE_COMMISSION_TYPE', 'percent'),
            commission_percent=commission_rate or config.AFFILIATE_COMMISSION_RATE,
            commission_fixed_amount=getattr(config, 'AFFILIATE_COMMISSION_FIXED_AMOUNT', 0),
            status='approved'
        )
        db.session.add(profile)
        db.session.commit()
        return profile

    def get_affiliate_profile_by_code(self, code: str):
        return AffiliateProfile.query.filter_by(affiliate_code=code).first()

    def create_referral(self, referral_code: str, referred_user_id: int):
        if not referral_code or not referred_user_id:
            return None
        profile = self.get_affiliate_profile_by_code(referral_code)
        if not profile or profile.user_id == referred_user_id:
            return None
        existing = Referral.query.filter_by(referred_user_id=referred_user_id).first()
        if existing:
            return existing
        referral = Referral(
            referrer_user_id=profile.user_id,
            referred_user_id=referred_user_id,
            referral_code=profile.affiliate_code,
            status='pending'
        )
        db.session.add(referral)
        profile.total_referrals += 1
        db.session.commit()
        return referral

    def get_affiliate_summary(self):
        total_affiliates = AffiliateProfile.query.count()
        total_referrals = Referral.query.count()
        pending_commission = db.session.query(db.func.sum(AffiliateCommission.commission_amount)).filter(
            AffiliateCommission.status.in_(['pending', 'approved', 'unpaid'])
        ).scalar() or 0.0
        paid_commission = db.session.query(db.func.sum(AffiliateCommission.commission_amount)).filter_by(status='paid').scalar() or 0.0
        return {
            'total_affiliates': total_affiliates,
            'total_referrals': total_referrals,
            'pending_commission': round(pending_commission, 2),
            'paid_commission': round(paid_commission, 2)
        }

    def get_affiliate_profiles(self):
        return AffiliateProfile.query.order_by(AffiliateProfile.total_referrals.desc()).all()

    def get_affiliate_commissions(self, status: str = None):
        query = AffiliateCommission.query
        if status:
            query = query.filter_by(status=status)
        return query.order_by(AffiliateCommission.created_at.desc()).all()

    def update_affiliate_commission_status(self, commission_id: int, new_status: str):
        if new_status not in ['pending', 'approved', 'unpaid', 'paid', 'cancelled']:
            return False, {'error': 'Trạng thái hoa hồng không hợp lệ'}
        commission = AffiliateCommission.query.get(commission_id)
        if not commission:
            return False, {'error': 'Hoa hồng không tồn tại'}
        commission.status = new_status
        if new_status == 'paid':
            commission.paid_at = datetime.utcnow()
            profile = AffiliateProfile.query.filter_by(user_id=commission.affiliate_user_id).first()
            if profile:
                profile.pending_commission = max(0.0, profile.pending_commission - commission.commission_amount)
                profile.paid_commission += commission.commission_amount
        db.session.commit()
        return True, {'commission': commission.to_dict()}

    def get_user_affiliate(self, user_id: int):
        profile = AffiliateProfile.query.filter_by(user_id=user_id).first()
        referrals = Referral.query.filter_by(referrer_user_id=user_id).order_by(Referral.created_at.desc()).all()
        commissions = AffiliateCommission.query.filter_by(affiliate_user_id=user_id).order_by(AffiliateCommission.created_at.desc()).all()
        return {
            'profile': profile.to_dict() if profile else None,
            'referrals': [ref.to_dict() for ref in referrals],
            'commissions': [comm.to_dict() for comm in commissions]
        }

    def create_commission_for_payment(self, payment: PaymentRequest):
        if not payment or payment.amount <= 0:
            return None
        referral = Referral.query.filter_by(referred_user_id=payment.user_id, status='pending').first()
        if not referral:
            return None
        profile = AffiliateProfile.query.filter_by(user_id=referral.referrer_user_id).first()
        if not profile or profile.status not in ['active', 'approved']:
            return None
        existing = AffiliateCommission.query.filter_by(payment_id=payment.id).first()
        if existing:
            return existing
        commission_type = profile.commission_type or getattr(config, 'AFFILIATE_COMMISSION_TYPE', 'percent')
        commission_rate = profile.commission_percent or profile.commission_rate or config.AFFILIATE_COMMISSION_RATE
        if commission_type == 'fixed':
            commission_amount = float(profile.commission_fixed_amount or getattr(config, 'AFFILIATE_COMMISSION_FIXED_AMOUNT', 0))
        else:
            commission_amount = round(payment.amount * commission_rate / 100.0, 2)
        commission = AffiliateCommission(
            affiliate_user_id=profile.user_id,
            referred_user_id=payment.user_id,
            payment_id=payment.id,
            amount_vnd=payment.amount,
            commission_rate=commission_rate,
            commission_amount=commission_amount,
            status='unpaid'
        )
        db.session.add(commission)
        profile.pending_commission += commission_amount
        profile.total_commission += commission_amount
        referral.first_payment_at = datetime.utcnow()
        referral.status = 'paid'
        db.session.commit()
        return commission

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
        user = self.get_user(user_id)
        if not user:
            return False, {'error': 'User khong ton tai'}

        plan = self.get_plan(plan_name)
        if not plan:
            return False, {'error': 'Plan không tồn tại'}

        reference_code = f"MSE-{user_id}-{plan_name}-{int(datetime.utcnow().timestamp())}"
        transfer_note = f"MSE-{user_id}-{plan_name}"
        payment_info = self.get_payment_info()
        bank_lines = [
            f"Ngan hang: {payment_info.get('bank_name') or 'Chua cau hinh'}",
            f"Chu tai khoan: {payment_info.get('account_name') or 'Chua cau hinh'}",
            f"So tai khoan: {payment_info.get('account_number') or 'Chua cau hinh'}",
            f"So dien thoai admin: {payment_info.get('admin_phone') or 'Chua cau hinh'}",
            f"Noi dung chuyen khoan: {transfer_note}"
        ]
        payment_request = PaymentRequest(
            user_id=user_id,
            plan_name=plan_name,
            amount=plan.price,
            currency=plan.currency,
            status='pending',
            reference_code=reference_code,
            transfer_note=transfer_note,
            bank_info='\n'.join(bank_lines)
        )
        db.session.add(payment_request)
        db.session.commit()

        return True, {
            'payment_request': payment_request.to_dict(),
            'payment_info': payment_info
        }

    def confirm_payment_paid(self, payment_id: int, user_id: int, note: str = ''):
        payment = PaymentRequest.query.get(payment_id)
        if not payment:
            return False, {'error': 'Payment request khong ton tai'}
        if int(payment.user_id) != int(user_id):
            return False, {'error': 'Ban khong co quyen xac nhan yeu cau nay'}
        if payment.status not in ['pending', 'paid_confirmed']:
            return False, {'error': 'Payment request da duoc xu ly'}
        payment.status = 'paid_confirmed'
        payment.customer_confirmed_at = datetime.utcnow()
        payment.customer_note = (note or '')[:255]
        db.session.commit()
        return True, {
            'message': 'Da ghi nhan ban da thanh toan. Admin se kiem tra va mo goi.',
            'payment_request': payment.to_dict()
        }

    def approve_payment(self, payment_id: int):
        payment = PaymentRequest.query.get(payment_id)
        if not payment:
            return False, {'error': 'Payment request không tồn tại'}
        if payment.status not in ['pending', 'paid_confirmed']:
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
        user.plan_end = datetime.utcnow() + timedelta(days=plan.duration_days)  # Use plan's duration_days
        user.subscription_start = user.plan_start
        user.subscription_end = user.plan_end
        user.trial_end = None
        db.session.commit()

        # Create affiliate commission if referred user paid
        commission = self.create_commission_for_payment(payment)

        result = {'message': 'Payment approved and subscription activated', 'payment': payment.to_dict()}
        if commission:
            result['affiliate_commission'] = commission.to_dict()
        return True, result

    def reject_payment(self, payment_id: int):
        payment = PaymentRequest.query.get(payment_id)
        if not payment:
            return False, {'error': 'Payment request không tồn tại'}
        if payment.status not in ['pending', 'paid_confirmed']:
            return False, {'error': 'Payment request đã xử lý'}
        payment.status = 'rejected'
        db.session.commit()
        return True, {'message': 'Payment đã bị từ chối', 'payment': payment.to_dict()}

    def get_payment_requests(self, status='actionable'):
        query = PaymentRequest.query
        if status and status != 'all':
            if status == 'actionable':
                query = query.filter(PaymentRequest.status.in_(['pending', 'paid_confirmed']))
            else:
                query = query.filter_by(status=status)
        return query.order_by(PaymentRequest.customer_confirmed_at.desc().nullslast(), PaymentRequest.created_at.desc()).all()

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
        estimated_cost = UsageLog.query.filter_by(date=today).with_entities(db.func.sum(UsageLog.estimated_cost_vnd)).scalar() or 0.0
        revenue = db.session.query(db.func.sum(PaymentHistory.amount)).scalar() or 0
        return {
            'total_users': total_users,
            'trial_users': trials,
            'active_users': active,
            'expired_users': expired,
            'banned_users': banned,
            'pending_payments': pending_payments,
            'new_feedback': new_feedback,
            'total_chat_today': total_chat_today,
            'estimated_cost_today': round(estimated_cost, 2),
            'estimated_revenue': int(revenue),
            'estimated_profit': int(revenue - estimated_cost)
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
    
    # ============ Agent / Affiliate Management ============
    
    def grant_agent_status(self, user_id: int) -> Tuple[bool, Dict]:
        """Grant agent status to a user - generates referral code"""
        user = self.get_user(user_id)
        if not user:
            return False, {'error': 'User không tồn tại'}
        
        if user.role == 'admin':
            return False, {'error': 'Admin không thể là đại lý'}
        
        # Generate referral code if not exists
        if not user.referral_code:
            user.referral_code = self._generate_referral_code(user_id)
        
        user.role = 'agent'
        user.agent_status = 'pending'
        db.session.commit()
        profile = AffiliateProfile.query.filter_by(user_id=user.id).first()
        if not profile:
            profile = AffiliateProfile(
                user_id=user.id,
                affiliate_code=user.referral_code,
                referral_link=f"{config.AFFILIATE_REFERRAL_LINK_BASE}/?ref={user.referral_code}",
                commission_rate=config.AFFILIATE_COMMISSION_RATE,
                commission_type=getattr(config, 'AFFILIATE_COMMISSION_TYPE', 'percent'),
                commission_percent=config.AFFILIATE_COMMISSION_RATE,
                commission_fixed_amount=getattr(config, 'AFFILIATE_COMMISSION_FIXED_AMOUNT', 0),
                status='pending'
            )
            db.session.add(profile)
        else:
            profile.affiliate_code = user.referral_code
            profile.referral_link = f"{config.AFFILIATE_REFERRAL_LINK_BASE}/?ref={user.referral_code}"
            profile.status = 'pending'
        db.session.commit()
        
        return True, {
            'user': user.to_dict(),
            'message': 'Cấp quyền đại lý thành công',
            'referral_code': user.referral_code
        }
    
    def approve_agent(self, user_id: int) -> Tuple[bool, Dict]:
        """Approve agent status"""
        user = self.get_user(user_id)
        if not user:
            return False, {'error': 'User không tồn tại'}
        
        if user.role != 'agent':
            return False, {'error': 'User không phải đại lý'}
        
        user.agent_status = 'approved'
        profile = AffiliateProfile.query.filter_by(user_id=user.id).first()
        if profile:
            profile.status = 'approved'
        db.session.commit()
        
        return True, {'user': user.to_dict(), 'message': 'Duyệt đại lý thành công'}
    
    def suspend_agent(self, user_id: int) -> Tuple[bool, Dict]:
        """Suspend agent status"""
        user = self.get_user(user_id)
        if not user:
            return False, {'error': 'User không tồn tại'}
        
        user.agent_status = 'suspended'
        profile = AffiliateProfile.query.filter_by(user_id=user.id).first()
        if profile:
            profile.status = 'suspended'
        db.session.commit()
        
        return True, {'user': user.to_dict(), 'message': 'Tạm dừng đại lý thành công'}
    
    def revoke_agent_status(self, user_id: int) -> Tuple[bool, Dict]:
        """Revoke agent status"""
        user = self.get_user(user_id)
        if not user:
            return False, {'error': 'User không tồn tại'}
        
        user.role = 'user'
        user.agent_status = None
        profile = AffiliateProfile.query.filter_by(user_id=user.id).first()
        if profile:
            profile.status = 'suspended'
        user.referral_code = None
        db.session.commit()
        
        return True, {'user': user.to_dict(), 'message': 'Thu hồi quyền đại lý thành công'}
    
    def search_users_advanced(self, query: str = None) -> List[User]:
        """Search users by name, email, phone, user_code, or referral_code"""
        if not query:
            return self.get_all_users()
        
        search_term = f"%{query}%"
        return User.query.filter(
            or_(
                User.email.ilike(search_term),
                User.name.ilike(search_term),
                User.phone.ilike(search_term),
                User.user_code.ilike(search_term),
                User.referral_code.ilike(search_term)
            )
        ).order_by(User.created_at.desc()).all()
    
    def get_agent_stats(self, agent_id: int) -> Dict:
        """Get statistics for an agent"""
        agent = self.get_user(agent_id)
        if not agent or agent.role != 'agent':
            return {}
        
        # Count referred users
        referrals = Referral.query.filter_by(referrer_user_id=agent_id).all()
        total_referred = len(referrals)
        paid_referrals = sum(1 for r in referrals if r.status == 'paid')
        
        # Calculate commission
        commissions = AffiliateCommission.query.filter_by(affiliate_user_id=agent_id).all()
        pending_commission = sum(c.commission_amount for c in commissions if c.status in ['pending', 'approved', 'unpaid'])
        paid_commission = sum(c.commission_amount for c in commissions if c.status == 'paid')
        total_commission = pending_commission + paid_commission
        
        # Calculate revenue
        total_revenue = sum(c.amount_vnd for c in commissions if c.status != 'cancelled')
        
        return {
            'agent_id': agent_id,
            'agent_name': agent.name,
            'agent_code': agent.referral_code,
            'agent_status': agent.agent_status,
            'total_referred': total_referred,
            'paid_referrals': paid_referrals,
            'total_commission': round(total_commission, 0),
            'pending_commission': round(pending_commission, 0),
            'paid_commission': round(paid_commission, 0),
            'total_revenue': int(total_revenue)
        }
    
    def get_all_agents(self, status: str = None) -> List[Dict]:
        """Get all agents with stats"""
        query = User.query.filter_by(role='agent')
        if status:
            query = query.filter_by(agent_status=status)
        
        agents = query.order_by(User.created_at.desc()).all()
        return [self.get_agent_stats(agent.id) for agent in agents]
    
    def get_referral_history(self, agent_id: int) -> List[Dict]:
        """Get referral history for an agent"""
        referrals = Referral.query.filter_by(referrer_user_id=agent_id)\
            .order_by(Referral.created_at.desc()).all()
        
        result = []
        for ref in referrals:
            referred_user = self.get_user(ref.referred_user_id)
            commissions = AffiliateCommission.query.filter_by(
                affiliate_user_id=agent_id,
                referred_user_id=ref.referred_user_id
            ).all()
            
            result.append({
                'referral_id': ref.id,
                'referred_user_name': referred_user.name if referred_user else 'Unknown',
                'referred_user_email': referred_user.email if referred_user else None,
                'referred_user_phone': referred_user.phone if referred_user else None,
                'referral_status': ref.status,
                'referred_date': ref.created_at.isoformat() if ref.created_at else None,
                'first_payment_date': ref.first_payment_at.isoformat() if ref.first_payment_at else None,
                'total_commission': sum(c.commission_amount for c in commissions)
            })
        
        return result
    
    def lock_user(self, user_id: int) -> Tuple[bool, Dict]:
        """Lock/ban user account"""
        user = self.get_user(user_id)
        if not user:
            return False, {'error': 'User không tồn tại'}
        
        user.is_locked = True
        user.status = 'banned'
        db.session.commit()
        
        return True, {'user': user.to_dict(), 'message': 'Khóa tài khoản thành công'}
    
    def unlock_user(self, user_id: int) -> Tuple[bool, Dict]:
        """Unlock user account"""
        user = self.get_user(user_id)
        if not user:
            return False, {'error': 'User không tồn tại'}
        
        user.is_locked = False
        user.status = 'trial'
        db.session.commit()
        
        return True, {'user': user.to_dict(), 'message': 'Mở khóa tài khoản thành công'}
    
    def reset_user_quota(self, user_id: int) -> Tuple[bool, Dict]:
        """Reset user's daily/monthly quota"""
        progress = self.get_user_progress(user_id)
        if not progress:
            return False, {'error': 'Không tìm thấy progress'}
        
        # Reset quota - this would be done by the quota service
        return True, {'message': 'Reset quota thành công'}


# Singleton instance
_user_service = None

def get_user_service():
    global _user_service
    if _user_service is None:
        _user_service = UserService()
    return _user_service
