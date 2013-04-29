import pytest
import os, sys
from django.conf import settings

DIRNAME = os.path.dirname(__file__)
TEST_LOCATION = os.path.join(DIRNAME, 'tests.py')
test_command = "-x {test_location}".format(test_location=TEST_LOCATION)

settings.configure(DEBUG=True,
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
                              'subscription_engine',))




pytest.main(test_command)