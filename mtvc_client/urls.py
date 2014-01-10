from django.conf.urls import patterns, url

import views


urlpatterns = patterns(
    '',
    url(r'^$', views.ChannelsView.as_view(), name='home'),
    url(r'^channel/$', views.ChannelsView.as_view(), name='channels'),
    url(r'^channel/(?P<slug>[\w-]+)/$', views.EPGView.as_view(), name='epg'),
    url(r'^show/$', views.ShowsView.as_view(), name='shows'),
    url(r'^clip/$', views.ClipsView.as_view(), name='clips'),
    url(r'^(?P<content_type>channel|clip)/(?P<slug>[\w-]+)/watch/$',
        views.WatchView.as_view(), name='watch'),
    url(r'^help/$', views.HelpView.as_view(), name='help'),
    url(r'^account/$', views.AccountView.as_view(), name='account'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^product/$', views.ProductView.as_view(), name='product'),
    url(r'^handset-not-supported/$', views.HandsetNotSupportedView.as_view(), name='handset-not-supported'),
)
