from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources

from .models import *
# Register your models here.

class ArtRegistrationResources(resources.ModelResource):
    # code = Field(attribute='code', column_name='Sector')
    class Meta:
        model = ArtRegistration
        import_id_fields = ('uuid',)

@admin.register(ArtRegistration)
class AdminArtRegistration(ImportExportActionModelAdmin,admin.ModelAdmin):
    search_fields = ['name_patient','uuid','pre_art_no']
    resource_class = ArtRegistrationResources
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]  

#=====================================
class ARTPatientLinkageResources(resources.ModelResource):
    # code = Field(attribute='code', column_name='Sector')
    class Meta:
        model = ARTPatientLinkage
        import_id_fields = ('uuid',)


@admin.register(ARTPatientLinkage)
class AdminARTPatientLinkage(ImportExportActionModelAdmin,admin.ModelAdmin):
    resource_class = ARTPatientLinkageResources
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]   

#StatusHistory
@admin.register(StatusHistory)
class AdminStatusHistory(ImportExportActionModelAdmin,admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]


class AnyIoResources(resources.ModelResource):
    # code = Field(attribute='code', column_name='Sector')
    class Meta:
        model = AnyIo
        import_id_fields = ('id',)



@admin.register(AnyIo)
class AdminAnyIo(ImportExportActionModelAdmin,admin.ModelAdmin):
    resource_class = AnyIoResources
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]  

class ARTVisitResources(resources.ModelResource):
    # code = Field(attribute='code', column_name='Sector')
    
    class Meta:
        model = ARTVisit
        import_id_fields = ('uuid',)

@admin.register(ARTVisit)
class AdminARTVisit(ImportExportActionModelAdmin,admin.ModelAdmin):
    resource_class = ARTVisitResources
    filter_horizontal = ('any_oi_uuid',)
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]          
