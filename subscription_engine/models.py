import hashlib
import random
import string

from django.conf import settings
from django.db import models

from django_helpers.models import CreateUpdateModel

class Subscription(CreateUpdateModel):
    """
     Describes a subscription
    """
    name = models.CharField(unique=True, max_length=100)
    active = models.BooleanField(default=True)
    token = models.CharField(max_length=50)

    def tokengen(self):
        seed = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(16))
        return hashlib.sha1(seed + settings.SECRET_KEY).hexdigest()


    def save(self, force_insert=False, force_update=False, using=None):
        self.token = self.tokengen()
        return super(Subscription, self).save(force_insert, force_update, using)

    def __unicode__(self):
        return self.name