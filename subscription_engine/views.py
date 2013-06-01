from django.views.generic import TemplateView

class UnSubscribeView(TemplateView):
    template_name = 'unsubscribe_confirmation.html'

