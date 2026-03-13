from django.db import models


class LangChoices(models.TextChoices):
    RU = 'ru', 'Русский'
    KG = 'kg', 'Кыргызский'
    EN = 'en', 'English'


class ProgramType(models.TextChoices):
    ENACTUS = 'enactus', 'Enactus'
    HULT_PRIZE = 'hult_prize', 'Hult Prize'
    YBI = 'ybi',  'YBI'
    YOUTH_INITIATIVES = 'youth_initiatives', 'Молодёжные инициативы'


class Program(models.Model):
    slug = models.SlugField(max_length=300, unique=True, verbose_name='Слаг')
    program_type = models.CharField(max_length=50, choices=ProgramType.choices, verbose_name='Тип программы')
    image = models.ImageField(upload_to='programs/', blank=True, null=True, verbose_name='Изображение')
    is_active  = models.BooleanField(default=True, verbose_name='Активна')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')

    class Meta:
        db_table = 'programs'
        ordering = ['sort_order']
        verbose_name = 'Программа'
        verbose_name_plural = 'Программы'

    def __str__(self):
        tr = self.translations.filter(lang='ru').first()
        return tr.title if tr else self.slug


class ProgramTranslation(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='translations', verbose_name='Программа')
    lang = models.CharField(max_length=5, choices=LangChoices.choices, verbose_name='Язык')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Описание')
    content = models.TextField(blank=True, verbose_name='Контент')
    instruction = models.TextField(blank=True, verbose_name='Инструкция')
    meta_title = models.CharField(max_length=255, blank=True, verbose_name='Meta Title')
    meta_description = models.CharField(max_length=500, blank=True, verbose_name='Meta Description')

    class Meta:
        db_table = 'program_translations'
        unique_together = ('program', 'lang')
        verbose_name  = 'Перевод программы'
        verbose_name_plural  = 'Переводы программ'

    def __str__(self):
        return f'{self.title} [{self.lang}]'


class ProgramGallery(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='gallery', verbose_name='Программа')
    image = models.ImageField(upload_to='programs/gallery/', verbose_name='Изображение')
    caption = models.CharField(max_length=255, blank=True, verbose_name='Подпись')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        db_table = 'program_gallery'
        ordering = ['sort_order']
        verbose_name = 'Фото галереи'
        verbose_name_plural = 'Галерея'

    def __str__(self):
        return f'Фото #{self.sort_order} — {self.program}'


class ProgramTeam(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='teams', verbose_name='Программа')
    name = models.CharField(max_length=255, verbose_name='Название команды')
    university = models.CharField(max_length=255, blank=True, verbose_name='Университет')
    logo = models.ImageField(upload_to='programs/teams/', blank=True, null=True, verbose_name='Логотип')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        db_table = 'program_teams'
        ordering = ['sort_order']
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self):
        return self.name


class ProgramAdvisor(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='advisors', verbose_name='Программа')
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    position = models.CharField(max_length=255, blank=True, verbose_name='Должность')
    photo = models.ImageField(upload_to='programs/advisors/', blank=True, null=True, verbose_name='Фото')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        db_table = 'program_advisors'
        ordering = ['sort_order']
        verbose_name = 'Советник'
        verbose_name_plural = 'Советники'

    def __str__(self):
        return self.full_name


class ProgramTimeline(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='timeline', verbose_name='Программа')
    year = models.PositiveIntegerField(verbose_name='Год')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        db_table = 'program_timeline'
        ordering = ['sort_order']
        verbose_name = 'Этап таймлайна'
        verbose_name_plural = 'Таймлайн'

    def __str__(self):
        return f'{self.program} — {self.year}'


class ProgramTimelineTranslation(models.Model):
    timeline = models.ForeignKey(ProgramTimeline, on_delete=models.CASCADE, related_name='translations', verbose_name='Этап')
    lang = models.CharField(max_length=5, choices=LangChoices.choices, verbose_name='Язык')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        db_table = 'program_timeline_translations'
        unique_together = ('timeline', 'lang')
        verbose_name = 'Перевод этапа'
        verbose_name_plural = 'Переводы этапов'

    def __str__(self):
        return f'{self.title} [{self.lang}]'