from django.db import models


class SiteSettings(models.Model):
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True, blank=True,
        verbose_name='Аватарка',
    )

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return 'Настройки сайта'

    def save(self, *args, **kwargs):
        self.pk = 1  # singleton
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Translation(models.Model):
    language = models.CharField(max_length=10, verbose_name='Язык')
    key = models.CharField(max_length=200, verbose_name='Ключ')
    value = models.TextField(verbose_name='Значение')

    class Meta:
        unique_together = ('language', 'key')
        ordering = ['language', 'key']
        verbose_name = 'Перевод'
        verbose_name_plural = 'Переводы интерфейса'

    def __str__(self):
        return f'[{self.language}] {self.key}'


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название тега')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Project(models.Model):
    slug = models.SlugField(max_length=100, unique=True, verbose_name='ID (slug)')
    url = models.URLField(verbose_name='Ссылка')
    link_type = models.CharField(
        max_length=100, verbose_name='Тип ссылки',
        help_text='Например: GitHub Repository, Website',
    )
    preview = models.CharField(
        max_length=300, blank=True, verbose_name='Превью (старый путь)',
        help_text='Автозаполняется при импорте. Используй поле ниже для загрузки.',
    )
    preview_image = models.ImageField(
        upload_to='projects/', null=True, blank=True,
        verbose_name='Превью (загрузить)',
        help_text='Загруженное изображение имеет приоритет над старым путём.',
    )
    is_mobile_app = models.BooleanField(default=False, verbose_name='Мобильное приложение')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    tags = models.ManyToManyField('Tag', blank=True, related_name='projects', verbose_name='Теги')

    class Meta:
        ordering = ['order']
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.slug


class ProjectScreenshot(models.Model):
    project = models.ForeignKey(
        Project, related_name='screenshots',
        on_delete=models.CASCADE, verbose_name='Проект',
    )
    image = models.CharField(
        max_length=300, blank=True, verbose_name='Изображение (старый путь)',
    )
    image_file = models.ImageField(
        upload_to='screenshots/', null=True, blank=True,
        verbose_name='Изображение (загрузить)',
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Скриншот'
        verbose_name_plural = 'Скриншоты'

    def __str__(self):
        return f'{self.project.slug} – скриншот {self.order}'


class ProjectScreenshotTranslation(models.Model):
    screenshot = models.ForeignKey(
        ProjectScreenshot, related_name='translations',
        on_delete=models.CASCADE, verbose_name='Скриншот',
    )
    language = models.CharField(max_length=10, verbose_name='Язык')
    title = models.CharField(max_length=300, verbose_name='Название', blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)

    class Meta:
        unique_together = ('screenshot', 'language')
        verbose_name = 'Перевод скриншота'
        verbose_name_plural = 'Переводы скриншотов'

    def __str__(self):
        title_suffix = f': "{self.title}"' if self.title else ''
        return f'[{self.language}] Скриншот {self.screenshot.order} ({self.screenshot.project.slug}){title_suffix}'



class ProjectTranslation(models.Model):
    project = models.ForeignKey(
        Project, related_name='translations',
        on_delete=models.CASCADE, verbose_name='Проект',
    )
    language = models.CharField(max_length=10, verbose_name='Язык')
    title = models.CharField(max_length=300, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        unique_together = ('project', 'language')
        verbose_name = 'Перевод проекта'
        verbose_name_plural = 'Переводы проектов'

    def __str__(self):
        return f'[{self.language}] {self.project.slug}'
