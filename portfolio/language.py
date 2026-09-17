import json
import logging
import re
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

SUPPORTED_LANGS = {'ru', 'en', 'uk'}
DEFAULT_LANG = 'ru'
_IP_API = 'http://ip-api.com/json/{ip}?fields=countryCode'
_IP_TIMEOUT = 2


def detect_language(request):
    """Detect the most suitable language for the request.

    Priority: explicit user cookie -> Accept-Language (browser/OS) ->
    IP geolocation (optional) -> default 'ru'.
    """
    lang = _from_cookie(request)
    if not lang:
        lang = _from_accept_language(request)
    if not lang and getattr(settings, 'USE_IP_DETECTION', False):
        lang = _from_ip(request)
    return lang if lang in SUPPORTED_LANGS else DEFAULT_LANG


def lang_to_locale(lang):
    return {'ru': 'ru_RU', 'uk': 'uk_UA', 'en': 'en_US'}.get(lang, 'ru_RU')


def _from_cookie(request):
    return (request.COOKIES.get('lang') or '').lower() or None


def _from_accept_language(request):
    header = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    if not header:
        return None
    items = []
    for part in header.split(','):
        part = part.strip()
        m = re.match(r'([a-zA-Z]+)(?:-[a-zA-Z]+)?(?:;\s*q=([0-9.]+))?', part)
        if not m:
            continue
        code = m.group(1).lower()
        q = float(m.group(2)) if m.group(2) else 1.0
        items.append((q, code))
    for _, code in sorted(items, key=lambda x: x[0], reverse=True):
        if code in SUPPORTED_LANGS:
            return code
    return None


def _from_ip(request):
    ip = _client_ip(request)
    if not ip:
        return None
    cache_key = f'lang_ip_{ip}'
    lang = cache.get(cache_key)
    if lang is not None:
        return lang or None
    try:
        req = Request(
            _IP_API.format(ip=ip),
            headers={'User-Agent': 'n4d3sh1k4-site-language-detection'},
        )
        with urlopen(req, timeout=_IP_TIMEOUT) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        cc = (data.get('countryCode') or '').lower()
        lang = {'ru': 'ru', 'ua': 'uk'}.get(cc, 'en') if cc else ''
    except Exception as exc:
        logger.debug('IP language lookup failed for %s: %s', ip, exc)
        lang = ''
    cache.set(cache_key, lang, 60 * 60)
    return lang or None


def _client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')