from django.conf.urls import url

from . import views as views

app_name = 'ndx_batch'

urlpatterns = (
    url(r'^$', views.BatchListView.as_view(), name='batches'),
    url(r'^(?P<pk>\d+)/$', views.BatchView.as_view(), name='batch'),
    url(r'^add/$', views.BatchCreateView.as_view(), name='batch-create'),
)
