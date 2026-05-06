"""Hybrid Learning Roadmap service.

Fixed lesson content lives in seed data; user-specific intelligence is layered
through explicit AI feature calls instead of generating every lesson realtime.
"""

from datetime import datetime, date, timedelta
from collections import defaultdict

from data.roadmap_seed import ROADMAP_LEVELS, ROADMAP_UNITS, PLACEMENT_QUESTIONS
from models import db, User, UserProgress, UserRoadmapProgress, AIUsageLog, LearningSession, FamilyMember


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
        self.lesson_sequence = []
        for level in self.levels:
            for unit in self.units_by_level[level["id"]]:
                for lesson in sorted(unit.get("lessons", []), key=lambda item: item["order"]):
                    self.lesson_sequence.append(lesson["id"])
        self.lesson_index = {lesson_id: idx for idx, lesson_id in enumerate(self.lesson_sequence)}
        self.lesson_sequence_by_level = {}
        for level in self.levels:
            seq = []
            for unit in self.units_by_level[level["id"]]:
                for lesson in sorted(unit.get("lessons", []), key=lambda item: item["order"]):
                    seq.append(lesson["id"])
            self.lesson_sequence_by_level[level["id"]] = seq

    def get_levels(self, user_id=None):
        progress = self.get_progress_map(user_id) if user_id else {}
        user = User.query.get(user_id) if user_id else None
        result = []
        for level in self.levels:
            lessons = [lesson for unit in self.units_by_level[level["id"]] for lesson in unit.get("lessons", [])]
            completed = sum(1 for lesson in lessons if progress.get(lesson["id"]) == "completed")
            total = len(lessons)
            item = dict(level)
            locked = all(self.get_lesson_status(lesson, user, progress) == "locked" for lesson in lessons)
            item["unitCount"] = len(self.units_by_level[level["id"]])
            item["lessonCount"] = total
            item["completedLessons"] = completed
            item["progressPercent"] = round((completed / total) * 100) if total else 0
            item["status"] = "completed" if total and completed == total else ("locked" if locked else "unlocked")
            item["icon"] = self.get_level_icon(level["id"])
            item["isSelected"] = bool(user and user.selected_roadmap_level == level["id"])
            result.append(item)
        return result

    def get_level_detail(self, level_id, user_id=None):
        level = next((item for item in self.levels if item["id"] == level_id), None)
        if not level:
            return None
        progress = self.get_progress_map(user_id) if user_id else {}
        user = User.query.get(user_id) if user_id else None
        units = []
        for unit in self.units_by_level[level_id]:
            unit_copy = {key: value for key, value in unit.items() if key != "lessons"}
            lessons = []
            for lesson in unit.get("lessons", []):
                status = self.get_lesson_status(lesson, user, progress)
                lessons.append({**lesson, "status": status, "icon": self.get_lesson_icon(lesson.get("type"))})
            unit_copy["lessons"] = lessons
            total = len(lessons)
            completed = sum(1 for lesson in lessons if lesson["status"] == "completed")
            unit_copy["completedLessons"] = completed
            unit_copy["lessonCount"] = total
            unit_copy["progressPercent"] = round((completed / total) * 100) if total else 0
            unit_copy["status"] = "completed" if total and completed == total else (
                "locked" if all(lesson["status"] == "locked" for lesson in lessons) else "unlocked"
            )
            units.append(unit_copy)
        return {**level, "icon": self.get_level_icon(level_id), "units": units, "dashboard": self.get_dashboard(user_id)}

    def get_lesson(self, lesson_id):
        return self.lessons.get(lesson_id)

    def get_progress_map(self, user_id):
        rows = UserRoadmapProgress.query.filter_by(user_id=user_id).all()
        return {row.lesson_id: row.status for row in rows if row.lesson_id}

    def is_full_roadmap_plan(self, user):
        plan = (user.plan_name if user else "free").lower()
        if any(key in plan for key in ["pro", "premium", "family", "yearly", "six_months"]):
            return True
        if user and FamilyMember.query.filter(
            FamilyMember.member_user_id == user.id,
            FamilyMember.status == 'active'
        ).first():
            return True
        return False

    def is_free_plan(self, user):
        plan = (user.plan_name if user else "free").lower()
        return plan in {"free", "free_trial", "trial"} or "free" in plan

    def is_first_unit_in_level(self, lesson):
        units = self.units_by_level.get(lesson.get("levelId"), [])
        if not units:
            return False
        first_unit = sorted(units, key=lambda item: item.get("order", 0))[0]
        return lesson.get("unitId") == first_unit.get("id")

    def is_allowed_by_plan(self, lesson, user):
        if not user:
            return self.is_first_unit_in_level(lesson)
        if self.is_full_roadmap_plan(user):
            return True
        if self.is_free_plan(user):
            return self.is_first_unit_in_level(lesson)
        return lesson.get("levelId") in {"starter", "flyer"}

    def get_lesson_status(self, lesson, user, progress):
        lesson_id = lesson["id"]
        if progress.get(lesson_id) == "completed":
            return "completed"
        if not self.is_allowed_by_plan(lesson, user):
            return "locked"
        level_sequence = self.lesson_sequence_by_level.get(lesson.get("levelId"), [])
        idx = level_sequence.index(lesson_id) if lesson_id in level_sequence else 0
        if idx == 0:
            return "unlocked"
        previous_id = level_sequence[idx - 1]
        return "unlocked" if progress.get(previous_id) == "completed" else "locked"

    def get_level_icon(self, level_id):
        return {
            "starter": "seedling",
            "flyer": "paper-plane",
            "ket": "book-open",
            "pet": "comments",
            "ielts_foundation": "pen-nib",
            "ielts_50": "chart-line",
            "ielts_65": "graduation-cap",
            "business": "briefcase",
            "sales": "handshake",
            "cafe": "mug-hot",
            "factory": "industry",
        }.get(level_id, "route")

    def get_lesson_icon(self, lesson_type):
        return {
            "vocabulary": "spell-check",
            "grammar": "diagram-project",
            "listening": "headphones",
            "speaking": "microphone-lines",
            "quiz": "circle-question",
            "review": "rotate-right",
            "integrated": "book-open-reader",
        }.get(lesson_type, "book")

    def get_or_create_user_progress(self, user_id):
        progress = UserProgress.query.filter_by(user_id=user_id).first()
        user = User.query.get(user_id)
        if not progress:
            progress = UserProgress(user_id=user_id)
            db.session.add(progress)
            db.session.flush()
        return progress

    def update_streak(self, progress):
        today = date.today()
        if progress.last_study_date == today:
            return
        if progress.last_study_date == today - timedelta(days=1):
            progress.current_streak = (progress.current_streak or 0) + 1
        else:
            progress.current_streak = 1
        progress.longest_streak = max(progress.longest_streak or 0, progress.current_streak or 0)
        progress.total_days_studied = (progress.total_days_studied or 0) + 1
        progress.last_study_date = today

    def award_badges(self, progress):
        badges = progress.get_badges()
        badge_ids = {badge.get("id") for badge in badges}
        candidates = [
            ("streak_3", "3-Day Streak", (progress.current_streak or 0) >= 3),
            ("streak_7", "7-Day Streak", (progress.current_streak or 0) >= 7),
            ("lesson_10", "10 Lesson Bonus", (progress.completed_lessons or 0) >= 10),
            ("beginner_finisher", "Beginner Finisher", (progress.completed_lessons or 0) >= 6),
        ]
        changed = False
        for badge_id, title, allowed in candidates:
            if allowed and badge_id not in badge_ids:
                badges.append({"id": badge_id, "title": title, "earned_at": datetime.utcnow().isoformat()})
                progress.total_xp = (progress.total_xp or 0) + (100 if badge_id == "lesson_10" else 25)
                changed = True
        if changed:
            progress.set_badges(badges)

    def today_start(self):
        return datetime.combine(date.today(), datetime.min.time())

    def week_start(self):
        today = date.today()
        return datetime.combine(today - timedelta(days=today.weekday()), datetime.min.time())

    def get_today_metrics(self, user_id):
        start = self.today_start()
        completed_today = UserRoadmapProgress.query.filter(
            UserRoadmapProgress.user_id == user_id,
            UserRoadmapProgress.status == "completed",
            UserRoadmapProgress.completed_at >= start,
        ).all()
        speaking_today = LearningSession.query.filter(
            LearningSession.user_id == user_id,
            LearningSession.created_at >= start,
            LearningSession.sentences_practiced > 0,
        ).all()
        daily_xp = sum(row.xp_awarded or 0 for row in completed_today)
        return {
            "lessons": len(completed_today),
            "speakingAttempts": sum(row.sentences_practiced or 0 for row in speaking_today),
            "xp": daily_xp,
        }

    def get_week_metrics(self, user_id):
        start = self.week_start()
        completed_week = UserRoadmapProgress.query.filter(
            UserRoadmapProgress.user_id == user_id,
            UserRoadmapProgress.status == "completed",
            UserRoadmapProgress.completed_at >= start,
        ).all()
        sessions = LearningSession.query.filter(
            LearningSession.user_id == user_id,
            LearningSession.created_at >= start,
        ).all()
        active_days = {session.date.isoformat() for session in sessions if session.date}
        speaking_minutes = sum(max(1, session.sentences_practiced or 0) for session in sessions if session.sentences_practiced)
        return {
            "activeDays": len(active_days),
            "lessons": len(completed_week),
            "speakingMinutes": speaking_minutes,
        }

    def apply_mission_rewards(self, progress):
        today_key = date.today().isoformat()
        week_key = f"{date.today().isocalendar().year}-W{date.today().isocalendar().week}"
        daily_state = progress.get_daily_missions_state()
        weekly_state = progress.get_weekly_challenge_state()
        if daily_state.get("date") != today_key:
            daily_state = {"date": today_key, "claimed": []}
        if weekly_state.get("week") != week_key:
            weekly_state = {"week": week_key, "claimed": []}

        today = self.get_today_metrics(progress.user_id)
        week = self.get_week_metrics(progress.user_id)
        daily_defs = [
            ("daily_lesson", "Complete 1 lesson", today["lessons"], 1, 20),
            ("daily_speaking", "Practice speaking 3 times", today["speakingAttempts"], 3, 30),
            ("daily_xp", "Earn 100 XP", today["xp"], 100, 40),
        ]
        weekly_defs = [
            ("weekly_days", "Study 5 days this week", week["activeDays"], 5, 120),
            ("weekly_lessons", "Complete 10 lessons", week["lessons"], 10, 150),
            ("weekly_speaking", "Practice speaking 20 minutes", week["speakingMinutes"], 20, 180),
        ]

        for mission_id, title, current, target, reward in daily_defs:
            if current >= target and mission_id not in daily_state["claimed"]:
                progress.total_xp = (progress.total_xp or 0) + reward
                daily_state["claimed"].append(mission_id)

        badges = progress.get_badges()
        badge_ids = {badge.get("id") for badge in badges}
        for mission_id, title, current, target, reward in weekly_defs:
            if current >= target and mission_id not in weekly_state["claimed"]:
                progress.total_xp = (progress.total_xp or 0) + reward
                weekly_state["claimed"].append(mission_id)
                badge_id = f"{mission_id}_{week_key}"
                if badge_id not in badge_ids:
                    badges.append({"id": badge_id, "title": title, "earned_at": datetime.utcnow().isoformat()})

        progress.set_daily_missions_state(daily_state)
        progress.set_weekly_challenge_state(weekly_state)
        progress.set_badges(badges)
        return daily_defs, weekly_defs

    def save_progress(self, user_id, lesson_id, status="completed", score=0):
        lesson = self.get_lesson(lesson_id)
        if not lesson:
            return None
        user = User.query.get(user_id)
        progress_map = self.get_progress_map(user_id)
        lesson_status = self.get_lesson_status(lesson, user, progress_map)
        if status == "completed" and lesson_status == "locked":
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
        already_completed = row.status == "completed"
        row.status = status
        row.score = score or row.score or 0
        row.attempts = (row.attempts or 0) + 1
        if status == "completed":
            row.completed_at = row.completed_at or datetime.utcnow()
            if not already_completed:
                xp = 50
                row.xp_awarded = xp
                user_progress = self.get_or_create_user_progress(user_id)
                user_progress.completed_lessons = (user_progress.completed_lessons or 0) + 1
                user_progress.total_xp = (user_progress.total_xp or 0) + xp
                if lesson.get("type") == "speaking":
                    user_progress.speaking_practices = (user_progress.speaking_practices or 0) + 1
                self.update_streak(user_progress)
                self.award_badges(user_progress)
                db.session.add(LearningSession(
                    user_id=user_id,
                    duration_minutes=5,
                    sentences_practiced=1 if lesson.get("type") in {"speaking", "integrated"} else 0,
                ))
                self.apply_mission_rewards(user_progress)
                user_progress.updated_at = datetime.utcnow()
        db.session.commit()
        return row

    def record_speaking_attempt(self, user_id, lesson_id=None, score=0):
        if not user_id:
            return None
        progress = self.get_or_create_user_progress(user_id)
        progress.speaking_practices = (progress.speaking_practices or 0) + 1
        progress.total_sentences_practiced = (progress.total_sentences_practiced or 0) + 1
        if score:
            progress.total_evaluations = (progress.total_evaluations or 0) + 1
            progress.avg_natural_score = ((progress.avg_natural_score or 0) + score) / 2 if progress.total_evaluations > 1 else score
        self.update_streak(progress)
        self.award_badges(progress)
        db.session.add(LearningSession(
            user_id=user_id,
            duration_minutes=1,
            sentences_practiced=1,
            avg_natural_score=score or None,
        ))
        self.apply_mission_rewards(progress)
        progress.updated_at = datetime.utcnow()
        db.session.commit()
        return progress

    def get_continue_lesson(self, user_id):
        user = User.query.get(user_id) if user_id else None
        progress = self.get_progress_map(user_id) if user_id else {}
        selected_level = user.selected_roadmap_level if user and user.selected_roadmap_level else None
        sequence = self.lesson_sequence_by_level.get(selected_level, self.lesson_sequence) if selected_level else self.lesson_sequence
        for lesson_id in sequence:
            lesson = self.lessons[lesson_id]
            if self.get_lesson_status(lesson, user, progress) == "unlocked":
                return lesson
        return self.lessons.get(sequence[-1]) if sequence else None

    def set_selected_level(self, user_id, level_id):
        user = User.query.get(user_id)
        if not user:
            return False, {"error": "User not found"}
        if level_id not in self.units_by_level:
            return False, {"error": "Level not found"}
        first_lesson = next((unit.get("lessons", [None])[0] for unit in self.units_by_level[level_id] if unit.get("lessons")), None)
        if first_lesson and not self.is_allowed_by_plan(first_lesson, user):
            return False, {"error": "Roadmap is not available for this plan"}
        user.selected_roadmap_level = level_id
        db.session.commit()
        return True, {"selected_roadmap_level": level_id}

    def get_dashboard(self, user_id):
        if not user_id:
            return {
                "totalXP": 0, "streakDays": 0, "dailyGoalXP": 50, "dailyProgressXP": 0,
                "badges": [], "completedLessons": 0, "speakingPractices": 0, "pronunciationScoreAvg": 0,
                "currentLevel": "starter", "continueLesson": None, "recentlyStudied": [],
                "dailyMissions": [
                    {"id": "daily_lesson", "title": "Complete 1 lesson", "current": 0, "target": 1, "rewardXP": 20},
                    {"id": "daily_speaking", "title": "Practice speaking 3 times", "current": 0, "target": 3, "rewardXP": 30},
                    {"id": "daily_xp", "title": "Earn 100 XP", "current": 0, "target": 100, "rewardXP": 40},
                ],
                "weeklyChallenge": [],
            }
        progress = UserProgress.query.filter_by(user_id=user_id).first()
        today = self.get_today_metrics(user_id)
        week = self.get_week_metrics(user_id)
        continue_lesson = self.get_continue_lesson(user_id)
        recent_rows = UserRoadmapProgress.query.filter(
            UserRoadmapProgress.user_id == user_id,
            UserRoadmapProgress.completed_at.isnot(None),
        ).order_by(UserRoadmapProgress.completed_at.desc()).limit(5).all()
        daily_missions = [
            {"id": "daily_lesson", "title": "Complete 1 lesson", "current": today["lessons"], "target": 1, "rewardXP": 20},
            {"id": "daily_speaking", "title": "Practice speaking 3 times", "current": today["speakingAttempts"], "target": 3, "rewardXP": 30},
            {"id": "daily_xp", "title": "Earn 100 XP", "current": today["xp"], "target": 100, "rewardXP": 40},
        ]
        weekly_challenge = [
            {"id": "weekly_days", "title": "Study 5 days this week", "current": week["activeDays"], "target": 5, "rewardXP": 120},
            {"id": "weekly_lessons", "title": "Complete 10 lessons", "current": week["lessons"], "target": 10, "rewardXP": 150},
            {"id": "weekly_speaking", "title": "Practice speaking 20 minutes", "current": week["speakingMinutes"], "target": 20, "rewardXP": 180},
        ]
        return {
            "totalXP": progress.total_xp if progress else 0,
            "streakDays": progress.current_streak if progress else 0,
            "dailyGoalXP": progress.daily_goal_xp if progress else 50,
            "dailyProgressXP": today["xp"],
            "badges": progress.get_badges() if progress else [],
            "completedLessons": progress.completed_lessons if progress else 0,
            "speakingPractices": progress.speaking_practices if progress else 0,
            "pronunciationScoreAvg": round(progress.avg_natural_score or 0, 1) if progress else 0,
            "currentLevel": (user.selected_roadmap_level if user else None) or (continue_lesson.get("levelId") if continue_lesson else "starter"),
            "selectedRoadmapLevel": user.selected_roadmap_level if user else None,
            "continueLesson": continue_lesson,
            "recentlyStudied": [
                {"lessonId": row.lesson_id, "title": self.lessons.get(row.lesson_id, {}).get("title", row.lesson_id), "completedAt": row.completed_at.isoformat() if row.completed_at else None}
                for row in recent_rows
            ],
            "dailyMissions": daily_missions,
            "weeklyChallenge": weekly_challenge,
        }

    def admin_learning_analytics(self):
        today_start = datetime.combine(date.today(), datetime.min.time())
        dau = db.session.query(LearningSession.user_id).filter(LearningSession.created_at >= today_start).distinct().count()
        lesson_completed = UserRoadmapProgress.query.filter(
            UserRoadmapProgress.status == "completed",
            UserRoadmapProgress.completed_at >= today_start,
        ).count()
        ai_usage_day = AIUsageLog.query.filter(AIUsageLog.created_at >= today_start).count()
        speaking_usage = UserRoadmapProgress.query.filter(
            UserRoadmapProgress.lesson_id.like("%speaking%"),
            UserRoadmapProgress.completed_at >= today_start,
        ).count()
        progress_rows = UserProgress.query.all()
        avg_xp = round(sum(row.total_xp or 0 for row in progress_rows) / len(progress_rows), 1) if progress_rows else 0
        top_users = sorted(progress_rows, key=lambda row: row.total_xp or 0, reverse=True)[:10]
        return {
            "dau": dau,
            "lessonCompletedToday": lesson_completed,
            "aiUsageToday": ai_usage_day,
            "averageXP": avg_xp,
            "speakingUsageToday": speaking_usage,
            "topActiveUsers": [
                {"userId": row.user_id, "totalXP": row.total_xp or 0, "streakDays": row.current_streak or 0}
                for row in top_users
            ],
        }

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
