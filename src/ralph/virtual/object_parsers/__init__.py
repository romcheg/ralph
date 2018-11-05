import logging

from ralph.virtual.object_parsers import nova

logger = logging.getLogger(__name__)


OBJECT_PARSERS = {
    'FlavorPayload': {
        '1.2': nova.parse_flavor_1_2,
    },
    'InstanceUpdatePayload': {
        '1.1': nova.parse_instance_update_1_1,
    },
    'InstanceActionPayload': {
        '1.1': nova.parse_instance_action_1_1,
    },
}


def get_object_parser(object_type, version):
    try:
        return OBJECT_PARSERS[object_type][version]
    except KeyError:
        logger.error(
            'Parser for the specified object type or version was not found.'
        )
