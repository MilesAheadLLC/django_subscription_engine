import pytest
import re

from django.contrib.sites.models import Site
from django.core import mail
from django.core.urlresolvers import reverse

from subscription_engine.mail import send_email, render_message
from subscription_engine.models import Subscription, SubscriptionAssignment
from subscription_engine.tests.fixtures.models import TestUser

def create_email_sub_user():
    """
     Helper function to create test email, sub and user
    """
    email = mail.EmailMessage('Subject', 'Body', 'from@example.com', ['to@example.com'])

    user = TestUser(name='Test')
    user.save()

    sub = Subscription(name='Sub')
    sub.save()

    usersub = SubscriptionAssignment(content_object=user, subscription=sub)
    usersub.save()

    return (email, usersub, user)

@pytest.mark.django_db
def test_use_http(email_mem_backend):
    """
     Check to see if the unsubscribe_url can be set to http
    """
    email, sub, user = create_email_sub_user()
    send_email(email, sub, user, subscription_view_name='unsubscribe', unsubscribe_template='unsubscribe.html', secure=False)
    messages = mail.outbox

    email_url = re.search("(?P<url>http?://[^\s]+)", messages[0].body).group('url')

    assert email_url.split("://example")[0] == 'http'

@pytest.mark.django_db
def test_use_https(email_mem_backend):
    """
     Check to see if the unsubscribe_url can be set to http
    """
    email, sub, user = create_email_sub_user()
    send_email(email, sub, user, subscription_view_name='unsubscribe', unsubscribe_template='unsubscribe.html')
    messages = mail.outbox

    email_url = re.search("(?P<url>https?://[^\s]+)", messages[0].body).group('url')

    assert email_url.split("://example")[0] == 'https'

@pytest.mark.django_db
def test_user_is_sent_to_unsubscribed_page(client,email_mem_backend):
    """
      User is sent to a unsubscribe confirmation page
     """
    email, usersub, user = create_email_sub_user()
    send_email(email, usersub, user, subscription_view_name='unsubscribe', unsubscribe_template='unsubscribe.html')
    messages = mail.outbox

    email_url = re.search("(?P<url>https?://[^\s]+)", messages[0].body).group('url')
    location = email_url.split("https://example.com")[1]
    response = client.get(location)

    assert "You have been successfully unsubscribed" in response.content

@pytest.mark.django_db
def test_user_can_unsubscribe(client,email_mem_backend):
    """
     User is unsubscribed from subscription
    """
    email, sub, user = create_email_sub_user()
    send_email(email, sub, user, subscription_view_name='unsubscribe', unsubscribe_template='unsubscribe.html')
    messages = mail.outbox

    email_url = re.search("(?P<url>https?://[^\s]+)", messages[0].body).group('url')
    location = email_url.split("https://example.com")[1]
    response = client.get(location)

    # Get new value for sub
    sub = SubscriptionAssignment.objects.get(pk=sub.pk)

    assert not sub.active

@pytest.mark.django_db
def test_user_receives_error_page_when_subscription_not_found(client):
    """
     If the link is incorrect the user receives and error page
    """
    response = client.get("/1-24928592045/")

    assert "This didn't work correctly" in response.content

@pytest.mark.django_db
def test_send_email(email_mem_backend):
    """
     Test that send_email sends an email with the unsubscribe template filled out
    """
    email, usersub, user = create_email_sub_user()
    send_email(email, usersub, user, subscription_view_name='unsubscribe', unsubscribe_template='unsubscribe.html')
    messages = mail.outbox

    unsubscribe_path = reverse('unsubscribe', args=[user.pk, usersub.token])
    unsubscribe_url = "https://{site}{path}".format(site=Site.objects.get_current(), path=unsubscribe_path)

    assert "To unsubscribe from this email list " +  unsubscribe_url in messages[0].body

def test_renders_message_body():
    """
     Test that render_message generates a message body using the correct template
    """
    body = "This is a test"
    url = "http://unsubscribeurl"
    template = "unsubscribe.html"
    message =  render_message(body, url, template)

    assert body in message
    assert url in message


