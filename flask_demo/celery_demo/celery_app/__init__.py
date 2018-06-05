#encoding: utf-8
from celery import Celery

cele = Celery('demo')
cele.config_from_object('celery_app.celeryconfig')