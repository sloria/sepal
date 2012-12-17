from sqk.datasets.models import *
from django.contrib import admin

class InstanceInline(admin.TabularInline):
    model = Instance
    extra = 1

class FeatureValueInline(admin.TabularInline):
    model = FeatureValue
    extra = 1

class LabelValueInline(admin.TabularInline):
    model = LabelValue
    extra = 3

class FeatureInstanceInline(admin.TabularInline):
    model = Feature.instances.through
    extra = 1


class DatasetInline(admin.TabularInline):
    model = Dataset

class DatasetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'description', 'species',]}),
        ('Date information',{'fields': ['created_at'], 'classes': ['collapse']})
    ]
    list_display = ('name', 'created_at', 'description', 'pk')
    inlines = [InstanceInline,]
    search_fields = ['name']

class InstanceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['dataset',]}),
    ]
    list_display = ('dataset', 'pk')
    inlines = [FeatureInstanceInline, FeatureValueInline]

class FeatureAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name',]})
    ]
    list_display = ('name','pk')
    inlines = [FeatureInstanceInline,]

class LabelNameAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']})
    ]
    list_display = ('name','pk')
    inlines = [LabelValueInline]

class LabelValueAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['value', 'label_name']})
    ]
    list_display = ('value','pk')
    inlines = []

admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Instance, InstanceAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(LabelName, LabelNameAdmin)
admin.site.register(LabelValue, LabelValueAdmin)