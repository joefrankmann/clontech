from django.conf.urls import url
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView

from . import views as views

app_name = 'ndx_eula'

urlpatterns = (
    url(r'^$', RedirectView.as_view(url=reverse_lazy('ndx_eula:eulas'), permanent=True), name='index'),
    url(r'^eula/$', views.EulaListView.as_view(), name='eulas'),
    url(r'^eula/create/$', views.EulaCreateView.as_view(), name='eula-create'),
    url(r'^eula/(?P<pk>\d+)/$', views.EulaDetailView.as_view(), name='eula-detail'),
    url(r'^eula/edit/(?P<pk>\d+)$', views.EulaUpdateView.as_view(), name='eula-edit'),
    url(r'^eula/add-language/(?P<eula>\d+)$', views.EulaAddLanguageView.as_view(), name='eula-add-language'),
    url(r'^eula-file/edit/(?P<pk>\d+)$', views.EulaFileUpdateView.as_view(), name='eula-file-edit'),
    url(r'^eula-file/delete/(?P<pk>\d+)$', views.EulaFileDeleteView.as_view(), name='eula-file-delete'),
)
