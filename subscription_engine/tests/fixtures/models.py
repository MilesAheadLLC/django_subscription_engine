from django.db import models
from django.contrib.contenttypes import generic
from subscription_engine.models import SubscriptionAssignment

class TestUser(models.Model):
    """
     Test user model
    """
    name = models.CharField(unique=True, max_length=75)

