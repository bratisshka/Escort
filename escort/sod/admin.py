from django.contrib import admin
from .models import Module


# Register your models here.
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    fields = ('name', 'description', ('periodic', 'timeout', 'state'), 'output_modules')
    list_display = ['name', 'state', 'purpose']
    ordering = ['name']
    filter_horizontal = ['output_modules']