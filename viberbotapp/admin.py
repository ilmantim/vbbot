from django.contrib import admin

from viberbotapp.models import Mro, Person, Bill, Favorite


@admin.register(Mro)
class MroAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    pass


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass
