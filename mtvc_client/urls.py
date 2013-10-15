from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
    url(r'^$', views.ChannelsView.as_view(), name='home'),
    url(r'^channel/(?P<slug>[\w-]+)/$', views.EPGView.as_view(), name='epg'),
    url(r'^channel/(?P<slug>[\w-]+)/watch/$', views.WatchView.as_view(), name='watch'),
    url(r'^help/$', views.HelpView.as_view(), name='help'),
    url(r'^account/$', views.AccountView.as_view(), name='account'),
)
