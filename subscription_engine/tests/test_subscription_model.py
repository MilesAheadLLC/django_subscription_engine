import pytest

from django.contrib.contenttypes.models import ContentType

from subscription_engine.models import Subscription, SubscriptionAssignment
from subscription_engine.tests.fixtures.models import TestUser

@pytest.mark.django_db
def test_subscription_generates_random_token():
    """
     Subscription model should assign a random token for each subscription
    """

    sub = Subscription(name='Beta')
    sub.save()

    sub2 = Subscription(name='Beta2')
    sub2.save()

    user = TestUser(name="Tester")
    user.save()

    assignment = SubscriptionAssignment(content_object=user, subscription=sub)
    assignment.save()

    user_type = ContentType.objects.get_for_model(TestUser)

    assignment = SubscriptionAssignment.objects.get(content_type=user_type, object_id=user.id, subscription=sub)

    assignment2 = SubscriptionAssignment(content_object=user, subscription=sub2)
    assignment2.save()

    assignment2 = SubscriptionAssignment.objects.get(content_type=user_type, object_id=user.id, subscription=sub2)

    assert assignment.token != assignment2.token

@pytest.mark.django_db
def test_subscription_contains_correct_attributes():
    """
     Subscription model should have - name, created_at, update_at, active
    """
    sub = Subscription(name='Beta')
    sub.save()

    sub3 = Subscription.objects.get(name='Beta')
    assert sub3.updated_at
    assert sub3.created_at
    assert sub3.active is True

@pytest.mark.django_db
def test_subscription_assignment_contains_correct_attributes():
    """
     Subcription assignment model should have name, created_at, updated_at, user_id and subscription_id
    """

    sub = Subscription(name='Beta')
    sub.save()

    user = TestUser(name="Tester")
    user.save()

    assignment = SubscriptionAssignment(content_object=user, subscription=sub)
    assignment.save()

    user_type = ContentType.objects.get_for_model(TestUser)

    assignment = SubscriptionAssignment.objects.get(content_type=user_type, object_id=user.id, subscription=sub)

    assert assignment.created_at
    assert assignment.updated_at
    assert assignment.subscription.id == sub.id
    assert assignment.object_id == user.id
    assert assignment.token
    assert assignment.active is True
    assert assignment.content_object
    assert assignment.content_type

@pytest.mark.django_db
def test_subscription_assignment_cannot_save_the_same_user_and_subscription():
    """
     Subscription assignment only allows for subscription assignment to be saved to the same user
    """

    sub = Subscription(name='Beta')
    sub.save()

    user = TestUser(name="Tester")
    user.save()

    assignment = SubscriptionAssignment(content_object=user, subscription=sub)
    assignment.save()

    assignment2 = SubscriptionAssignment(content_object=user, subscription=sub)

    try:
        assignment2.save()
    except Exception as error:
        pass

    assert error

