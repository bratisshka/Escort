from django.contrib import admin
from escort.ocs.models import Task, SubTask


# Register your models here.
class SubtaskInline(admin.TabularInline):
    model = SubTask


class TaskAdmin(admin.ModelAdmin):
    inlines = (SubtaskInline,)


admin.site.register(Task, TaskAdmin)
