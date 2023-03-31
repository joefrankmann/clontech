from django.conf.urls import url

from . import views as views

app_name = 'ndx_feedback'

urlpatterns = (
    url(r'^$', views.FeedbackListView.as_view(), name='feedback'),
    url(r'^(?P<pk>\d+)/$', views.FeedbackDetailView.as_view(), name='feedback-detail'),
    url(r'^data_source/$', views.FeedbackAjaxListView.as_view(), name='feedback-data-source')
)
