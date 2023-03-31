from ndx_result_source.urls import *  # noqa
import ndx_result_source.urls as source  # noqa
from django.conf.urls import url
from ndx_result_source.urls import urlpatterns

from ndx_result import views

urlpatterns += (
    url(r'^result_csv_download/$', views.ResultCsvDownloadView.as_view(), name='result-csv-download'),
) 
