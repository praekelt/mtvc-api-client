from django.conf import settings
from django.views.generic import TemplateView

from client import APIClient


class ChannelsView(TemplateView):
    template_name = 'smart/channels.html'

    def get_context_data(self, **kwargs):
        kwargs = super(ChannelsView, self).get_context_data(**kwargs)
        kwargs['object_list'] = APIClient(**settings.API_CLIENT).get_channels()
        return kwargs


class EPGView(TemplateView):
    template_name = 'smart/epg.html'

    def get_context_data(self, **kwargs):
        kwargs = super(EPGView, self).get_context_data(**kwargs)
        kwargs['object'] = APIClient(**settings.API_CLIENT).get_epg(self.kwargs['slug'])
        return kwargs


class WatchView(TemplateView):
    template_name = 'smart/watch.html'

    def get_context_data(self, **kwargs):
        kwargs = super(WatchView, self).get_context_data(**kwargs)
        kwargs['object'] = APIClient(**settings.API_CLIENT).get_watch(self.kwargs['slug'])
        return kwargs


class HelpView(TemplateView):
    template_name = 'smart/help.html'


class AccountView(TemplateView):
    template_name = 'smart/account.html'

    def get_context_data(self, **kwargs):
        kwargs = super(AccountView, self).get_context_data(**kwargs)
        kwargs['object'] = APIClient(**settings.API_CLIENT).get_account_info(
            self.request.META.get('HTTP_X_MSISDN', None))
        return kwargs

