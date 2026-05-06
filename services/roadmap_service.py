"""Hybrid Learning Roadmap service.

Fixed lesson content lives in seed data; user-specific intelligence is layered
through explicit AI feature calls instead of generating every lesson realtime.
"""

from datetime import datetime, date
from collections import defaultdict

from data.roadmap_seed import ROADMAP_LEVELS, ROADMAP_UNITS, PLACEMENT_QUESTIONS
from models import db, User, UserRoadmapProgress, AIUsageLog


AI_DAILY_LIMITS = {
    "free_trial": 3,
    "free": 3,
    "basic": 30,
    "basic_monthly": 30,
    "basic_six_months": 30,
    "basic_yearly": 30,
    "pro": 120,
    "pro_monthly": 120,
    "pro_six_months": 120,
    "pro_yearly": 120,
    "premium": 300,
    "family": 300,
    "family_monthly": 300,
    "family_six_months": 300,
    "family_yearly": 300,
}


class RoadmapService:
    def __init__(self):
        self.levels = sorted(ROADMAP_LEVELS, key=lambda item: item["order"])
        self.units = ROADMAP_UNITS
        self.units_by_level = defaultdict(list)
        self.lessons = {}
        for unit in self.units:
            self.units_by_level[unit["levelId"]].append(unit)
            for lesson in unit.get("lessons", []):
                self.lessons[lesson["id"]] = lesson
        for level_units in self.units_by_level.values():
            level_units.sort(key=lambda item: item["order"])

    def get_levels(self, user_id=None):
        progress = self.get_progress_map(user_id) if user_id else {}
        result = []
        for level in self.levels:
            lessons = [lesson for unit in self.units_by_level[level["id"]] for lesson in unit.get("lessons", [])]
            completed = sum(1 for lesson in lessons if progress.get(lesson["id"]) == "completed")
            total = len(lessons)
            item = dict(level)
            item["unitCount"] = len(self.units_by_level[level["id"]])
            item["lessonCount"] = total
            item["progressPercent"] = round((completed / total) * 100) if total else 0
            result.append(item)
        return result

    def get_level_detail(self, level_id, user_id=None):
        level = next((item for item in self.levels if item["id"] == level_id), None)
        if not level:
            return None
        progress = self.get_progress_map(user_id) if user_id else {}
        units = []
        for unit in self.units_by_level[level_id]:
            unit_copy = {key: value for key, value in unit.items() if key != "lessons"}
            unit_copy["lessons"] = [
                {**lesson, "status": progress.get(lesson["id"], "not_started")}
                for lesson in unit.get("lessons", [])
            ]
            units.append(unit_copy)
        return {**level, "units": units}

    def get_lesson(self, lesson_id):
        return self.lessons.get(lesson_id)

    def get_progress_map(self, user_id):
        rows = UserRoadmapProgress.query.filter_by(user_id=user_id).all()
        return {row.lesson_id: row.status for row in rows if row.lesson_id}

    def save_progress(self, user_id, lesson_id, status="completed", score=0):
        lesson = self.get_lesson(lesson_id)
        if not lesson:
            return None
        row = UserRoadmapProgress.query.filter_by(user_id=user_id, lesson_id=lesson_id).first()
        if not row:
            row = UserRoadmapProgress(
                user_id=user_id,
                level_id=lesson["levelId"],
                unit_id=lesson["unitId"],
                lesson_id=lesson_id,
            )
            db.session.add(row)
        row.status = status
        row.score = score or row.score or 0
        row.completed_at = datetime.utcnow() if status == "completed" else row.completed_at
        db.session.commit()
        return row

    def get_placement_questions(self):
        return [{key: value for key, value in item.items() if key != "answer"} for item in PLACEMENT_QUESTIONS]

    def score_placement(self, answers):
        correct = 0
        by_id = {item["id"]: item for item in PLACEMENT_QUESTIONS}
        for question_id, answer in (answers or {}).items():
            question = by_id.get(question_id)
            if question and str(answer).strip() == question["answer"]:
                correct += 1
        total = len(PLACEMENT_QUESTIONS)
        percent = round((correct / total) * 100) if total else 0
        if percent < 30:
            level_id = "starter"
        elif percent < 50:
            level_id = "flyer"
        elif percent < 70:
            level_id = "ket"
        elif percent < 85:
            level_id = "pet"
        elif percent < 93:
            level_id = "ielts_foundation"
        else:
            level_id = "ielts_50"
        return {
            "correct": correct,
            "total": total,
            "percent": percent,
            "recommendedLevelId": level_id,
            "recommendedLevel": next((item for item in self.levels if item["id"] == level_id), None),
        }

    def get_ai_limit_status(self, user_id, feature_type):
        user = User.query.get(user_id) if user_id else None
        plan = user.plan_name if user else "free"
        limit = AI_DAILY_LIMITS.get(plan, 3)
        start = datetime.combine(date.today(), datetime.min.time())
        used = AIUsageLog.query.filter(
            AIUsageLog.user_id == user_id,
            AIUsageLog.created_at >= start,
        ).count() if user_id else 0
        return {"allowed": used < limit, "used": used, "limit": limit, "planType": plan, "featureType": feature_type}


_roadmap_service = None


def get_roadmap_service():
    global _roadmap_service
    if _roadmap_service is None:
        _roadmap_service = RoadmapService()
    return _roadmap_service
