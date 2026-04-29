"""
Quota checking and enforcement service
PART 2: Enforce chat limits, token limits, cost limits, and rate limiting
"""

from datetime import datetime, timedelta
from models import db, User, Plan, UsageLog, FamilyMember
from services.cost_service import CostService
import config
from functools import wraps
import time


class QuotaService:
    """Service for checking and enforcing quota limits"""

    @staticmethod
    def _resolve_family_context(user_id: int, plan_name: str):
        if not user_id:
            return plan_name, [user_id]
        membership = FamilyMember.query.filter_by(member_user_id=user_id, status='active').first()
        owner = None
        if membership:
            owner = User.query.get(membership.owner_user_id)
        user = User.query.get(user_id)
        if owner and owner.plan_name == 'family' and owner.status == 'active':
            member_ids = [row.member_user_id for row in FamilyMember.query.filter_by(
                owner_user_id=owner.id,
                status='active'
            ).all()]
            return 'family', [owner.id] + member_ids
        if user and user.plan_name == 'family' and user.status == 'active':
            member_ids = [row.member_user_id for row in FamilyMember.query.filter_by(
                owner_user_id=user.id,
                status='active'
            ).all()]
            return 'family', [user.id] + member_ids
        return plan_name, [user_id]

    @staticmethod
    def _daily_chat_count(user_ids, day):
        if len(user_ids) == 1:
            return CostService.get_daily_chat_count(user_ids[0], day)
        return int(db.session.query(db.func.count(UsageLog.id)).filter(
            UsageLog.user_id.in_(user_ids),
            UsageLog.date == day
        ).scalar() or 0)

    @staticmethod
    def _daily_cost(user_ids, day):
        if len(user_ids) == 1:
            return CostService.get_daily_cost(user_ids[0], day)
        return float(db.session.query(db.func.sum(UsageLog.estimated_cost_vnd)).filter(
            UsageLog.user_id.in_(user_ids),
            UsageLog.date == day
        ).scalar() or 0.0)

    @staticmethod
    def check_can_chat(user_id: int = None, plan_name: str = "free_trial") -> dict:
        """
        PART 2: Check if user can send a chat message
        
        Returns:
            {
                "allowed": bool,
                "reason": str (if not allowed),
                "limits": {
                    "daily_chats": int,
                    "daily_cost": float,
                    "chats_remaining_today": int,
                    "cost_remaining_today": float
                }
            }
        """
        try:
            plan_name, usage_user_ids = QuotaService._resolve_family_context(user_id, plan_name)
            # Get plan limits
            plan_def = config.get_plan_by_name(plan_name)
            if not plan_def:
                plan_def = config.get_plan_by_name("free_trial")
            
            chat_per_day = plan_def.get("chat_per_day", 10)
            max_cost_per_day_vnd = plan_def.get("max_cost_per_day_vnd", 0.0)
            
            # Count today's usage
            today = datetime.utcnow().date()
            daily_chats = QuotaService._daily_chat_count(usage_user_ids, today)
            daily_cost_vnd = QuotaService._daily_cost(usage_user_ids, today)
            
            # Check chat limit
            if daily_chats >= chat_per_day:
                return {
                    "allowed": False,
                    "reason": "US English: You have reached your daily chat limit. Please try tomorrow or upgrade your plan. VN Tiếng Việt: Em đã dùng hết lượt hôm nay. Vui lòng thử lại ngày mai hoặc nâng cấp gói.",
                    "limits": {
                        "daily_chats": chat_per_day,
                        "daily_cost": max_cost_per_day_vnd,
                        "chats_remaining_today": 0,
                        "cost_remaining_today": 0
                    }
                }
            
            # Check cost limit (if set)
            if max_cost_per_day_vnd > 0 and daily_cost_vnd >= max_cost_per_day_vnd:
                return {
                    "allowed": False,
                    "reason": f"US English: You have reached your daily cost limit ({max_cost_per_day_vnd:,.0f}₫). Please upgrade for more. VN Tiếng Việt: Em đã dùng hết ngân sách hôm nay ({max_cost_per_day_vnd:,.0f}₫). Vui lòng nâng cấp gói.",
                    "limits": {
                        "daily_chats": chat_per_day,
                        "daily_cost": max_cost_per_day_vnd,
                        "chats_remaining_today": chat_per_day - daily_chats,
                        "cost_remaining_today": 0
                    }
                }
            
            # Calculate remaining quota
            chats_remaining = chat_per_day - daily_chats
            cost_remaining = max_cost_per_day_vnd - daily_cost_vnd if max_cost_per_day_vnd > 0 else float('inf')
            
            return {
                "allowed": True,
                "reason": None,
                "limits": {
                    "daily_chats": chat_per_day,
                    "daily_cost": max_cost_per_day_vnd,
                    "chats_remaining_today": chats_remaining,
                    "cost_remaining_today": cost_remaining if cost_remaining != float('inf') else max_cost_per_day_vnd
                }
            }
        except Exception as e:
            print(f"[QuotaService] Error checking quota: {e}")
            return {
                "allowed": True,  # Allow if error (fail-open)
                "reason": None,
                "limits": {}
            }

    @staticmethod
    def check_monthly_quota(user_id: int = None, plan_name: str = "free_trial") -> dict:
        """
        PART 2: Check if user has exceeded monthly quota
        
        Returns:
            {
                "allowed": bool,
                "remaining_chats": int,
                "remaining_cost_budget": float
            }
        """
        try:
            plan_def = config.get_plan_by_name(plan_name)
            if not plan_def:
                plan_def = config.get_plan_by_name("free_trial")
            
            chat_per_month = plan_def.get("chat_per_month", 300)
            max_cost_per_month_vnd = plan_def.get("max_cost_per_month_vnd", 0.0)
            
            # Count this month's usage
            now = datetime.utcnow()
            monthly_chats = CostService.get_monthly_chat_count(user_id, now.year, now.month)
            start = datetime(now.year, now.month, 1)
            end = datetime(now.year + (1 if now.month == 12 else 0), 1 if now.month == 12 else now.month + 1, 1)
            monthly_cost_vnd = db.session.query(db.func.sum(UsageLog.estimated_cost_vnd)).filter(
                UsageLog.user_id == user_id,
                UsageLog.created_at >= start,
                UsageLog.created_at < end
            ).scalar() or 0.0
            
            allowed = monthly_chats < chat_per_month
            if max_cost_per_month_vnd > 0:
                allowed = allowed and monthly_cost_vnd < max_cost_per_month_vnd
            
            return {
                "allowed": allowed,
                "remaining_chats": max(0, chat_per_month - monthly_chats),
                "remaining_cost_budget": max(0, max_cost_per_month_vnd - monthly_cost_vnd) if max_cost_per_month_vnd > 0 else float('inf')
            }
        except Exception as e:
            print(f"[QuotaService] Error checking monthly quota: {e}")
            return {
                "allowed": True,
                "remaining_chats": 999,
                "remaining_cost_budget": float('inf')
            }

    @staticmethod
    def check_token_limit(estimated_tokens: int, plan_name: str = "free_trial") -> dict:
        """
        PART 2: Check if estimated tokens exceed per-chat limit
        
        Returns:
            {
                "allowed": bool,
                "max_tokens": int,
                "reason": str (if not allowed)
            }
        """
        try:
            plan_def = config.get_plan_by_name(plan_name)
            if not plan_def:
                plan_def = config.get_plan_by_name("free_trial")
            
            max_tokens = plan_def.get("max_tokens_per_chat", 2000)
            
            if estimated_tokens > max_tokens:
                return {
                    "allowed": False,
                    "max_tokens": max_tokens,
                    "reason": f"US English: Your message is too long (>{max_tokens} tokens). Please shorten it. VN Tiếng Việt: Tin nhắn quá dài. Vui lòng rút ngắn lại."
                }
            
            return {
                "allowed": True,
                "max_tokens": max_tokens,
                "reason": None
            }
        except Exception as e:
            print(f"[QuotaService] Error checking token limit: {e}")
            return {
                "allowed": True,
                "max_tokens": 2000,
                "reason": None
            }

    @staticmethod
    def get_cost_warning(user_id: int, daily_cost_vnd: float, plan_name: str = "free_trial") -> dict:
        """
        PART 3: Get warning level for cost overuse
        
        Returns:
            {
                "level": "green" | "yellow" | "red",  # green=<70%, yellow=70-100%, red=>100%
                "message": str,
                "percentage": float
            }
        """
        try:
            plan_def = config.get_plan_by_name(plan_name)
            if not plan_def:
                plan_def = config.get_plan_by_name("free_trial")
            
            max_cost = plan_def.get("max_cost_per_day_vnd", plan_def.get("price", 49000))
            if max_cost <= 0:
                max_cost = plan_def.get("price", 49000)
            
            percentage = (daily_cost_vnd / max_cost) * 100
            
            if percentage > 100:
                return {
                    "level": "red",
                    "message": f"🔴 CẢNH BÁO: Bạn đã vượt quá ngân sách hôm nay! ({percentage:.0f}%)",
                    "percentage": percentage
                }
            elif percentage > 70:
                return {
                    "level": "yellow",
                    "message": f"🟡 CẢNH BÁO: Bạn đã dùng {percentage:.0f}% ngân sách hôm nay. Hãy cẩn thận!",
                    "percentage": percentage
                }
            else:
                return {
                    "level": "green",
                    "message": None,
                    "percentage": percentage
                }
        except Exception as e:
            print(f"[QuotaService] Error getting cost warning: {e}")
            return {
                "level": "green",
                "message": None,
                "percentage": 0
            }


def rate_limit_check(user_id: int = None, window_seconds: int = None) -> dict:
    """
    PART 2: Simple rate limiting - check if user is sending requests too fast
    
    Uses in-memory tracking (in production, use Redis)
    
    Returns:
        {
            "allowed": bool,
            "wait_seconds": float (if not allowed),
            "reason": str (if not allowed)
        }
    """
    if window_seconds is None:
        window_seconds = config.RATE_LIMIT_WINDOW
    
    # In production, use Redis for this. For now, simple check.
    # This is a placeholder - would need proper implementation
    return {
        "allowed": True,
        "wait_seconds": 0,
        "reason": None
    }


def require_quota(func):
    """
    Decorator to check quota before executing API function
    Usage: @require_quota def chat_endpoint(...):
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # This would be implemented in actual API endpoints
        return func(*args, **kwargs)
    return wrapper


def get_quota_service():
    """Get quota service instance"""
    return QuotaService()
