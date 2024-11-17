from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import check_for_notifications

def init_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_for_notifications, trigger="interval", hours=24)
    scheduler.start()