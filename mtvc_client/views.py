from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from client import APIClient
from utils import get_request_msisdn, get_request_ip, get_request_user_agent
from forms import ProfileForm, ProductForm


class ChannelsView(TemplateView):
    template_name = 'smart/channels.html'

    def get_context_data(self, **kwargs):
        kwargs = super(ChannelsView, self).get_context_data(**kwargs)
        kwargs['object_list'] = APIClient(**settings.API_CLIENT).get_channels()
        return kwargs


class ShowsView(TemplateView):
    template_name = 'smart/shows.html'

    def get_context_data(self, **kwargs):
        kwargs = super(ShowsView, self).get_context_data(**kwargs)
        kwargs['object_list'] = APIClient(**settings.API_CLIENT).get_shows()
        return kwargs


class ClipsView(TemplateView):
    template_name = 'smart/clips.html'

    def get_context_data(self, **kwargs):
        kwargs = super(ClipsView, self).get_context_data(**kwargs)
        kwargs['object_list'] = APIClient(**settings.API_CLIENT).get_clips()
        return kwargs


class EPGView(TemplateView):
    template_name = 'smart/epg.html'

    def get_context_data(self, **kwargs):
        kwargs = super(EPGView, self).get_context_data(**kwargs)
        kwargs['object'] = APIClient(**settings.API_CLIENT).get_epg(
            self.kwargs['slug'])
        return kwargs


class WatchView(TemplateView):
    template_name = 'smart/watch.html'

    def get_context_data(self, **kwargs):
        kwargs = super(WatchView, self).get_context_data(**kwargs)
        kwargs['object'] = APIClient(**settings.API_CLIENT).get_stream_url(
            self.kwargs['content_type'], self.kwargs['slug'],
            user_agent=get_request_user_agent(self.request),
            msisdn=get_request_msisdn(self.request),
            client_ip=get_request_ip(self.request))
        return kwargs


class HelpView(TemplateView):
    template_name = 'smart/help.html'


class ProfileView(FormView):
    template_name = 'smart/profile_form.html'
    form_class = ProfileForm
    success_url = '/'

    def form_valid(self, form):
        APIClient(**settings.API_CLIENT).post_profile(
            msisdn=get_request_msisdn(self.request),
            client_ip=get_request_ip(self.request),
            data=form.get_json_data())
        return super(ProfileView, self).form_valid(form)


class ProductView(FormView):
    template_name = 'smart/product_form.html'
    form_class = ProductForm
    success_url = '/'

    def form_valid(self, form):
        APIClient(**settings.API_CLIENT).post_transaction(
            user_agent=get_request_user_agent(self.request),
            msisdn=get_request_msisdn(self.request),
            client_ip=get_request_ip(self.request),
            data=form.get_json_data())
        return super(ProductView, self).form_valid(form)


class AccountView(TemplateView):
    template_name = 'smart/account.html'

    def get_context_data(self, **kwargs):
        kwargs = super(AccountView, self).get_context_data(**kwargs)
        kwargs['object'] = APIClient(**settings.API_CLIENT).get_account_info(
            msisdn=get_request_msisdn(self.request),
            client_ip=get_request_ip(self.request))
        return kwargs
