import logging
import os

from django.db import ProgrammingError

from ralph.apps import RalphAppConfig
from ralph.virtual.subscriptions import generate_listeners


logger = logging.getLogger(__name__)


class Virtual(RalphAppConfig):

    name = 'ralph.virtual'

    def ready(self):
        super().ready()

        try:
            generate_listeners()
        except ProgrammingError as e:
            logger.info(
                'Some cloud sync endpoints were not created due to a generic '
                'DB problem. This could have happened because Ralph is not '
                'running, e. g., when applying a DB migration.{}{}'
                ''.format(os.linesep, e)
            )
