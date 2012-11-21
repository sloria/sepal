from sqk.datasets.models import Dataset, Instance, Feature
from django.contrib import admin

class InstanceInline(admin.TabularInline):
    model = Instance
    extra = 1

class DatasetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'description']}),
        ('Date information',{'fields': ['created_at'], 'classes': ['collapse']})
    ]
    list_display = ('name', 'created_at', 'description', 'pk')
    inlines = [InstanceInline]
    search_fields = ['name']

class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1

class InstanceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'dataset']}),
    ]
    list_display = ('name','dataset', 'pk')
    inlines = [FeatureInline]
    search_fields = ['name']

admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Instance, InstanceAdmin)