from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

from .models import SiteSettings, Translation, Project, ProjectTranslation


def index(request):
    site = SiteSettings.get()
    avatar_url = site.avatar.url if site.avatar else None
    return render(request, 'portfolio/index.html', {'avatar_url': avatar_url})


def translations_json(request, lang):
    qs = Translation.objects.filter(language=lang).values('key', 'value')
    data = {item['key']: item['value'] for item in qs}
    return JsonResponse(data)


def projects_json(request):
    projects = Project.objects.prefetch_related('screenshots').order_by('order')
    data = [
        {
            'id': p.slug,
            'url': p.url,
            'linkType': p.link_type,
            'preview': _image_url(p.preview_image, p.preview),
            'screenshots': [_image_url(s.image_file, s.image) for s in p.screenshots.all()],
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
