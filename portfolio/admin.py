from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSettings, Translation, Project, ProjectScreenshot, ProjectTranslation


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


class ProjectScreenshotInline(admin.TabularInline):
    model = ProjectScreenshot
    fields = ['image_file', 'image', 'order']
    readonly_fields = ['image']
    extra = 1


class ProjectTranslationInline(admin.StackedInline):
    model = ProjectTranslation
    extra = 1
    max_num = 3


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['slug', 'link_type', 'is_mobile_app', 'order', 'preview_thumb']
    list_editable = ['order']
    fieldsets = [
        ('Основное', {
            'fields': ['slug', 'url', 'link_type', 'is_mobile_app', 'order'],
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
