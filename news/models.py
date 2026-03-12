from django.db import models
from programs.models import LangChoices


class NewsCategory(models.Model):
    slug       = models.SlugField(max_length=100, unique=True, verbose_name='Слаг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')

    class Meta:
        db_table            = 'news_categories'
        verbose_name        = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        tr = self.translations.filter(lang='ru').first()
        return tr.name if tr else self.slug


class NewsCategoryTranslation(models.Model):
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='translations', verbose_name='Категория')
    lang     = models.CharField(max_length=5, choices=LangChoices.choices, verbose_name='Язык')
    name     = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        db_table            = 'news_category_translations'
        unique_together     = ('category', 'lang')
        verbose_name        = 'Перевод категории'
        verbose_name_plural = 'Переводы категорий'

    def __str__(self):
        return f'{self.name} [{self.lang}]'


class News(models.Model):
    slug         = models.SlugField(max_length=255, unique=True, verbose_name='Слаг')
    category     = models.ForeignKey(
        NewsCategory, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='news', verbose_name='Категория'
    )
    cover        = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name='Обложка')
    is_published = models.BooleanField(default=False, verbose_name='Опубликована')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата публикации')
    created_at   = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at   = models.DateTimeField(auto_now=True, verbose_name='Обновлена')

    class Meta:
        db_table            = 'news'
        ordering            = ['-published_at']
        verbose_name        = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        tr = self.translations.filter(lang='ru').first()
        return tr.title if tr else self.slug


class NewsTranslation(models.Model):
    news             = models.ForeignKey(News, on_delete=models.CASCADE, related_name='translations', verbose_name='Новость')
    lang             = models.CharField(max_length=5, choices=LangChoices.choices, verbose_name='Язык')
    title            = models.CharField(max_length=255, verbose_name='Заголовок')
    excerpt          = models.TextField(blank=True, verbose_name='Краткое описание')
    content          = models.TextField(blank=True, verbose_name='Контент')
    meta_title       = models.CharField(max_length=255, blank=True, verbose_name='Meta Title')
    meta_description = models.CharField(max_length=500, blank=True, verbose_name='Meta Description')

    class Meta:
        db_table            = 'news_translations'
        unique_together     = ('news', 'lang')
        verbose_name        = 'Перевод новости'
        verbose_name_plural = 'Переводы новостей'

    def __str__(self):
        return f'{self.title} [{self.lang}]'