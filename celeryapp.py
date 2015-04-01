from __future__ import absolute_import
from celery.utils.log import get_task_logger
from celery import Celery
import logging

# app = Celery(
#               broker='amqp://',
#               backend='amqp://',
#               include=['tasks'])

app = Celery()

app.config_from_object('celeryconfig')

logger = get_task_logger(__name__)

@app.task
def add(x, y):
    logger.info('Adding %s + %s' % (x, y))
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

# # instantiate Celery object
# celery = Celery(include=[
#                          'tasks'
#                         ])

# Optional configuration, see the application user guide.
# app.conf.update(
#     CELERY_TASK_RESULT_EXPIRES=3600,
# )

# import celery config file

if __name__ == '__main__':
    app.start()