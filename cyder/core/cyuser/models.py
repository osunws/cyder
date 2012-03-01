from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals

from cyder.core.ctnr.models import Ctnr


class UserProfile( models.Model ):
    user            = models.OneToOneField(User)
    default_ctnr    = models.ForeignKey(Ctnr, default=0)
    phone_number    = models.IntegerField(null=True)


def create_user_profile(sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        profile = UserProfile(user=user)
        profile.save()

signals.post_save.connect(create_user_profile, sender=User)
