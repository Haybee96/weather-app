from django.contrib import admin
from . models import City

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    list_display_links = ('name',)
    list_per_page = 20
    search_fields = ('name',)

admin.site.register(City, CityAdmin)
