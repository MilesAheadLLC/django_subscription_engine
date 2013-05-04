from django.db import models
from subscription_engine.models import Subscription

class TestUser(models.Model):
    name = models.CharField(unique=True, max_length=75)
    subscription = models.ForeignKey(Subscription)