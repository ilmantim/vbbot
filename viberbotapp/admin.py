from django.contrib import admin

from viberbotapp.models import Mro


@admin.register(Mro)
class MroAdmin(admin.ModelAdmin):
    pass