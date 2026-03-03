from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import database
import datetime
from config import SILENT_TIMEOUT_HOURS

class DevCoreScheduler:
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()

    def start(self):
        # Schedule daily review check
        self.scheduler.add_job(
            self.send_daily_reviews,
            CronTrigger(hour=9, minute=0) # Every day at 9:00 AM
        )
        
        # Schedule inactivity check
        self.scheduler.add_job(
            self.check_user_inactivity,
            CronTrigger(hour=18, minute=0) # Every day at 6:00 PM
        )
        
        self.scheduler.start()

    async def send_daily_reviews(self):
        """
        Send scheduled review prompts via Telegram.
        """
        conn = database.get_db_connection()
        today = datetime.date.today()
        due_reviews = conn.execute("""
            SELECT user_id, topic, concept FROM review_schedule 
            WHERE due_date <= ? AND completed = FALSE
        """, (today,)).fetchall()
        conn.close()
        
        for review in due_reviews:
            user_id = review["user_id"]
            topic = review["topic"]
            concept = review["concept"]
            
            message = f"🔔 *Spaced Repetition Review*\n\nTopic: `{topic}`\nConcept: `{concept}`\n\nReady to review? Use `/learn {topic}` or `/quiz {topic}`."
            try:
                await self.bot.send_message(chat_id=user_id, text=message, parse_mode="Markdown")
            except Exception as e:
                print(f"Error sending review to user {user_id}: {e}")

    async def check_user_inactivity(self):
        """
        Check for inactive users and send re-engagement messages.
        """
        conn = database.get_db_connection()
        cutoff = datetime.datetime.now() - datetime.timedelta(hours=SILENT_TIMEOUT_HOURS)
        inactive_users = conn.execute("""
            SELECT user_id, first_name FROM users 
            WHERE last_active < ?
        """, (cutoff,)).fetchall()
        
        for user in inactive_users:
            user_id = user["user_id"]
            # Get their last topic
            last_topic = conn.execute("""
                SELECT topic FROM user_knowledge 
                WHERE user_id = ? ORDER BY last_reviewed DESC LIMIT 1
            """, (user_id,)).fetchone()
            
            topic_name = last_topic["topic"] if last_topic else "your engineering journey"
            
            message = f"👋 Hello {user["first_name"]}, it's been a while. " \
                      f"Last topic: `{topic_name}`. Resume? Use `/learn {topic_name}`."
            try:
                await self.bot.send_message(chat_id=user_id, text=message, parse_mode="Markdown")
            except Exception as e:
                print(f"Error sending inactivity reminder to user {user_id}: {e}")
        
        conn.close()

def schedule_review(user_id, topic, concept, days=1):
    """
    Schedule a review task in the database.
    """
    due_date = datetime.date.today() + datetime.timedelta(days=days)
    conn = database.get_db_connection()
    conn.execute("""
        INSERT INTO review_schedule (user_id, topic, concept, due_date)
        VALUES (?, ?, ?, ?)
    """, (user_id, topic, concept, due_date))
    conn.commit()
    conn.close()
