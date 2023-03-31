from django.conf.urls import url, include

from rest_framework import routers

from ndx_feedback import api_views as views

app_name = 'ndx_feedback_api'

router = routers.DefaultRouter()
router.register(r'', views.FeedbackViewSet)

urlpatterns = (
    url(r'^', include(router.urls), name='feedback'),
    url(r'csv', views.feedback_csv_view, name='feedback_csv')
)
