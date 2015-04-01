from celery import Celery
import os

app = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y

@app.task
def mul(x, y):
    return x * y

@app.task
def xsum(numbers):
    return sum(numbers)

@app.task
def make_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)