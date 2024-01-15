from django.contrib import admin
from .models import (
    Address,
    Country,
)

class AddressAdmin(admin.ModelAdmin):
    list_display = ['apartment', 'country']
    list_select_related = ['country']
        
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    ordering = ['name']
        
admin.site.register(Address, AddressAdmin)
admin.site.register(Country, CountryAdmin)