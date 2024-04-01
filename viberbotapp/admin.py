from django.contrib import admin

from viberbotapp.models import Mro, Person


@admin.register(Mro)
class MroAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass