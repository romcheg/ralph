def parse_instance_update_1_1(nova_obj_data):
    return {
        'host_id': nova_obj_data['uuid'],
        'hostname': nova_obj_data['host_name'],
        'hypervisor': nova_obj_data['host'],
        'image_name': fetch_image_name(
            nova_obj_data['image_uuid']
        ),
    }


parse_instance_action_1_1 = parse_instance_update_1_1


def parse_flavor_1_2(nova_obj_data):
    return {
        'name': nova_obj_data['name'],
        'flavor_id': nova_obj_data['flavorid'],
    }


def fetch_image_name(image_uuid):
    # TODO(romcheg): Implement this
    return image_uuid
