import os

from fabric.api import task, lcd, local

subscription_engine_path = os.path.split(os.path.realpath(os.path.dirname(__file__)))[0] #django_subscription_engine/subscription_engine

@task
def all():
    '''
        Run all tests using the django environment provided by runtest.py

        usage: fab all
    '''
    print subscription_engine_path
    with lcd(subscription_engine_path):
        local('python runtest.py')