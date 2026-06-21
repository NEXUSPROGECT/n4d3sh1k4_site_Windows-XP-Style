from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import SiteSettings, Translation, Project, ProjectTranslation, ProjectScreenshot



def index(request):
    site = SiteSettings.get()
    avatar_url = site.avatar.url if site.avatar else None
    return render(request, 'portfolio/index.html', {'avatar_url': avatar_url})


def translations_json(request, lang):
    qs = Translation.objects.filter(language=lang).values('key', 'value')
    data = {item['key']: item['value'] for item in qs}
    return JsonResponse(data)


def projects_json(request):
    projects = Project.objects.prefetch_related('screenshots', 'tags').order_by('order')
    data = [
        {
            'id': p.slug,
            'url': p.url,
            'linkType': p.link_type,
            'preview': _image_url(p.preview_image, p.preview),
            'screenshots': [_image_url(s.image_file, s.image) for s in p.screenshots.all()],
            'tags': [t.name for t in p.tags.all()],
            'isMobileApp': p.is_mobile_app,
        }
        for p in projects
    ]
    return JsonResponse(data, safe=False)


def project_translations_json(request, lang):
    qs = ProjectTranslation.objects.filter(language=lang).select_related('project')
    data = {}
    for pt in qs:
        key = pt.project.slug
        data[f'project.{key}.title'] = pt.title
        data[f'project.{key}.description'] = pt.description

    # Добавляем переводы для скриншотов
    from collections import defaultdict
    screenshot_indices = defaultdict(int)
    screenshots = ProjectScreenshot.objects.select_related('project').prefetch_related('translations').order_by('project_id', 'order')
    for s in screenshots:
        slug = s.project.slug
        idx = screenshot_indices[slug]
        screenshot_indices[slug] += 1

        trans = None
        for t in s.translations.all():
            if t.language == lang:
                trans = t
                break

        data[f'project.{slug}.screenshot.{idx}.title'] = trans.title if trans else ""
        data[f'project.{slug}.screenshot.{idx}.description'] = trans.description if trans else ""

    return JsonResponse(data)



def _image_url(image_field, fallback_path=''):
    """ImageField (MinIO) takes priority; falls back to static asset path."""
    if image_field:
        return image_field.url
    if fallback_path:
        return _static_url(fallback_path)
    return ''


def _static_url(path):
    if path.startswith('/') or path.startswith('http'):
        return path
    return f'{settings.STATIC_URL}{path}'
