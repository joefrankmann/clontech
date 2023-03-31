from django.contrib import admin

from .models import Batch, QuadraticCurveParameters


class QuadraticCurveParametersAdmin(admin.TabularInline):
    model = QuadraticCurveParameters


class BatchAdmin(admin.ModelAdmin):
    inlines = (QuadraticCurveParametersAdmin,)


admin.site.register(Batch, BatchAdmin)
