from __future__ import absolute_import

# This will make sure the app is always imported when 
# Django starts to that shared_task will use this app.
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())