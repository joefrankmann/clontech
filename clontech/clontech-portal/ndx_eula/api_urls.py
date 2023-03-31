from django.conf.urls import url

from . import api_views as views

app_name = 'ndx_eula'


urlpatterns = [
    url(r'^current$', views.CurrentEulaView.as_view(), name='current-eula'),
]
