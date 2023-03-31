from django.contrib import admin

from .models import Eula, EulaFile


class EulaFileAdmin(admin.TabularInline):
    model = EulaFile


class EulaAdmin(admin.ModelAdmin):
    inlines = (EulaFileAdmin,)


admin.site.register(Eula, EulaAdmin)