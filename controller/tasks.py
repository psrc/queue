from __future__ import absolute_import

from celery import shared_task

@shared_task(track_started=True)
def add(x, y):
    return x + y

@shared_task(track_started=True)
def mu1(x, y):
    return x * y

@shared_task(track_started=True)
def xsum(numbers):
    return sum(numbers)
