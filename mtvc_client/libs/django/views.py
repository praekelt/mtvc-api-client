from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator

from mtvc_client.client import APIClient
from mtvc_client.libs.django import utils
from mtvc_client.libs.django.forms import ProfileForm, ProductForm
from mtvc_client.libs.django.decorators import view_exception_handler


class TemplateViewBase(TemplateView):

    @method_decorator(view_exception_handler)
    def dispatch(self, *args, **kwargs):
        return super(TemplateViewBase, self).dispatch(*args, **kwargs)


class ChannelsView(TemplateViewBase):
    template_name = 'channels.html'

    def get_context_data(self, **kwargs):
        results = super(ChannelsView, self).get_context_data(**kwargs)
        page = utils.get_request_page_number(self.request)
        channels = utils.get_channel_list(page)
        results['meta'] = channels['meta']
        results['object_list'] = channels['objects']
        return results


class ShowsView(TemplateViewBase):
    template_name = 'shows.html'

    def get_context_data(self, **kwargs):
        results = super(ShowsView, self).get_context_data(**kwargs)
        page = utils.get_request_page_number(self.request)
        shows = utils.get_show_list(page)
        results['meta'] = shows['meta']
        results['object_list'] = shows['objects']
        return results


class ClipsView(TemplateViewBase):
    template_name = 'clips.html'

    def get_context_data(self, **kwargs):
        results = super(ClipsView, self).get_context_data(**kwargs)
        page = utils.get_request_page_number(self.request)
        clips = utils.get_clips_list(page)
        results['meta'] = clips['meta']
        results['object_list'] = clips['objects']
        return results


class ClipsFeaturedView(TemplateViewBase):
    template_name = 'clips.html'

    def get_context_data(self, **kwargs):
        results = super(ClipsFeaturedView, self).get_context_data(**kwargs)
        page = utils.get_request_page_number(self.request)
        clips = utils.get_featured_clips(page)
        results['meta'] = clips['meta']
        results['object_list'] = clips['objects']
        return results


class ClipsPopularView(TemplateViewBase):
    template_name = 'clips.html'

    def get_context_data(self, **kwargs):
        results = super(ClipsPopularView, self).get_context_data(**kwargs)
        page = utils.get_request_page_number(self.request)
        clips = utils.get_popular_clips(page)
        results['meta'] = clips['meta']
        results['object_list'] = clips['objects']
        return results


class ClipsByChannelView(TemplateViewBase):
    template_name = 'clips_list.xml'

    def get_context_data(self, **kwargs):
        show_channel = utils.get_showchannel(kwargs['slug'])
        if not show_channel:
            raise Http404

        results = super(ClipsByChannelView, self).get_context_data(**kwargs)
        page = utils.get_request_page_number(self.request)
        clips = utils.get_clips_by_channel(kwargs['slug'], page)
        results['meta'] = clips['meta']
        results['object_list'] = clips['objects']
        results['show_channel'] = show_channel
        return results


class ClipDetailView(TemplateViewBase):
    template_name = 'clip_detail.xml'

    def get_context_data(self, **kwargs):
        clip = utils.get_clip_detail(slug=kwargs['slug'])
        if not clip:
            raise Http404

        results = super(ClipDetailView, self).get_context_data(**kwargs)
        results['object'] = clip
        return results


class EPGView(TemplateViewBase):
    template_name = 'epg.html'

    def get_context_data(self, **kwargs):
        results = super(EPGView, self).get_context_data(**kwargs)
        results['object'] = utils.get_channel_epgs(self.kwargs['slug'])
        return results


class WatchView(TemplateViewBase):
    template_name = 'watch.html'

    def get_context_data(self, **kwargs):
        kwargs = super(WatchView, self).get_context_data(**kwargs)
        kwargs['object'] = APIClient(**settings.API_CLIENT).get_stream_url(
            self.kwargs['content_type'], self.kwargs['slug'],
            user_agent=utils.get_request_user_agent(self.request),
            msisdn=utils.get_request_msisdn(self.request),
            client_ip=utils.get_request_ip(self.request))
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
            msisdn=utils.get_request_msisdn(self.request),
            client_ip=utils.get_request_ip(self.request),
            data=form.get_json_data())
        return super(ProfileView, self).form_valid(form)


class ProductView(FormView):
    template_name = 'product_form.html'
    form_class = ProductForm
    success_url = '/'

    def form_valid(self, form):
        APIClient(**settings.API_CLIENT).post_transaction(
            user_agent=utils.get_request_user_agent(self.request),
            msisdn=utils.get_request_msisdn(self.request),
            client_ip=utils.get_request_ip(self.request),
            data=form.get_json_data())
        return super(ProductView, self).form_valid(form)


class AccountView(TemplateViewBase):
    template_name = 'account.html'

    def get_context_data(self, **kwargs):
        kwargs = super(AccountView, self).get_context_data(**kwargs)
        kwargs['object'] = APIClient(**settings.API_CLIENT).get_account_info(
            msisdn=utils.get_request_msisdn(self.request),
            client_ip=utils.get_request_ip(self.request))
        return kwargs
