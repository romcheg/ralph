from django.test import TestCase

from ralph.assets.models import Ethernet
from ralph.data_center.tests.factories import (
    DataCenterAssetFactory,
    RackFactory
)
from ralph.networks.models.networks import IPAddress
from ralph.networks.tests.factories import (
    IPAddressFactory,
    NetworkEnvironmentFactory,
    NetworkFactory
)
from ralph.virtual.tests.factories import VirtualServerFactory


class _BaseTestDeploymentActionsTestCase(object):
    def test_clean_hostname(self):
        self.instance.hostname = 'test'
        self.instance.__class__.clean_hostname([self.instance])
        # TODO: needs NullableCharField fix for VirtualServer
        self.assertIsNone(self.instance.hostname)

    def test_clean_dns(self):
        # TODO
        pass

    def test_clean_ipaddresses(self):
        ip = IPAddressFactory(ethernet__base_object=self.instance)
        ip_mgmt = IPAddressFactory(
            ethernet__base_object=self.instance, is_management=True
        )
        ip_without_eth = IPAddressFactory(
            ethernet__base_object=self.instance,
            ethernet__mac=None,
            ethernet__label=None,
        )
        self.instance.__class__.clean_ipaddresses([self.instance])
        # eth of ip should not be deleted
        ip.ethernet.refresh_from_db()
        # ip should be deleted
        with self.assertRaises(IPAddress.DoesNotExist):
            ip.refresh_from_db()
        # ip mgmt should not be deleted
        ip_mgmt.refresh_from_db()
        # ip without eth, as well as its ethernet should be deleted
        with self.assertRaises(Ethernet.DoesNotExist):
            ip_without_eth.ethernet.refresh_from_db()
        with self.assertRaises(IPAddress.DoesNotExist):
            ip_without_eth.refresh_from_db()

    def test_clean_dhcp(self):
        # TODO
        pass

    def _prepare_rack(self):
        self.rack = RackFactory()
        self.net_env = NetworkEnvironmentFactory(
            hostname_template_prefix='server_1',
            hostname_template_postfix='.mydc.net',
        )
        self.net = NetworkFactory(
            network_environment=self.net_env,
            address='10.20.30.0/24',
        )
        self.net.racks.add(self.rack)

    def test_assign_new_hostname(self):
        net_env = NetworkEnvironmentFactory()
        net_env.racks.add(self.instance.rack)
        next_free_hostname = self.instance.get_next_free_hostname()
        self.instance.__class__.assign_new_hostname(
            [self.instance], net_env.id
        )
        self.assertEqual(self.instance.hostname, next_free_hostname)


class DataCenterAssetDeploymentActionsTestCase(
    _BaseTestDeploymentActionsTestCase, TestCase
):
    def setUp(self):
        self.instance = DataCenterAssetFactory()


class VirtualServerDeploymentActionsTestCase(
    _BaseTestDeploymentActionsTestCase, TestCase
):
    def setUp(self):
        self.instance = VirtualServerFactory()
