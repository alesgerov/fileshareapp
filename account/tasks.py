from celery import shared_task
from .models import File
from time import sleep
from django.shortcuts import get_object_or_404
import datetime
from django.utils import timezone

@shared_task
def schedulerDelete():
    File.objects.filter(date_posted__lte=datetime.datetime.now()-datetime.timedelta(days=7)).delete()
    return None