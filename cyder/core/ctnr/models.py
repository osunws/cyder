from django.contrib.auth.models import User
from django.db import models

from cyder.cydhcp.range.models import Range
from cyder.cydns.domain.models import Domain
from cyder.cydns.models import ObjectUrlMixin
from cyder.cydns.reverse_domain.models import ReverseDomain


class Ctnr(models.Model, ObjectUrlMixin):
    id              = models.AutoField(primary_key=True)
    name            = models.CharField(max_length=100, unique=True)
    users           = models.ManyToManyField(User, null=False, related_name='users', through='CtnrUser')
    domains         = models.ManyToManyField(Domain, null=False)
    reverse_domains = models.ManyToManyField(ReverseDomain, null=False)
    ranges          = models.ManyToManyField(Range, null=False)
    description     = models.CharField(max_length=200)
    purgeable       = models.BooleanField()

    class Meta:
        db_table = 'ctnr'

    def __str__(self):
        return self.name

    def details(self):
        return (
            ('Name', self.name),
            ('Description', self.description),
        )


class CtnrUser(models.Model):
    user = models.ForeignKey(User)
    ctnr = models.ForeignKey(Ctnr)
    level = models.IntegerField()

    class Meta:
        db_table = 'ctnr_users'
        unique_together = ('ctnr', 'user')
