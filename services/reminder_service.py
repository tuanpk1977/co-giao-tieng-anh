"""
Learning reminder service - sends email reminders to inactive users
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import List, Dict
from models import db, ReminderLog, User, UserProgress
from services.user_service import get_user_service
import os

class ReminderService:
    """Service for sending learning reminders"""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_pass = os.getenv('SMTP_PASS', '')
        self.from_email = os.getenv('FROM_EMAIL', 'ms.smile.english@gmail.com')
    
    def send_reminder_email(self, user: User, reminder_type: str) -> bool:
        """Send reminder email to user"""
        if not user.email:
            return False
        
        # Get message content
        subject, body = self._get_reminder_content(user, reminder_type)
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = user.email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html', 'utf-8'))
            
            # Send email (or just log for demo)
            if self.smtp_user and self.smtp_pass:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.send_message(msg)
                server.quit()
            else:
                # Demo mode - just log
                print(f"\n{'='*60}")
                print(f"📧 REMINDER EMAIL (Demo Mode)")
                print(f"{'='*60}")
                print(f"To: {user.email}")
                print(f"Subject: {subject}")
                print(f"\n{body}")
                print(f"{'='*60}\n")
            
            # Log reminder
            log = ReminderLog(
                user_id=user.id,
                reminder_type=reminder_type
            )
            db.session.add(log)
            db.session.commit()
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to send reminder to {user.email}: {e}")
            return False
    
    def _get_reminder_content(self, user: User, reminder_type: str) -> tuple:
        """Get email subject and body based on reminder type"""
        
        if reminder_type == 'daily':
            subject = "🌟 Bạn chưa luyện tiếng Anh hôm nay - Chỉ cần 5 phút thôi!"
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #e74c3c;">Chào {user.name}! 👋</h2>
                    
                    <p>Hôm nay bạn chưa luyện tiếng Anh với Ms. Smile English.</p>
                    
                    <p><strong>Chỉ cần 5 phút</strong>, bạn có thể:</p>
                    <ul>
                        <li>Luyện 1 tình huống thực tế</li>
                        <li>Chat với AI</li>
                        <li>Ôn lại câu đã học</li>
                    </ul>
                    
                    <div style="background: #fff9f9; padding: 15px; border-radius: 8px; margin: 20px 0;">
                        <p style="margin: 0;">💡 <em>"Consistency is key to language learning"</em></p>
                    </div>
                    
                    <a href="http://localhost:5000" 
                       style="display: inline-block; background: #e74c3c; color: white; 
                              padding: 12px 30px; text-decoration: none; border-radius: 25px;">
                        🚀 Luyện ngay 5 phút
                    </a>
                    
                    <p style="color: #666; font-size: 12px; margin-top: 30px;">
                        Ms. Smile English - Trợ lý giao tiếp tiếng Anh của bạn
                    </p>
                </div>
            </body>
            </html>
            """
            
        elif reminder_type == '3days':
            progress = get_user_service().get_user_progress(user.id)
            streak = progress.current_streak if progress else 0
            
            subject = "😢 Bạn đang quên mất mục tiêu của mình rồi..."
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #e74c3c;">{user.name} ơi... 😢</h2>
                    
                    <p>Bạn đã <strong>3 ngày</strong> không luyện tiếng Anh rồi.</p>
                    
                    <p>Streak hiện tại của bạn: <strong style="color: #e74c3c; font-size: 24px;">{streak} ngày</strong></p>
                    
                    <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0;">
                        <p style="margin: 0;">💪 Đừng để công sức trước đó bị mất!</p>
                    </div>
                    
                    <p>Hãy quay lại ngay hôm nay:</p>
                    <ul>
                        <li>Chỉ 5 phút thôi</li>
                        <li>Chọn tình huống thực tế bạn đang cần</li>
                        <li>Luyện ngay câu gợi ý</li>
                    </ul>
                    
                    <a href="http://localhost:5000" 
                       style="display: inline-block; background: #27ae60; color: white; 
                              padding: 12px 30px; text-decoration: none; border-radius: 25px;">
                        💪 Quay lại ngay
                    </a>
                    
                    <p style="color: #666; font-size: 12px; margin-top: 30px;">
                        Ms. Smile English luôn ở đây chờ bạn!
                    </p>
                </div>
            </body>
            </html>
            """
            
        elif reminder_type == 'weekly':
            subject = "📊 Tiến độ tuần này của bạn"
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #3498db;">Báo cáo tuần này, {user.name}! 📊</h2>
                    
                    <p>Hãy xem bạn đã tiến bộ như thế nào:</p>
                    
                    <div style="background: #e8f4f8; padding: 15px; border-radius: 8px; margin: 20px 0;">
                        <p>🎯 Mục tiêu: Luyện 5 phút mỗi ngày</p>
                        <p>📈 Tiến độ: Đang theo dõi...</p>
                    </div>
                    
                    <a href="http://localhost:5000/dashboard" 
                       style="display: inline-block; background: #3498db; color: white; 
                              padding: 12px 30px; text-decoration: none; border-radius: 25px;">
                        📊 Xem tiến độ chi tiết
                    </a>
                </div>
            </body>
            </html>
            """
        
        else:
            subject = "🌟 Nhắc nhở luyện tiếng Anh"
            body = f"<p>Chào {user.name}, hãy quay lại luyện tiếng Anh nhé!</p>"
        
        return subject, body
    
    def check_and_send_reminders(self):
        """Check for inactive users and send reminders"""
        print("\n📧 Checking for reminders...")
        
        user_service = get_user_service()
        
        # 1 day inactive - daily reminder
        users_1day = self._get_users_inactive_for(1)
        for user in users_1day:
            if not self._was_reminded_recently(user.id, 'daily'):
                print(f"  → Sending daily reminder to {user.email or user.phone}")
                self.send_reminder_email(user, 'daily')
        
        # 3 days inactive - urgent reminder
        users_3days = self._get_users_inactive_for(3)
        for user in users_3days:
            if not self._was_reminded_recently(user.id, '3days'):
                print(f"  → Sending 3-day reminder to {user.email or user.phone}")
                self.send_reminder_email(user, '3days')
        
        print(f"📧 Sent {len(users_1day)} daily and {len(users_3days)} 3-day reminders\n")
    
    def _get_users_inactive_for(self, days: int) -> List[User]:
        """Get users inactive for specified days"""
        cutoff_date = datetime.now().date() - timedelta(days=days)
        
        # Users with progress who haven't studied since cutoff
        users = User.query.join(UserProgress).filter(
            UserProgress.last_study_date <= cutoff_date
        ).all()
        
        # Also include users who never studied (no last_study_date)
        never_studied = User.query.join(UserProgress).filter(
            UserProgress.last_study_date == None,
            User.created_at <= datetime.now() - timedelta(days=days)
        ).all()
        
        return users + never_studied
    
    def _was_reminded_recently(self, user_id: int, reminder_type: str) -> bool:
        """Check if user was reminded in last 24 hours"""
        yesterday = datetime.now() - timedelta(hours=24)
        
        recent = ReminderLog.query.filter(
            ReminderLog.user_id == user_id,
            ReminderLog.reminder_type == reminder_type,
            ReminderLog.sent_at >= yesterday
        ).first()
        
        return recent is not None


# Singleton
_reminder_service = None

def get_reminder_service():
    global _reminder_service
    if _reminder_service is None:
        _reminder_service = ReminderService()
    return _reminder_service
