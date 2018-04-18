import logging

import pkg_resources
import pyhermes
from django.conf import settings


LOGGER = logging.getLogger(__name__)


ENTRY_POINTS_GROUP = 'ralph.dchost_processors'
DCHOST_PROCESSORS = {}
SUBSCRIPTIONS = {}


def load_processors():
    for ep in pkg_resources.iter_entry_points(ENTRY_POINTS_GROUP):
        try:
            DCHOST_PROCESSORS[ep.name] = ep.resolve()
        except ImportError:
            LOGGER.error(
                'Could not import DC asset event processor from {}.'
                ''.format(ep.module_name)
            )


def generate_listeners():
    load_processors()

    for subscription_config in settings.DCASSET_SYNC_ENDPOINTS:
        sub_name = subscription_config['name']

        # NOTE(romcheg): Work around the issue when ready() hook is called
        #                10 times.
        if sub_name in SUBSCRIPTIONS:
            continue

        SUBSCRIPTIONS[sub_name] = pyhermes.subscriber(sub_name)(
            DCHOST_PROCESSORS[subscription_config['processor']]
        )
