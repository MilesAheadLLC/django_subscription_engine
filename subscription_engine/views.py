from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.shortcuts import render_to_response

from subscription_engine.models import SubscriptionAssignment

class UnSubscribeView(View):
    template_name='unsubscribe_confirmation.html'
    error_template='unsubscribe_error.html'

    def get(self, request, *args, **kwargs):
        try:
            sub = SubscriptionAssignment.objects.get(token=kwargs['token'])
            sub.active = False
            sub.save()
        except ObjectDoesNotExist:
            return render_to_response(self.error_template)

        return render_to_response(self.template_name,)


