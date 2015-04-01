# config file for Celery Daemon

# default RabbitMQ broker
BROKER_URL = 'amqp://psrc:psrc1@10.10.11.194/psrcvhost'

# List of modules to import when celery starts.
CELERY_IMPORTS = ('tasks', )

# default RabbitMQ backend
CELERY_RESULT_BACKEND = 'amqp://'

# specify location of log files
CELERYD_LOG_FILE="celery.log"


#from celery.signals import setup_logging
#@setup_logging.connect
#def configure_logging(sender=None, **kwargs):
#    import logging
#    import logging.config
#    logging.config.dictConfig(LOGGING)