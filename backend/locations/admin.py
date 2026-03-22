from django.contrib import admin
from locations.models import Region,District,Ward

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'value','code', 'name','label']
    ordering = ['id']
    search_fields = ['code', 'name']
    
    
@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'value','code', 'name','label']
    ordering = ['id']
    search_fields = ['code', 'name']
    
    
    
@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ['id', 'value','code', 'name','label']
    ordering = ['id']
    search_fields = ['name']