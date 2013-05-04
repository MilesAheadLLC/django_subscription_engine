from django.conf.urls import *

urlpatterns = patterns('unsubscribe.views',
    url(r'^(?P<user_id>\d*)-(?P<token>.*)/$', 'unsubscribe',\
                                                name="unsubscribe"),
)