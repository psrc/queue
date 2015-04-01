from celery import Celery

app = Celery('tasks', backend='amqp',
                      broker='amqp://psrc:psrc1@10.10.11.89/psrcvhost')

def add(x, y):
     return x + y