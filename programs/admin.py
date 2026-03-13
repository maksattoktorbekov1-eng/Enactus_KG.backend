from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Program, ProgramTranslation, ProgramGallery,
    ProgramTeam, ProgramAdvisor,
    ProgramTimeline, ProgramTimelineTranslation,
)


class ProgramTranslationInline(admin.TabularInline):
    model = ProgramTranslation
    extra = 3
    max_num = 3
    verbose_name = 'Перевод'
    verbose_name_plural = 'Переводы (RU / KG / EN)'
    fields = ['lang', 'title', 'description', 'content', 'instruction', 'meta_title', 'meta_description']


class ProgramGalleryInline(admin.TabularInline):
    model = ProgramGallery
    extra = 1
    verbose_name = 'Фото'
    verbose_name_plural = 'Галерея'
    fields = ['image', 'caption', 'sort_order']


class ProgramTeamInline(admin.TabularInline):
    model = ProgramTeam
    extra = 1
    verbose_name = 'Команда'
    verbose_name_plural = 'Команды'
    fields = ['name', 'university', 'logo', 'is_active', 'sort_order']


class ProgramAdvisorInline(admin.TabularInline):
    model = ProgramAdvisor
    extra = 1
    verbose_name = 'Советник'
    verbose_name_plural = 'Советники'
    fields = ['full_name', 'position', 'photo', 'sort_order']


class ProgramTimelineTranslationInline(admin.TabularInline):
    model = ProgramTimelineTranslation
    extra = 3
    max_num = 3
    verbose_name = 'Перевод'
    verbose_name_plural = 'Переводы (RU / KG / EN)'
    fields = ['lang', 'title', 'description']


@admin.register(ProgramTimeline)
class ProgramTimelineAdmin(admin.ModelAdmin):
    inlines = [ProgramTimelineTranslationInline]
    list_display = ['program', 'year', 'sort_order']
    list_editable = ['sort_order']
    ordering = ['sort_order']
    verbose_name = 'Этап таймлайна'
    verbose_name_plural = 'Таймлайн'


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    inlines = [
        ProgramTranslationInline,
        ProgramGalleryInline,
        ProgramTeamInline,
        ProgramAdvisorInline,
    ]

    list_display = ['preview_image', 'get_title', 'program_type', 'is_active', 'sort_order', 'updated_at']
    list_editable = ['is_active', 'sort_order']
    list_filter = ['program_type', 'is_active']
    search_fields = ['slug', 'translations__title']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    ordering = ['sort_order']

    fieldsets = [
        ('Основное', {
            'fields': ['slug', 'program_type', 'image', 'is_active', 'sort_order']
        }),
        ('Служебное', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]

    @admin.display(description='Название (RU)')
    def get_title(self, obj):
        tr = obj.translations.filter(lang='ru').first()
        return tr.title if tr else '—'

    @admin.display(description='Фото')
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px"/>', obj.image.url)
        return '—'