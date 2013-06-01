import pytest
import os
from django.conf import settings

DIRNAME = os.path.dirname(__file__)
TEST_LOCATION = os.path.join(DIRNAME, 'tests')
test_command = "-x {test_location}".format(test_location=TEST_LOCATION)

settings.configure(
    DEBUG=True,
    SECRET_KEY='cj439m2vj3dgk3kd,2~dtrk3',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    ROOT_URLCONF='subscription_engine.urls',
    INSTALLED_APPS=('django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.admin',
                  'subscription_engine',
                  'subscription_engine.tests.fixtures',
                  ))

pytest.main(test_command)
