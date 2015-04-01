from __future__ import absolute_import

from celery import Celery

app = Celery(
              broker='amqp://',
              backend='amqp://',
              include=['tasks'])

# instantiate Celery object
celery = Celery(include=[
                         'tasks'
                        ])

# Optional configuration, see the application user guide.
# app.conf.update(
#     CELERY_TASK_RESULT_EXPIRES=3600,
# )

# import celery config file
celery.config_from_object('celeryconfig')

if __name__ == '__main__':
    app.start()