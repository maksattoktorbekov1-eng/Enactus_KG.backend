from django.contrib import admin
from django.utils.html import format_html
from .models import News, NewsTranslation, NewsCategory, NewsCategoryTranslation


class NewsTranslationInline(admin.TabularInline):
    model = NewsTranslation
    extra = 3
    max_num = 3
    verbose_name = 'Перевод'
    verbose_name_plural = 'Переводы (RU / KG / EN)'
    fields = ['lang', 'title', 'excerpt', 'content', 'meta_title', 'meta_description']


class NewsCategoryTranslationInline(admin.TabularInline):
    model = NewsCategoryTranslation
    extra = 3
    max_num = 3
    verbose_name = 'Перевод'
    verbose_name_plural = 'Переводы (RU / KG / EN)'
    fields = ['lang', 'name']


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    inlines = [NewsCategoryTranslationInline]
    list_display = ['get_name', 'slug', 'created_at']
    readonly_fields = ['created_at']

    @admin.display(description='Название (RU)')
    def get_name(self, obj):
        tr = obj.translations.filter(lang='ru').first()
        return tr.name if tr else obj.slug


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsTranslationInline]
    list_display = ['preview_cover', 'get_title', 'category', 'is_published', 'published_at']
    list_editable = ['is_published']
    list_filter = ['is_published', 'category']
    search_fields = ['slug', 'translations__title']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    ordering = ['-published_at']

    fieldsets = [
        ('Основное', {
            'fields': ['slug', 'cover', 'category', 'is_published', 'published_at']
        }),
        ('Служебное', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]

    @admin.display(description='Заголовок (RU)')
    def get_title(self, obj):
        tr = obj.translations.filter(lang='ru').first()
        return tr.title if tr else '—'

    @admin.display(description='Обложка')
    def preview_cover(self, obj):
        if obj.cover:
            return format_html('<img src="{}" style="height:40px;border-radius:4px"/>', obj.cover.url)
        return '—'