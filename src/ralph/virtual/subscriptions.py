import logging

import pkg_resources
import pyhermes
from django.conf import settings
from django.utils.text import slugify



logger = logging.getLogger(__name__)


ENTRY_POINTS_GROUP = 'ralph.dchost_processors'
ENDPOINT_PREFIX = 'cloud-sync-'
DCHOST_PROCESSORS = {}
SUBSCRIPTIONS = {}


def load_processors():
    for ep in pkg_resources.iter_entry_points(ENTRY_POINTS_GROUP):
        try:
            DCHOST_PROCESSORS[ep.name] = ep.resolve()
        except ImportError:
            logger.error(
                'Could not import DC asset event processor from {}.'
                ''.format(ep.module_name)
            )


def generate_listeners():
    load_processors()

    from ralph.virtual.models import CloudProvider
    cloud_providers = CloudProvider.objects.filter(
        sync_enabled=True,
        sync_event_processor__isnull=False
    ).all()

    for cloud in cloud_providers:
        sub_name = ENDPOINT_PREFIX + slugify(cloud.name)

        # NOTE(romcheg): Work around the issue when ready() hook is called
        #                10 times.
        if sub_name in SUBSCRIPTIONS:
            continue

        SUBSCRIPTIONS[sub_name] = pyhermes.subscriber(sub_name)(
            DCHOST_PROCESSORS[cloud.sync_event_processor.module]
        )
