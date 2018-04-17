import logging


LOGGER = logging.getLogger(__name__)


def endpoint(event_data):
    """The endpoint for DC asset synchronisation that does nothing."""
    LOGGER.info('Received new DC asset syncronisation event. Doing nothing.')
