from django.contrib import admin

from worker.models import Airport, Destination


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')
    fields = ('code', 'name')


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('id', 'fly_from', 'fly_to')
    fields = ('fly_from', 'fly_to')
