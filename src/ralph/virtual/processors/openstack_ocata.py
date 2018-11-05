import logging

from ralph.virtual.object_parsers import get_object_parser
from ralph.virtual.models import CloudHost


logger = logging.getLogger(__name__)


def endpoint(cloud_provider, event_data):
    try:
        event_type = event_data['event_type']
        event_payload = event_data['payload']

        logger.info(
            'Received {} event from {}'.format(event_type, cloud_provider.name)
        )

        if event_type not in OS_EVENT_HANDLERS:
            logger.debug('Event type does not have specified handler.')

        handler = OS_EVENT_HANDLERS[event_type]
        handler(event_payload)
    except KeyError as e:
        logger.error('Malformed event payload. Key {} not found'.format(e))


def delete_cloudhost(event_payload):
    instance_parser = get_object_parser(
        event_payload['nova_object.name'],
        event_payload['nova_object.version']
    )

    parsed_instance = instance_parser(event_payload['nova_object.data'])

    CloudHost.objects.filter(host_id=parsed_instance['host_id']).delete()


OS_EVENT_HANDLERS = {
    'instance.delete.end': delete_cloudhost,
}
