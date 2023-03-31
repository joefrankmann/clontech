from ndx_portal_source.urls import include, url, urlpatterns

urlpatterns += (
    url(r'^api/batch/', include('ndx_batch.api_urls', namespace='ndx-batch-api')),
    url(r'^batch/', include('ndx_batch.urls', namespace='ndx_batch')),
    url(r'^api/feedback/', include('ndx_feedback.api_urls', namespace="ndx_feedback_api")),
    url(r'^feedback/', include('ndx_feedback.urls', namespace='ndx_feedback'))
)
