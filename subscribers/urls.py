from . import views
from django.conf.urls import url


urlpatterns = [

    url(r'^(?P<page_number>\d+)/$', views.home, name='home'),
    url(r'^detail/(?P<pk>\d+)/$', views.PersonDetail.as_view(), name='detail'),
    url(r'add/$', views.PersonCreate.as_view(), name='add'),
    url(r'new-number/$', views.NewPhoneCreate.as_view(), name='new-number'),
    url(r'update/(?P<pk>\d+)/$', views.PersonUpdate.as_view(), name='update'),
    url(r'delete/(?P<pk>\d+)/$', views.PersonDelete.as_view(), name='delete'),
    url(r'^$', views.home, name='home'),


]
