from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.cache import cache

from mtvc_client.client import APIClient


def get_request_msisdn(request):
    try:
        return request.META.get(settings.MSISDN_HEADER, '')
    except AttributeError:
        raise ImproperlyConfigured(
            'Missing setting MSISDN_HEADER in the settings file')


def get_request_ip(request):
    try:
        return request.META.get(settings.CLIENT_IP_HEADER, '')
    except AttributeError:
        raise ImproperlyConfigured(
            'Missing setting CLIENT_IP_HEADER in the settings file')


def get_request_user_agent(request):
    return request.META.get('HTTP_USER_AGENT', '')


def get_request_referer(request):
    """
    Returns the HTTP referer header of the request, defaults to ''
    """
    return request.META.get('HTTP_REFERER', '')


def get_request_page_number(request):
    """
    Returns the page number in the request.

    Defaults to 1.
    """
    return int(request.GET.get('page', 1))


def get_response_paginator(request, meta):
    """
    Returns a paginator for the response meta-data given the request.
    """
    # calculate number of pages
    pages = meta['total_count'] / meta['limit']

    # add a page for the remainder
    if meta['total_count'] % meta['limit']:
        pages += 1

    current_page = (meta['offset'] / meta['limit']) + 1

    return {
        'pages': [{
            'current': page == current_page,
            'index': page,
            'url': '%s?page=%s' % (request.path_info, page)
        } for page in range(1, pages + 1)]
    }


def get_cached_api_response(key, timeout, fn, **fn_kwargs):
    """
    Returns an API response from cache, if available, else updates
    the cache
    """
    results = cache.get(key)
    if not results:
        results = fn(**fn_kwargs)
        cache.set(key, results, timeout)
    return results


def get_profile_schema(timeout=60 * 60 * 24):
    """
    Returns the schema for a subscriber profile form, cached for 24
    hours by default
    """
    return get_cached_api_response(
        'PROFILE-SCHEMA', timeout,
        APIClient(**settings.API_CLIENT).get_profile_schema)


def get_transaction_schema(timeout=60 * 60 * 24):
    """
    Returns the schema for a subscriber transaction form, cached for 24
    hours by default
    """
    return get_cached_api_response(
        'TRANSACTION-SCHEMA', timeout,
        APIClient(**settings.API_CLIENT).get_transaction_schema)


def get_channel_list(page=1, results_per_page=30, timeout=60):
    """
    Returns a channel list, by default cached for 60 seconds.
    """
    return get_cached_api_response(
        'CHANNELS', timeout, APIClient(**settings.API_CLIENT).get_channels,
        limit=results_per_page, offset=(page - 1) * results_per_page)


def get_clips_list(page=1, results_per_page=5, timeout=60 * 5):
    """
    Returns a clips list, by default cached for 5 minutes.
    """
    return get_cached_api_response(
        'CLIPS', timeout, APIClient(**settings.API_CLIENT).get_clips,
        limit=results_per_page, offset=(page - 1) * results_per_page)


def get_featured_clips(page=1, results_per_page=5, timeout=60 * 5):
    """
    Returns a list of featured clips for the page number specified.

    Results for the page are cached for 5 minutes by default.
    """
    return get_cached_api_response(
        'CLIPS:::FEATURED:::%d' % page, timeout,
        APIClient(**settings.API_CLIENT).get_clips, featured=True,
        limit=results_per_page, offset=(page - 1) * results_per_page)


def get_popular_clips(page=1, results_per_page=5, timeout=60 * 5):
    """
    Returns a list of the popular clips for the page number specified.

    Results for the page are cached for 5 minutes by default.
    """
    return get_cached_api_response(
        'CLIPS:::POPULAR:::%d' % page, timeout,
        APIClient(**settings.API_CLIENT).get_clips,
        order_by='-stream_requests', limit=results_per_page,
        offset=(page - 1) * results_per_page)


def get_clips_by_channel(slug, page=1, results_per_page=5, timeout=60 * 5):
    """
    Returns a list of the clips, filtered by channel slug, for the page
    number specified.

    Results for the page are cached for 5 minutes by default.
    """
    return get_cached_api_response(
        'CLIPS:::CHANNEL:::%s' % slug, timeout,
        APIClient(**settings.API_CLIENT).get_clips,
        show__show_channel__slug__exact=slug, limit=results_per_page,
        offset=(page - 1) * results_per_page)


def get_clip_detail(slug, timeout=60 * 5):
    """
    Looks up and returns a clip by slug.

    Returns None if no clip was found.

    The result (possibly None) is cached for 5 minutes by default.
    """
    result = get_cached_api_response(
        'CLIP:::%s' % slug, timeout,
        APIClient(**settings.API_CLIENT).get_clips,
        slug__exact=slug)

    if result and 'objects' in result and result['objects']:
        return result['objects'][0]
    else:
        return None


def get_shows(timeout=60 * 5):
    """
    Returns a clip show list, cached for 5 minutes by default
    """
    return get_cached_api_response(
        'SHOWS', timeout, APIClient(**settings.API_CLIENT).get_shows)


def get_showchannels(timeout=60 * 5):
    """
    Returns a list of clip show channels, cached for 5 minutes by default
    """
    return get_cached_api_response(
        'SHOWCHANNELS', timeout,
        APIClient(**settings.API_CLIENT).get_showchannels)


def get_showchannel(slug, timeout=60 * 5):
    """
    Looks up and returns a clip show channel by slug.

    Returns None if no clip show channel was found.

    The result (possibly None) is cached for 5 minutes by default.
    """
    result = get_cached_api_response(
        'SHOWCHANNEL:::%s' % slug, timeout,
        APIClient(**settings.API_CLIENT).get_showchannels, slug__exact=slug)

    if result and 'objects' in result and result['objects']:
        return result['objects'][0]
    else:
        return None


def get_channel_epgs(slug, timeout=60 * 5):
    """
    Returns a list of EPGs for the channel identified by slug.

    The result is cached for 5 minutes by default
    """
    return get_cached_api_response(
        'CHANNEL-EPG:::%s' % slug, timeout,
        APIClient(**settings.API_CLIENT).get_epg, slug=slug)


def get_gender_choices():
    schema = get_profile_schema()
    return [['', '---------']] + schema['fields']['gender']['choices']


def get_region_choices():
    schema = get_profile_schema()
    return [['', '---------']] + schema['fields']['region']['choices']


def get_product_choices():
    schema = get_transaction_schema()
    return schema['fields']['product_name']['choices']
