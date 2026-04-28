"""
Cost tracking and calculation service
PART 1 & 3: AI cost tracking, quota enforcement, and profit/loss analytics
"""

from datetime import datetime, timedelta
from models import db, UsageLog, CostAnalytics, User, Plan
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
        model_config = config.MODEL_COSTS.get(model, config.MODEL_COSTS["gpt-4o-mini"])
        
        input_cost_usd = (input_tokens / 1000) * model_config.get("input_per_1k_tokens", 0.00015)
        output_cost_usd = (output_tokens / 1000) * model_config.get("output_per_1k_tokens", 0.0006)
        
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


def get_cost_service():
    """Get cost service instance"""
    return CostService()
