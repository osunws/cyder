from cyder.cydns.nameserver.nameserver.models import Nameserver
from cyder.cydns.nameserver.view_tests import *


class NSViewTests(TestCase):
    def setUp(self):
        url_slug = "nameserver"
        dname = random_label()
        self.client = Client()
        self.url_slug = url_slug
        self.domain, create = Domain.objects.get_or_create(name=dname)
        while not create:
            dname = "a"+dname
            self.domain, create = Domain.objects.get_or_create(name=dname)
        server = random_label()
        self.test_obj, create = Nameserver.objects.get_or_create( server=server, domain= self.domain )
        while not create:
            server = "a"+server
            self.test_obj, create = Nameserver.objects.get_or_create( server=server, domain= self.domain )

    def post_data(self):
        server = random_label()
        return {'server': server, 'domain':self.domain.pk}


builder = GenericViewTests()
for test in builder.build_all_tests():
    setattr(NSViewTests,test.__name__+"_ns", test)
