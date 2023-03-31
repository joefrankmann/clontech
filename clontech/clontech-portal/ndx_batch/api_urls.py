from django.conf.urls import url

from . import api_views as views

app_name = 'ndx_batch'

urlpatterns = (
    url(r'^active/$', views.ActiveBatchesView.as_view(), name='batches-active'),
)
