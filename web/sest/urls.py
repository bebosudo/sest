from django.conf.urls import url

from . import views

app_name = 'sest'


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    # url(r'^(?P<pk>[0-9]+)/$', views.ChannelView.as_view(), name="channel"),
    url(r'^(?P<channel_id>[0-9]+)/$', views.channel, name="channel")
    # url(r'^(?P<channel_id>[0-9]+)/upload/$', views.upload, name="upload")
    #url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), title='results'),
    #url(r'^(?P<questio_id>[0-9]+)/vote/$', views.vote, title='vote'),
]
