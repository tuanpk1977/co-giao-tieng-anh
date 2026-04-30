"""
Cost tracking and calculation service
PART 1 & 3: AI cost tracking, quota enforcement, and profit/loss analytics
"""

from datetime import datetime, timedelta
from models import db, UsageLog, CostAnalytics, User, Plan, UserUsageCost, AdminAlert
import config
from sqlalchemy import func


class CostService:
    """Service for calculating and tracking AI costs"""

    @staticmethod
    def calculate_cost_from_tokens(input_tokens: int, output_tokens: int, model: str = "gpt-4o-mini"):
        """
        PART 1: Calculate cost in USD from tokens
        
        Args:
            input_tokens: Number of input tokens used
            output_tokens: Number of output tokens used
            model: AI model name
        
        Returns:
            Tuple of (cost_usd, cost_vnd)
        """
        model_config = config.AI_COST_CONFIG.get(model, config.AI_COST_CONFIG["gpt-4o-mini"])

        input_cost_usd = (input_tokens / 1_000_000) * model_config.get("input_per_1m_usd", 0.15)
        output_cost_usd = (output_tokens / 1_000_000) * model_config.get("output_per_1m_usd", 0.60)
        
        cost_usd = input_cost_usd + output_cost_usd
        cost_vnd = cost_usd * config.USD_TO_VND
        
        return round(cost_usd, 6), round(cost_vnd, 0)

    @staticmethod
    def estimate_tokens_from_text(text: str) -> int:
        """
        Estimate token count from text if API doesn't provide actual count
        Generally: 1 token ≈ 4 characters for English
        """
        return max(1, len(text) // 4)

    @staticmethod
    def _month_key(day=None) -> str:
        day = day or datetime.utcnow().date()
        return day.strftime("%Y-%m")

    @staticmethod
    def _month_range(month_key: str = None):
        if not month_key:
            month_key = CostService._month_key()
        year, month = [int(part) for part in month_key.split('-')]
        start = datetime(year, month, 1)
        end = datetime(year + (1 if month == 12 else 0), 1 if month == 12 else month + 1, 1)
        return start, end

    @staticmethod
    def calculate_user_revenue(user: User, month_key: str = None, through_day=None) -> float:
        if not user or user.status != 'active' or user.plan_name == 'free_trial':
            return 0.0
        plan = Plan.query.filter_by(name=user.plan_name).first()
        if not plan or not plan.price:
            return 0.0

        month_start, month_end = CostService._month_range(month_key)
        through_dt = datetime.combine(through_day or datetime.utcnow().date(), datetime.min.time()) + timedelta(days=1)
        period_end = min(month_end, through_dt)
        sub_start = user.subscription_start or user.plan_start or month_start
        sub_end = user.subscription_end or user.plan_end or period_end
        active_start = max(month_start, sub_start)
        active_end = min(period_end, sub_end)
        active_days = max(0, (active_end - active_start).days)
        duration_days = max(1, int(getattr(plan, 'duration_days', None) or 30))
        return round((plan.price / duration_days) * active_days, 0)

    @staticmethod
    def calculate_risk(revenue_vnd: float, cost_vnd: float, user: User = None) -> str:
        revenue_vnd = float(revenue_vnd or 0)
        cost_vnd = float(cost_vnd or 0)
        if user and (user.status == 'trial' or user.plan_name == 'free_trial'):
            if cost_vnd > config.TRIAL_HARD_LIMIT_VND:
                return 'loss'
            if cost_vnd > config.TRIAL_COST_LIMIT_VND:
                return 'danger'
            return 'safe'
        if revenue_vnd <= 0:
            return 'loss' if cost_vnd > 0 else 'safe'
        ratio = cost_vnd / revenue_vnd
        if ratio >= config.USER_LOSS_COST_RATIO:
            return 'loss'
        if ratio > config.USER_DANGER_COST_RATIO:
            return 'danger'
        if ratio > config.USER_WARNING_COST_RATIO:
            return 'warning'
        return 'safe'

    @staticmethod
    def _margin(revenue_vnd: float, gross_profit_vnd: float, cost_vnd: float) -> float:
        if revenue_vnd and revenue_vnd > 0:
            return round((gross_profit_vnd / revenue_vnd) * 100, 2)
        return -100.0 if cost_vnd > 0 else 0.0

    @staticmethod
    def create_admin_alert(user_id: int, alert_type: str, message: str):
        today = datetime.utcnow().date()
        existing = AdminAlert.query.filter(
            AdminAlert.user_id == user_id,
            AdminAlert.type == alert_type,
            func.date(AdminAlert.created_at) == today
        ).first()
        if existing:
            return existing
        alert = AdminAlert(user_id=user_id, type=alert_type, message=message, is_read=False)
        db.session.add(alert)
        return alert

    @staticmethod
    def _alert_type_for_risk(user: User, risk_level: str) -> str:
        if user and (user.status == 'trial' or user.plan_name == 'free_trial') and risk_level in ['danger', 'loss']:
            return 'trial_abuse'
        return {
            'warning': 'cost_warning',
            'danger': 'cost_danger',
            'loss': 'user_loss'
        }.get(risk_level)

    @staticmethod
    def _upsert_user_usage_cost(user_id: int, day=None):
        day = day or datetime.utcnow().date()
        month_key = CostService._month_key(day)
        user = User.query.get(user_id)
        if not user:
            return None
        start, end = CostService._month_range(month_key)
        usage_logs = UsageLog.query.filter(
            UsageLog.user_id == user_id,
            UsageLog.created_at >= start,
            UsageLog.created_at < end
        ).all()

        revenue_vnd = CostService.calculate_user_revenue(user, month_key, through_day=day)
        input_tokens = sum(log.input_tokens or 0 for log in usage_logs)
        output_tokens = sum(log.output_tokens or 0 for log in usage_logs)
        cost_usd = sum(log.estimated_cost_usd or 0 for log in usage_logs)
        cost_vnd = sum(log.estimated_cost_vnd or 0 for log in usage_logs)
        gross_profit = revenue_vnd - cost_vnd
        old = UserUsageCost.query.filter_by(user_id=user_id, date=day, month=month_key).first()
        old_risk = old.risk_level if old else 'safe'
        risk = CostService.calculate_risk(revenue_vnd, cost_vnd, user)

        record = old or UserUsageCost(user_id=user_id, date=day, month=month_key)
        record.chat_count = sum(log.chat_count or 0 for log in usage_logs)
        record.lesson_count = sum(log.lesson_count or 0 for log in usage_logs)
        record.speaking_count = sum(log.speaking_count or 0 for log in usage_logs)
        record.input_tokens = input_tokens
        record.output_tokens = output_tokens
        record.total_tokens = input_tokens + output_tokens
        record.estimated_ai_cost_usd = round(cost_usd, 6)
        record.estimated_ai_cost_vnd = round(cost_vnd, 0)
        record.revenue_vnd = round(revenue_vnd, 0)
        record.gross_profit_vnd = round(gross_profit, 0)
        record.profit_margin_percent = CostService._margin(revenue_vnd, gross_profit, cost_vnd)
        record.risk_level = risk
        record.updated_at = datetime.utcnow()
        db.session.add(record)

        if risk in ['warning', 'danger', 'loss'] and risk != old_risk:
            alert_type = CostService._alert_type_for_risk(user, risk)
            if alert_type:
                CostService.create_admin_alert(
                    user_id,
                    alert_type,
                    f"User #{user_id} risk {risk}: revenue {revenue_vnd:,.0f} VND, AI cost {cost_vnd:,.0f} VND"
                )
        return record

    @staticmethod
    def _latest_month_records(month_key: str = None):
        month_key = month_key or CostService._month_key()
        for user in User.query.filter(User.role != 'admin').all():
            CostService._upsert_user_usage_cost(user.id, datetime.utcnow().date())
        db.session.commit()

        rows = db.session.query(
            UserUsageCost.user_id,
            func.max(UserUsageCost.date).label('max_date')
        ).filter_by(month=month_key).group_by(UserUsageCost.user_id).subquery()

        return UserUsageCost.query.join(
            rows,
            (UserUsageCost.user_id == rows.c.user_id) & (UserUsageCost.date == rows.c.max_date)
        ).filter(UserUsageCost.month == month_key)

    @staticmethod
    def get_user_current_cost(user_id: int):
        day = datetime.utcnow().date()
        record = CostService._upsert_user_usage_cost(user_id, day)
        db.session.commit()
        return record

    @staticmethod
    def log_usage(user_id: int, input_tokens: int = 0, output_tokens: int = 0, 
                  model: str = "gpt-4o-mini", message_count: int = 1, ai_provider: str = "openai"):
        """
        PART 1: Log AI usage and cost for a user
        
        Creates a new UsageLog entry with calculated costs
        """
        try:
            # Calculate costs
            if input_tokens == 0 and output_tokens == 0:
                # No token info provided - estimate from placeholder
                input_tokens = message_count * 100
                output_tokens = message_count * 150
            
            cost_usd, cost_vnd = CostService.calculate_cost_from_tokens(
                input_tokens, output_tokens, model
            )
            
            usage_log = UsageLog(
                user_id=user_id,
                message_count=message_count,
                chat_count=message_count,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                estimated_tokens=input_tokens + output_tokens,
                model=model,
                estimated_cost=cost_vnd,
                estimated_cost_usd=cost_usd,
                estimated_cost_vnd=cost_vnd,
                ai_provider=ai_provider,
                date=datetime.utcnow().date(),
                created_at=datetime.utcnow()
            )
            
            db.session.add(usage_log)
            CostService._upsert_user_usage_cost(user_id, usage_log.date)
            db.session.commit()
            
            return usage_log.to_dict()
        except Exception as e:
            print(f"[CostService] Error logging usage: {e}")
            return None

    @staticmethod
    def get_daily_cost(user_id: int, date=None) -> float:
        """
        Get total estimated AI cost for a user on a specific date
        """
        if date is None:
            date = datetime.utcnow().date()
        
        try:
            total = db.session.query(func.sum(UsageLog.estimated_cost_vnd)).filter(
                UsageLog.user_id == user_id,
                UsageLog.date == date
            ).scalar() or 0.0
            
            return round(total, 0)
        except Exception as e:
            print(f"[CostService] Error getting daily cost: {e}")
            return 0.0

    @staticmethod
    def get_monthly_cost(user_id: int, year: int = None, month: int = None) -> float:
        """
        Get total estimated AI cost for a user in a specific month
        """
        if year is None:
            year = datetime.utcnow().year
        if month is None:
            month = datetime.utcnow().month
        
        try:
            start = datetime(year, month, 1)
            end = datetime(year + (1 if month == 12 else 0), 1 if month == 12 else month + 1, 1)
            total = db.session.query(func.sum(UsageLog.estimated_cost_vnd)).filter(
                UsageLog.user_id == user_id,
                UsageLog.created_at >= start,
                UsageLog.created_at < end
            ).scalar() or 0.0
            
            return round(total, 0)
        except Exception as e:
            print(f"[CostService] Error getting monthly cost: {e}")
            return 0.0

    @staticmethod
    def get_daily_chat_count(user_id: int, date=None) -> int:
        """
        Get number of chats for a user on a specific date
        """
        if date is None:
            date = datetime.utcnow().date()
        
        try:
            count = db.session.query(func.count(UsageLog.id)).filter(
                UsageLog.user_id == user_id,
                UsageLog.date == date
            ).scalar() or 0
            
            return int(count)
        except Exception as e:
            print(f"[CostService] Error getting daily chat count: {e}")
            return 0

    @staticmethod
    def get_monthly_chat_count(user_id: int, year: int = None, month: int = None) -> int:
        """
        Get number of chats for a user in a specific month
        """
        if year is None:
            year = datetime.utcnow().year
        if month is None:
            month = datetime.utcnow().month
        
        try:
            start = datetime(year, month, 1)
            end = datetime(year + (1 if month == 12 else 0), 1 if month == 12 else month + 1, 1)
            count = db.session.query(func.count(UsageLog.id)).filter(
                UsageLog.user_id == user_id,
                UsageLog.created_at >= start,
                UsageLog.created_at < end
            ).scalar() or 0
            
            return int(count)
        except Exception as e:
            print(f"[CostService] Error getting monthly chat count: {e}")
            return 0

    @staticmethod
    def update_cost_analytics(user_id: int = None, date=None):
        """
        PART 3: Update CostAnalytics table for admin dashboard
        Calculate profit/loss for each user based on costs vs. revenue
        """
        if date is None:
            date = datetime.utcnow().date()
        
        try:
            if user_id:
                users = [User.query.get(user_id)]
            else:
                users = User.query.filter(User.role != 'admin').all()
            
            for user in users:
                if not user:
                    continue
                
                # Get daily usage
                usage_logs = UsageLog.query.filter(
                    UsageLog.user_id == user.id,
                    UsageLog.date == date
                ).all()
                
                ai_cost_vnd = sum(log.estimated_cost_vnd for log in usage_logs)
                ai_cost_usd = sum(log.estimated_cost_usd for log in usage_logs)
                chat_count = len(usage_logs)
                total_tokens = sum(log.estimated_tokens for log in usage_logs)
                
                # Get revenue (if user has paid subscription)
                revenue_vnd = 0.0
                if user.status == 'active' and user.plan_name != 'free_trial':
                    plan = Plan.query.filter_by(name=user.plan_name).first()
                    if plan:
                        # Prorate revenue by number of days in month
                        days_in_month = 30  # Simplified
                        revenue_vnd = plan.price / days_in_month
                
                # Calculate profit/loss
                profit_loss_vnd = revenue_vnd - ai_cost_vnd
                is_profitable = profit_loss_vnd >= 0
                
                # Update or create CostAnalytics entry
                analytics = CostAnalytics.query.filter(
                    CostAnalytics.user_id == user.id,
                    CostAnalytics.date == date
                ).first()
                
                if not analytics:
                    analytics = CostAnalytics(user_id=user.id, date=date)
                
                analytics.ai_cost_vnd = round(ai_cost_vnd, 0)
                analytics.ai_cost_usd = round(ai_cost_usd, 6)
                analytics.revenue_vnd = round(revenue_vnd, 0)
                analytics.chat_count = chat_count
                analytics.total_tokens = total_tokens
                analytics.is_profitable = is_profitable
                analytics.profit_loss_vnd = round(profit_loss_vnd, 0)
                analytics.updated_at = datetime.utcnow()
                
                db.session.add(analytics)
            
            db.session.commit()
            return True
        except Exception as e:
            print(f"[CostService] Error updating cost analytics: {e}")
            db.session.rollback()
            return False

    @staticmethod
    def check_chat_cost_policy(user_id: int):
        user = User.query.get(user_id)
        if not user:
            return {'allowed': True, 'risk_level': 'safe', 'short_answer': False}
        record = CostService.get_user_current_cost(user_id)
        cost_vnd = record.estimated_ai_cost_vnd if record else 0
        risk = record.risk_level if record else 'safe'
        if user.status == 'trial' or user.plan_name == 'free_trial':
            if cost_vnd >= config.TRIAL_HARD_LIMIT_VND:
                return {'allowed': False, 'risk_level': 'loss', 'short_answer': False, 'reason': 'trial_hard_limit'}
        if risk == 'loss':
            return {'allowed': False, 'risk_level': risk, 'short_answer': False, 'reason': 'loss'}
        return {'allowed': True, 'risk_level': risk, 'short_answer': risk == 'danger'}

    @staticmethod
    def get_cost_summary(month_key: str = None):
        month_key = month_key or CostService._month_key()
        records = CostService._latest_month_records(month_key).all()
        total_revenue = sum(r.revenue_vnd or 0 for r in records)
        total_cost = sum(r.estimated_ai_cost_vnd or 0 for r in records)
        return {
            'month': month_key,
            'total_revenue': round(total_revenue, 0),
            'total_ai_cost': round(total_cost, 0),
            'total_profit': round(total_revenue - total_cost, 0),
            'total_users_loss': sum(1 for r in records if r.risk_level == 'loss'),
            'total_users_danger': sum(1 for r in records if r.risk_level == 'danger'),
            'unread_alerts': AdminAlert.query.filter_by(is_read=False).count()
        }

    @staticmethod
    def get_cost_users(risk_filter: str = None, month_key: str = None):
        month_key = month_key or CostService._month_key()
        query = CostService._latest_month_records(month_key)
        if risk_filter and risk_filter not in ['all', 'profit']:
            query = query.filter_by(risk_level=risk_filter)
        records = query.order_by(UserUsageCost.risk_level.desc(), UserUsageCost.estimated_ai_cost_vnd.desc()).all()
        result = []
        for record in records:
            if risk_filter == 'profit' and (record.gross_profit_vnd or 0) < 0:
                continue
            user = record.user
            result.append({
                **record.to_dict(),
                'user_name': user.name if user else '',
                'email': user.email if user else '',
                'phone': user.phone if user else '',
                'plan_name': user.plan_name if user else '',
                'status': user.status if user else ''
            })
        return result

    @staticmethod
    def get_user_cost_detail(user_id: int):
        records = UserUsageCost.query.filter_by(user_id=user_id).order_by(UserUsageCost.date.desc()).limit(90).all()
        logs = UsageLog.query.filter_by(user_id=user_id).order_by(UsageLog.created_at.desc()).limit(100).all()
        return {
            'daily_costs': [r.to_dict() for r in records],
            'usage_logs': [log.to_dict() for log in logs]
        }

    @staticmethod
    def reset_user_cost(user_id: int):
        month_key = CostService._month_key()
        start, end = CostService._month_range(month_key)
        UsageLog.query.filter(
            UsageLog.user_id == user_id,
            UsageLog.created_at >= start,
            UsageLog.created_at < end
        ).delete(synchronize_session=False)
        UserUsageCost.query.filter_by(user_id=user_id, month=month_key).delete()
        db.session.commit()
        return True


def get_cost_service():
    """Get cost service instance"""
    return CostService()
