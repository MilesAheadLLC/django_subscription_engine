from django.conf.urls import *
from subscription_engine.views import UnSubscribeView


urlpatterns = patterns(
    url(r'^(?P<model_id>\d*)-(?P<token>.*)/$',UnSubscribeView.as_view(),\
                                                name="unsubscribe"),
)