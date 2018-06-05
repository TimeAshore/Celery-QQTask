#encoding: utf-8
from celery.schedules import crontab

# Broker and Backend
BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'

CELERY_TIMEZONE='Asia/Shanghai'    # 指定时区，不指定默认为 'UTC'
# CELERY_TIMEZONE='UTC'

# import
CELERY_IMPORTS = (
    'celery_app.task1',
)
# schedules
CELERYBEAT_SCHEDULE = {
    'multiply-at-some-time': {
        'task': 'celery_app.task1.send_email_image',
        'schedule': crontab(hour=6, minute=20),   # 每天早上 6 点 00 分执行一次
        'args': ()                                  # 任务函数参数
    }
}