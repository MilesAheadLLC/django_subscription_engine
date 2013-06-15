import hashlib
import random
import string


from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models

from django_helpers.models import CreateUpdateModel

class Subscription(CreateUpdateModel):
    """
     Describes a subscription as a static entity that can be active or inactive
    """
    name = models.CharField(unique=True, max_length=100)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class SubscriptionAssignment(CreateUpdateModel):
    """
     Describes a subscription assignment between another model and a subscription
    """
    content_type = models.ForeignKey(ContentType)
    subscription = models.ForeignKey(Subscription)
    token = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def tokengen(self):
        seed = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(16))
        return hashlib.sha1(seed + settings.SECRET_KEY).hexdigest()

    def save(self, force_insert=False, force_update=False, using=None):
        self.token = self.tokengen()
        return super(SubscriptionAssignment, self).save(force_insert, force_update, using)

    class Meta:
        unique_together = (('content_type', 'subscription', 'object_id'),)



