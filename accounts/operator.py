from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from .views import check


def start():
    scheduler=BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    @scheduler.scheduled_job('cron', minute = 1, name = 'auto_check')
    #@scheduler.scheduled_job('cron', hour=23, name = 'expiry_check')
    def auto_check():
        check()
    scheduler.start()