"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import ipaddr
from cyder.cydns.ip.models import ipv6_to_longs, Ip, add_str_ipv4, add_str_ipv6
from cyder.cydns.reverse_domain.models import add_reverse_ipv4_domain
from cyder.cydns.reverse_domain.models import boot_strap_add_ipv6_reverse_domain
import pdb

class SimpleTest(TestCase):
    def test_ipv4_str(self):
        rd = add_reverse_ipv4_domain('192')
        ip_str = '192.168.1.1'
        ip = ipaddr.IPv4Address(ip_str)
        new_ip = Ip( ip_upper = 0, ip_lower = ip.__int__(), reverse_domain = rd, ip_type = '4')
        self.assertEqual(ip_str, new_ip.__str__())
        rd = add_reverse_ipv4_domain('128')
        ip_str = '128.193.2.1'
        ip = ipaddr.IPv4Address(ip_str)
        ip.__int__()
        new_ip = Ip( ip_upper = 0, ip_lower = ip.__int__(), reverse_domain = rd, ip_type = '4')
        self.assertEqual(ip_str, new_ip.__str__())

    def test_ipv6_str(self):
        rd = boot_strap_add_ipv6_reverse_domain('1.2.3.4')
        ip_str = '1234:1234:1243:1243:1243::'
        ip = ipaddr.IPv6Address(ip_str)
        ip_upper, ip_lower = ipv6_to_longs(ip_str)
        self.assertEqual( ip.__int__(), (2**64)*ip_upper + ip_lower)
        new_ip = Ip( ip_upper = ip_upper, ip_lower = ip_lower, reverse_domain = rd, ip_type = '6')
        self.assertEqual(ip_str, new_ip.__str__())
        ip_str = '1234:432:3:0:3414:22::'
        ip = ipaddr.IPv6Address(ip_str)
        ip_upper, ip_lower = ipv6_to_longs(ip_str)
        new_ip = Ip( ip_upper = ip_upper, ip_lower = ip_lower, reverse_domain = rd, ip_type = '6')
        self.assertEqual(ip_str, new_ip.__str__())

    def test_large_ipv6(self):
        rd = boot_strap_add_ipv6_reverse_domain('f')
        ip_str = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'
        ip = ipaddr.IPv6Address(ip_str)
        ip_upper, ip_lower = ipv6_to_longs(ip_str)
        self.assertEqual( ip.__int__(), (2**64)*ip_upper + ip_lower)
        new_ip = Ip( ip_upper = ip_upper, ip_lower = ip_lower, reverse_domain = rd, ip_type = '6')
        self.assertEqual(ip_str, new_ip.__str__())

    def test_int_ip(self):
        rd = add_reverse_ipv4_domain('128')
        ip = add_str_ipv4("128.193.1.1")
        ip.__int__()
        ip.__repr__()
        rd = boot_strap_add_ipv6_reverse_domain('e')
        ip_str = 'efff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'
        ip = add_str_ipv6(ip_str)
        ip.__int__()
        ip.__repr__()
