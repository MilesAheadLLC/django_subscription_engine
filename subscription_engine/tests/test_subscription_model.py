import pytest

from subscription_engine.models import Subscription

@pytest.mark.django_db
def test_subscription_generates_random_token():
    """
     Subscription model should assign a random token for each subscription
    """
    sub = Subscription(name='Beta')
    sub.save()

    sub2 = Subscription(name='Test')
    sub2.save()

    sub3 = Subscription.objects.get(name='Beta')
    sub4 = Subscription.objects.get(name='Test')

    assert sub3.token != sub4.token

@pytest.mark.django_db
def test_subscription_contains_correct_attributes():
    """
     Subscription model should have - name, created_at, update_at, active, and token
    """
    sub = Subscription(name='Beta')
    sub.save()

    sub3 = Subscription.objects.get(name='Beta')
    assert sub.updated_at
    assert sub.created_at
    assert sub.active is True
    assert sub3.token

