from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from django_apscheduler.jobstores import register_events, DjangoJobStore
import time
from .views import check


def start():
    scheduler=BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    @scheduler.scheduled_job('cron', hour=23, name = 'auto_check')
    def auto_check():
        check()
    scheduler.start()