from subscription_engine.models import Subscription
from factory_boy import factory

class SubscriptionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Subscription
    FACTORY_DJANGO_GET_OR_CREATE = ('name')

    name = 'test_subscription'