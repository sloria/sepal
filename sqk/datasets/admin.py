from sqk.datasets.models import Dataset, Instance, Feature, Value, Species
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

class DatasetInline(admin.TabularInline):
    model = Dataset

class DatasetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'description', 'species',]}),
        ('Date information',{'fields': ['created_at'], 'classes': ['collapse']})
    ]
    list_display = ('name', 'created_at', 'description', 'pk')
    inlines = [InstanceInline, FeatureDatasetInline]
    search_fields = ['name']

class InstanceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['dataset',]}),
    ]
    list_display = ('dataset', 'pk')
    inlines = [FeatureInstanceInline, ValueInline]

class FeatureAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']})
    ]
    list_display = ('name','pk')
    inlines = [FeatureInstanceInline, FeatureDatasetInline]

class SpeciesAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']})
    ]
    list_display = ('name','pk')
    inlines = [DatasetInline]


admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Instance, InstanceAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Species, SpeciesAdmin)