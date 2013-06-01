import pytest
import re

from django.core import mail
from django.core.urlresolvers import reverse

from subscription_engine.mail import send_email, render_message
from subscription_engine.models import Subscription
from subscription_engine.tests.fixtures.models import TestUser

@pytest.mark.xfail
def test_user_can_unsubscribe():
    pass

@pytest.mark.xfail
@pytest.mark.django_db
def test_user_is_sent_to_unsubscribed_page(client):
    """
      User is sent to a unsubscribe confirmation page
     """
    email = mail.EmailMessage('Subject', 'Body', 'from@example.com', ['to@example.com'])
    sub = Subscription(name='Test')
    sub.save()

    user = TestUser(name='TestUser', subscription=sub)
    user.save()

    send_email(email, sub, user, subscription_view_name='unsubscribe', unsubscribe_template='unsubscribe.html')

    messages = mail.outbox

    print messages[0].body
    email_url = re.search("(?P<url>https?://[^\s]+)", messages[0].body).group('url')

    location = email_url.split("http://example.com")[1]

    response = client.get(location)
    assert reverse('unsubscribe_confirmation') in response.get('location')

@pytest.mark.django_db
def test_send_email(email_mem_backend):
    """
     Test that send_email sends an email witht the unsubscribe template filled out
    """
    email = mail.EmailMessage('Subject', 'Body', 'from@example.com', ['to@example.com'])
    sub = Subscription(name='Test')
    sub.save()

    user = TestUser(name='TestUser', subscription=sub)
    user.save()

    send_email(email, sub, user, subscription_view_name='unsubscribe', unsubscribe_template='unsubscribe.html')

    messages = mail.outbox

    assert "To unsubscribe from this email list " + reverse('unsubscribe', args=[user.pk, sub.token]) in messages[0].body

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


