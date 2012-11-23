from sqk.datasets.models import Dataset, Instance, Feature, Value, Label
from django.contrib import admin

class InstanceInline(admin.TabularInline):
    model = Instance
    extra = 1

class ValueInline(admin.TabularInline):
    model = Value
    extra = 1

class FeatureInstanceInline(admin.TabularInline):
    model = Feature.instances.through
    extra = 1

class FeatureDatasetInline(admin.TabularInline):
    model = Feature.datasets.through
    extra = 1

class DatasetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'description', 'source']}),
        ('Date information',{'fields': ['created_at'], 'classes': ['collapse']})
    ]
    list_display = ('name', 'created_at', 'description', 'source', 'pk')
    inlines = [InstanceInline, FeatureDatasetInline]
    search_fields = ['name']

class InstanceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'dataset', 'label']}),
    ]
    list_display = ('name','dataset', 'label', 'pk')
    inlines = [FeatureInstanceInline, ValueInline]
    search_fields = ['name']

class FeatureAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name',]})
    ]
    list_display = ('name', 'pk')
    inlines = [FeatureInstanceInline, FeatureDatasetInline]

class LabelAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['label',]})
    ]
    list_display = ('label', 'pk')
    inlines = [InstanceInline]

admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Instance, InstanceAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Label, LabelAdmin)