from django.contrib import admin
from django.utils.html import format_html
from .models import Partner, PartnerTranslation


class PartnerTranslationInline(admin.TabularInline):
    model = PartnerTranslation
    extra = 3
    max_num = 3
    verbose_name = 'Перевод'
    verbose_name_plural = 'Переводы (RU / KG / EN)'
    fields = ['lang', 'name']


@admin.register(Partner)

class PartnerAdmin(admin.ModelAdmin):
    inlines       = [PartnerTranslationInline]
    list_display  = ['preview_logo', 'get_name', 'website_url', 'is_active', 'sort_order']
    list_editable = ['is_active', 'sort_order']
    readonly_fields = ['created_at', 'updated_at']
    ordering      = ['sort_order']

    fieldsets = [
        ('Основное', {
            'fields': ['logo', 'website_url', 'is_active', 'sort_order']
        }),
        ('Служебное', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]


    @admin.display(description='Название (RU)')
    def get_name(self, obj):
        tr = obj.translations.filter(lang='ru').first()
        return tr.name if tr else '—'


    @admin.display(description='Логотип')
    def preview_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:40px;object-fit:contain"/>', obj.logo.url)
        return '—'