from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from .models import SiteSettings, Translation, Project, ProjectTranslation, ProjectScreenshot, Tag, SocialLink
from .language import detect_language, lang_to_locale


def index(request):
    site = SiteSettings.get()
    avatar_url = site.avatar.url if site.avatar else None

    default_lang = detect_language(request)
    translations = Translation.objects.filter(language=default_lang)
    trans_dict = {t.key: t.value for t in translations}

    projects_qs = Project.objects.prefetch_related(
        'screenshots', 'tags', 'translations'
    ).order_by('order')

    projects = []
    for p in projects_qs:
        ru_trans = None
        for t in p.translations.all():
            if t.language == default_lang:
                ru_trans = t
                break
        screenshots = [_image_url(s.image_file, s.image) for s in p.screenshots.all()]
        projects.append({
            'slug': p.slug,
            'url': p.url,
            'link_type': p.link_type,
            'preview': _image_url(p.preview_image, p.preview),
            'screenshots': screenshots,
            'title': ru_trans.title if ru_trans else p.slug,
            'description': ru_trans.description if ru_trans else '',
            'is_mobile_app': p.is_mobile_app,
            'tags': [t.name for t in p.tags.all()],
        })

    canonical_url = request.build_absolute_uri('/').rstrip('/')
    available_langs = ['ru', 'en', 'uk']
    avatar_abs_url = _absolute_url(request, avatar_url, settings.STATIC_URL + 'assets/avatar.jpg')

    social_links = [
        {'name': sl.name, 'url': sl.url, 'icon_url': _image_url(sl.icon)}
        for sl in SocialLink.objects.order_by('order')
    ]

    return render(request, 'portfolio/index.html', {
        'avatar_url': avatar_url,
        'avatar_abs_url': avatar_abs_url,
        'translations': trans_dict,
        'projects': projects,
        'default_lang': default_lang,
        'og_locale': lang_to_locale(default_lang),
        'canonical_url': canonical_url,
        'available_langs': available_langs,
        'social_links': social_links,
    })


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


def _absolute_url(request, url, fallback_path=''):
    """Turn a possibly-relative URL into an absolute one for OG/social tags."""
    if url and (url.startswith('http://') or url.startswith('https://')):
        return url
    target = url or fallback_path
    if not target:
        return ''
    return request.build_absolute_uri(target)


def _static_url(path):
    if path.startswith('/') or path.startswith('http'):
        return path
    return f'{settings.STATIC_URL}{path}'


def robots_txt(request):
    host = request.get_host()
    scheme = 'https' if request.is_secure() else 'http'
    content = f"User-agent: *\nAllow: /\nSitemap: {scheme}://{host}/sitemap.xml\n"
    return HttpResponse(content, content_type='text/plain')


def webmanifest(request):
    from django.template.loader import render_to_string
    context = {
        'start_url': request.build_absolute_uri('/'),
        'icon_urls': {
            '192': _static_url('assets/favicon/android-chrome-192x192.png'),
            '512': _static_url('assets/favicon/android-chrome-512x512.png'),
        },
    }
    return HttpResponse(
        render_to_string('portfolio/webmanifest.json', context),
        content_type='application/manifest+json',
    )


def sitemap_xml(request):
    host = request.get_host()
    scheme = 'https' if request.is_secure() else 'http'
    today = __import__('datetime').date.today().isoformat()
    content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{scheme}://{host}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>'''
    return HttpResponse(content, content_type='application/xml')
