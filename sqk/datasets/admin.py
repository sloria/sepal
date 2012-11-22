from sqk.datasets.models import Dataset, Instance, Feature, Value
from django.contrib import admin

class InstanceInline(admin.TabularInline):
    model = Instance
    extra = 1

class ValueInline(admin.TabularInline):
    model = Value
    extra = 1

class FeatureInline(admin.TabularInline):
    model = Feature.instances.through
    extra = 1

class DatasetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'description', 'source']}),
        ('Date information',{'fields': ['created_at'], 'classes': ['collapse']})
    ]
    list_display = ('name', 'created_at', 'description', 'source', 'pk')
    inlines = [InstanceInline]
    search_fields = ['name']

class InstanceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'dataset']}),
    ]
    list_display = ('name','dataset', 'pk')
    inlines = [FeatureInline, ValueInline]
    search_fields = ['name']

class FeatureAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name',]})
    ]
    list_display = ('name', 'pk')

admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Instance, InstanceAdmin)
admin.site.register(Feature, FeatureAdmin)