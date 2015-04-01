from __future__ import absolute_import

from celery import Celery

app = Celery('tasks', backend='amqp',
                      broker='amqp://psrc:psrc1@10.10.11.194/psrcvhost')
@app.task
def add(x, y):
     return x + y