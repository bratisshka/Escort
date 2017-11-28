from django.contrib import admin
from escort.app.models import Document, News


# Register your models here.
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('description', 'date_published')


admin.site.register(Document, DocumentAdmin)


class NewsAdmin(admin.ModelAdmin):
    list_display = ('header', 'date_published', 'own')
    list_filter = ('own',)
    ordering = ('date_published',)
    search_fields = ('header',)


admin.site.register(News, NewsAdmin)
