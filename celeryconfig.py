# config file for Celery Daemon

# default RabbitMQ broker
BROKER_URL = 'amqp://psrc:psrc1@10.10.11.194/psrcvhost'

# default RabbitMQ backend
CELERY_RESULT_BACKEND = 'amqp://'

# specify location of log files
CELERYD_LOG_FILE="celery.log"