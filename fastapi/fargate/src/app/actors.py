import dramatiq

import logging
logger = logging.getLogger(__name__)




@dramatiq.actor
def sample_actor():
    logger.error("I did it,")
