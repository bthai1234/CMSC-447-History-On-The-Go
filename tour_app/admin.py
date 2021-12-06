from django.contrib import admin
from .models import Itinerary, Itinerary_location


class Itinerary_locationInline(admin.StackedInline):
    model = Itinerary_location
    extra = 0

# Register your models here.
class ItineraryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'itinerary_name']}),
    ]
    inlines = [Itinerary_locationInline]


admin.site.register(Itinerary, ItineraryAdmin)

