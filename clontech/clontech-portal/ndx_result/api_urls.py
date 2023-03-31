from ndx_result_source.api_urls import *  # noqa
import ndx_result_source.api_urls as source  # noqa
from ndx_result_source.api_urls import urlpatterns

from django.conf.urls import url
from ndx_result import api_views as views 

urlpatterns += (
    url(r'csv', views.result_csv_view, name="api_result_csv"),
)
