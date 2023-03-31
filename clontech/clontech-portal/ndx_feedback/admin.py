from django.contrib import admin
from ndx_feedback.models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    model = Feedback


admin.site.register(Feedback, FeedbackAdmin)
