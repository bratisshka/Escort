from django.contrib import admin
from .models import Module, Dependancy


class ModuleInlineAdmin(admin.TabularInline):
    model = Dependancy
    fk_name = 'input_module'
    extra = 3

# Register your models here.
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    fields = ('name', 'description', ('periodic', 'timeout', 'state'))
    list_display = ['name', 'state', 'purpose']
    ordering = ['name']
    #filter_horizontal = ['output_modules']
    inlines = (ModuleInlineAdmin,)

