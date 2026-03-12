from django.db import models
from programs.models import LangChoices


class Partner(models.Model):
    logo = models.ImageField(upload_to='partners/', blank=True, null=True, verbose_name='Логотип')
    website_url = models.URLField(max_length=500, blank=True, verbose_name='Сайт')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлён')

    class Meta:
        db_table = 'partners'
        ordering  = ['sort_order']
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'

    def __str__(self):
        tr = self.translations.filter(lang='ru').first()
        return tr.name if tr else f'Партнёр #{self.id}'


class PartnerTranslation(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='translations', verbose_name='Партнёр')
    lang = models.CharField(max_length=5, choices=LangChoices.choices, verbose_name='Язык')
    name = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        db_table = 'partner_translations'
        unique_together = ('partner', 'lang')
        verbose_name = 'Перевод партнёра'
        verbose_name_plural = 'Переводы партнёров'

    def __str__(self):
        return f'{self.name} [{self.lang}]'