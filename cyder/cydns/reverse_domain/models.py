from django.db import models
from cyder.cydns.soa.models import Soa
import ipaddr
import pdb

class Reverse_Domain( models.Model ):
    id                      = models.AutoField(primary_key=True)
    name                    = models.CharField(max_length=100)
    master_reverse_domain   = models.ForeignKey("self", null=True)
    soa                     = models.ForeignKey(Soa, null=True)

    class Meta:
        db_table = 'reverse_domain'

class ReverseDomainNotFoundError(Exception):
    def __str__(self):
        return "No reverse domain found. Condisder creating one."

class ReverseDomainExistsError(Exception):
    def __str__(self):
        return "Reverse domain already exists."
"""
Given an ip return the most specific reverse domain that the ip can belong to.
@param: ip <ipaddr.IpAddres>
@return: Reverse_Domain <'object'>
"""
def ip_to_reverse_domain( ip, split='.' ):
    octets = ip.split(split)
    for i in reversed(range(len(octets)+1)):
        search_reverse_domain = split.join(octets[:i])
        rev_dom = Reverse_Domain.objects.filter( name = search_reverse_domain )
        if rev_dom:
            return rev_dom
        else:
            continue
    raise ReverseDomainNotFoundError

"""
There are some formalities that need to happen when a reverse domain is added. For example
say we had the ip address 128.193.4.0 and it had the reverse_domain 128.193. If we add the
reverse_domain 128.193.4, our 128.193.4.0 no longer belongs to the 128.193 domain. We need
to re-asign the ip to it's correct reverse domain.
This function needs to:
    1) Get all it's master_domain.
    2) Get all ip's that belong to the master_domain.
        * if any ip's now belong to the new reverse_domain, reassign the ip.
"""
def add_reverse_ipv4_domain( name, master_reverse_domain ):
    #For now just add it. MUST ADD LOGIC HERE TODO

    if master_reverse_domain is None:
        soa = None
    else:
        soa = master_reverse_domain.soa

    reverse_domain = Reverse_Domain( name=name, master_reverse_domain=None, soa=soa )
    reverse_domain.save()

"""
Use ipaddr.IPv6Address('2001:0db8:85a3:0002:0:0:0:2').__str__()
this will represent the ip in a consisten manner.
"""
def add_reverse_ipv6_domain( name, master_reverse_domain ):
    #For now just add it. MUST ADD LOGIC HERE TODO
    try:
        ip = ipaddr.IPv6Address(name)
    except ipaddr.AddressValueError, e:
        raise

    if master_reverse_domain is None:
        soa = None
    else:
        soa = master_reverse_domain.soa

    # Check for a domain that already exists.
    ip_name = ip.__str__().rstrip(':') #Get rid of trailing ':'
    if Reverse_Domain.objects.filter( name=ip_name ):
        raise ReverseDomainExistsError

    reverse_domain = Reverse_Domain( name=ip_name, master_reverse_domain=None, soa=soa )
    reverse_domain.save()
