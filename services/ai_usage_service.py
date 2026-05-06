"""AI usage logging and cost summary service."""

from datetime import datetime, date

from models import db, AIUsageLog, User


class AIUsageService:
    def log_usage(self, user_id=None, feature_type="unknown", token_used=0, estimated_cost=0.0, plan_type=None):
        if not plan_type and user_id:
            user = User.query.get(user_id)
            plan_type = user.plan_name if user else "free"
        log = AIUsageLog(
            user_id=user_id,
            feature_type=feature_type,
            token_used=int(token_used or 0),
            estimated_cost=float(estimated_cost or 0.0),
            plan_type=plan_type or "free",
        )
        db.session.add(log)
        db.session.commit()
        return log

    def today_summary(self):
        start = datetime.combine(date.today(), datetime.min.time())
        rows = AIUsageLog.query.filter(AIUsageLog.created_at >= start).all()
        by_user = {}
        feature_counts = {}
        total_cost = 0.0
        total_tokens = 0
        for row in rows:
            total_cost += row.estimated_cost or 0.0
            total_tokens += row.token_used or 0
            feature_counts[row.feature_type] = feature_counts.get(row.feature_type, 0) + 1
            item = by_user.setdefault(row.user_id or "guest", {
                "userId": row.user_id,
                "count": 0,
                "estimatedCost": 0.0,
                "tokenUsed": 0,
                "planType": row.plan_type,
                "warning": False,
            })
            item["count"] += 1
            item["estimatedCost"] += row.estimated_cost or 0.0
            item["tokenUsed"] += row.token_used or 0
            item["warning"] = item["count"] > 30 or item["estimatedCost"] > 50000
        heavy_users = sorted(by_user.values(), key=lambda item: (item["count"], item["estimatedCost"]), reverse=True)
        return {
            "totalCallsToday": len(rows),
            "estimatedCostToday": round(total_cost, 2),
            "tokenUsedToday": total_tokens,
            "featureCounts": feature_counts,
            "users": heavy_users[:50],
            "warnings": [item for item in heavy_users if item["warning"]],
        }


_ai_usage_service = None


def get_ai_usage_service():
    global _ai_usage_service
    if _ai_usage_service is None:
        _ai_usage_service = AIUsageService()
    return _ai_usage_service
