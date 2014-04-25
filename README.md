# Django Subscrption Engine

As far as I know this works and I needed it for another project that was cancelled. Ata minimum it should serve as an example of how to build a custom mailer for django if you need one. If there is some interest I'll clean it up and add some docs.

The Django Subscription Engine is intended to provide an API to easily allow you to send customized emails with an
unsubscribe link.  It should have enough customization to allow it work with virtually any email provider.

## Requirements

1. Django 1.5+ (not tested with any earlier versions)
2. py.test - 2.6.3 (to run tests)
3. Django_helpers

## How to Use

1. Add the subscription_engine to your apps list
2. In your models:
    1. create a relationship between the model that owns the subscription and the subscription
3. In your views:
    1. When creating a model that has a subscription create the subscription first and add it to the model
        * The subscription will contain a name (name of subscription e.g. my newsletter, a randomly generated token for
        the subscription (used to create the unsubscribe link) and a status of the subscription (defaults to true)
4. Add the subscription_engine urls to your urls, if you need to you can change the view name of the unsubscribe url to
whatever your want however when you call send_email you will need to pass in the new name of the unsubscribe url, it defaults to unsubscribe.
5.  You will need 3 templates:
    * unsubscribe.html - The email template that contains the unsubscribe link code - see subscription_engine/tests/fixtures/templates for more examples
    * unsubscribe_confirmation.html - The confirmation page that the user is directed to after clicking the unsubscribe link
    * unsubscribe_error.html - The error page that the user is directed to after clicking the unsubscribe link and the link is incorrect.
6. Calling send_mail from your view will send the email with your unsubscribe wrapper attached.

## Running Tests

Run python runtest.py. This will run all of the tests with a limited django environment with just enough django for the tests to run.
