from ndx_feedback.models import Feedback
from rest_framework import serializers


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = (
            "id", "uploader_email", "created_at", "device_os", "device_make", "device_model", "device_id", "app_version",
            "reader_type", "reader_version", "rating", "follow_up", "comments"
        )
