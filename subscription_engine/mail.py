from django.core.urlresolvers import reverse
from django.template.loader import render_to_string


def send_email(email,subscription, model, subscription_view_name='unsubscribe', unsubscribe_template='unsubscribe.html'):
    unsubscribe_url = reverse(subscription_view_name, args=[model.pk, subscription.token])
    email.body = render_message(email.body, unsubscribe_url, unsubscribe_template)
    email.send()

def render_message(body, url, template):
    """
     Wrapper around render_to_string which feeds the template additional context, body and url.
    """
    context = { 'body':body, 'unsubscribe_url':url}
    return render_to_string(template, context)