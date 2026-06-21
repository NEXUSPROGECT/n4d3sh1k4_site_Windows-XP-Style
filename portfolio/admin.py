from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import SiteSettings, Translation, Project, ProjectScreenshot, ProjectTranslation, ProjectScreenshotTranslation, Tag


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fields = ['avatar', 'avatar_preview']
    readonly_fields = ['avatar_preview']

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="max-height:150px; border-radius:4px;">', obj.avatar.url)
        return '—'
    avatar_preview.short_description = 'Превью'

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ['language', 'key', 'value']
    list_filter = ['language']
    search_fields = ['key', 'value']
    list_editable = ['value']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class ProjectScreenshotTranslationInline(admin.StackedInline):
    model = ProjectScreenshotTranslation
    extra = 1
    max_num = 5


@admin.register(ProjectScreenshot)
class ProjectScreenshotAdmin(admin.ModelAdmin):
    list_display = ['id', 'project', 'order', 'image_thumb']
    list_filter = ['project']
    inlines = [ProjectScreenshotTranslationInline]

    def image_thumb(self, obj):
        url = obj.image_file.url if obj.image_file else (obj.image if obj.image else '')
        if url:
            return format_html('<img src="{}" style="height:40px; border-radius:2px;">', url)
        return '—'
    image_thumb.short_description = 'Миниатюра'


class ProjectScreenshotInline(admin.TabularInline):
    model = ProjectScreenshot
    fields = ['image_file', 'image', 'order', 'edit_translations']
    readonly_fields = ['image', 'edit_translations']
    extra = 1

    def edit_translations(self, obj):
        if obj.pk:
            url = reverse('admin:portfolio_projectscreenshot_change', args=[obj.pk])
            return format_html('<a href="{}" target="_blank">Переводы (открыть)</a>', url)
        return 'Сохраните проект для перевода скриншотов'
    edit_translations.short_description = 'Переводы'


class ProjectTranslationInline(admin.StackedInline):
    model = ProjectTranslation
    extra = 1
    max_num = 3


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['slug', 'link_type', 'is_mobile_app', 'order', 'preview_thumb']
    list_editable = ['order']
    filter_horizontal = ['tags']
    fieldsets = [
        ('Основное', {
            'fields': ['slug', 'url', 'link_type', 'is_mobile_app', 'order', 'tags'],
        }),
        ('Превью', {
            'fields': ['preview_image', 'preview'],
            'description': 'Загрузи новое изображение — оно имеет приоритет над старым путём.',
        }),
    ]
    readonly_fields = ['preview']
    inlines = [ProjectTranslationInline, ProjectScreenshotInline]

    def preview_thumb(self, obj):
        if obj.preview_image:
            return format_html('<img src="{}" style="height:40px; border-radius:2px;">', obj.preview_image.url)
        return '—'
    preview_thumb.short_description = 'Превью'


