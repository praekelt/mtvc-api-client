from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator

from client import APIClient
from utils import get_request_msisdn, get_request_ip, get_request_user_agent
from forms import ProfileForm, ProductForm
from decorators import view_exception_handler


class TemplateViewBase(TemplateView):

    @method_decorator(view_exception_handler)
    def dispatch(self, *args, **kwargs):
        return super(TemplateViewBase, self).dispatch(*args, **kwargs)


class ChannelsView(TemplateViewBase):
    template_name = 'channels.html'

    def get_context_data(self, **kwargs):
        kwargs = super(ChannelsView, self).get_context_data(**kwargs)
        kwargs['object_list'] = APIClient(**settings.API_CLIENT).get_channels()
        return kwargs


class ShowsView(TemplateViewBase):
    template_name = 'shows.html'

    def get_context_data(self, **kwargs):
        kwargs = super(ShowsView, self).get_context_data(**kwargs)
        kwargs['object_list'] = APIClient(**settings.API_CLIENT).get_shows()
        return kwargs


class ClipsView(TemplateViewBase):
    template_name = 'clips.html'

    def get_context_data(self, **kwargs):
        kwargs = super(ClipsView, self).get_context_data(**kwargs)
        kwargs['object_list'] = APIClient(**settings.API_CLIENT).get_clips()
        return kwargs


class EPGView(TemplateViewBase):
    template_name = 'epg.html'

    def get_context_data(self, **kwargs):
        kwargs = super(EPGView, self).get_context_data(**kwargs)
        kwargs['object'] = APIClient(**settings.API_CLIENT).get_epg(
            self.kwargs['slug'])
        return kwargs


class WatchView(TemplateViewBase):
    template_name = 'watch.html'

    def get_context_data(self, **kwargs):
        kwargs = super(WatchView, self).get_context_data(**kwargs)
        kwargs['object'] = APIClient(**settings.API_CLIENT).get_stream_url(
            self.kwargs['content_type'], self.kwargs['slug'],
            user_agent=get_request_user_agent(self.request),
            msisdn=get_request_msisdn(self.request),
            client_ip=get_request_ip(self.request))
        return kwargs


class HelpView(TemplateViewBase):
    template_name = 'help.html'


class HandsetNotSupportedView(TemplateViewBase):
    template_name = 'handset_not_supported.html'

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['status'] = 412
        return super(HandsetNotSupportedView, self).render_to_response(
            context, **response_kwargs)


class ProfileView(FormView):
    template_name = 'profile_form.html'
    form_class = ProfileForm
    success_url = '/'

    def form_valid(self, form):
        APIClient(**settings.API_CLIENT).post_profile(
            msisdn=get_request_msisdn(self.request),
            client_ip=get_request_ip(self.request),
            data=form.get_json_data())
        return super(ProfileView, self).form_valid(form)


class ProductView(FormView):
    template_name = 'product_form.html'
    form_class = ProductForm
    success_url = '/'

    def form_valid(self, form):
        APIClient(**settings.API_CLIENT).post_transaction(
            user_agent=get_request_user_agent(self.request),
            msisdn=get_request_msisdn(self.request),
            client_ip=get_request_ip(self.request),
            data=form.get_json_data())
        return super(ProductView, self).form_valid(form)


class AccountView(TemplateViewBase):
    template_name = 'account.html'

    def get_context_data(self, **kwargs):
        kwargs = super(AccountView, self).get_context_data(**kwargs)
        kwargs['object'] = APIClient(**settings.API_CLIENT).get_account_info(
            msisdn=get_request_msisdn(self.request),
            client_ip=get_request_ip(self.request))
        return kwargs
