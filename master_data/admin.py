from django.contrib import admin
from .models import *
from import_export.admin import ImportExportActionModelAdmin


# Register your models here.

@admin.register(Boundary)
class AdminBoundary(ImportExportActionModelAdmin,admin.ModelAdmin):
    list_filter = ["boundary_level","parent__name"]
    search_fields = ["name"]
    exclude = ('latitude','longitude')
    filter_horizontal = ('sacep',)
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

@admin.register(MasterLookUp)
class AdminMasterLookUp(ImportExportActionModelAdmin,admin.ModelAdmin):
    list_filter = ["parent__name"]
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]



@admin.register(BoundaryLevel)
class AdminBoundaryLevel(ImportExportActionModelAdmin,admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]


@admin.register(Sacepconfig)
class AdminSacepconfig(ImportExportActionModelAdmin,admin.ModelAdmin):
    # list_filter = [ 'art_center','sacep']
    search_fields = ["art_center__name",'sacep__name']
    exclude = ('deactivation_date',)
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "sacep":
            '''In Sacep only Sacep(5) and ART Center Should List'''
            kwargs["queryset"] = Boundary.objects.filter(boundary_level__code__in=[5,3])
        elif db_field.name == "art_center":
            kwargs["queryset"] = Boundary.objects.filter(boundary_level__code__in=[3])
        return super(AdminSacepconfig, self).formfield_for_foreignkey(db_field, request, **kwargs)