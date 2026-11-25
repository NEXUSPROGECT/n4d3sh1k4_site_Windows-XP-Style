from django.conf import settings
from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views

SPLAV_URL = f'{settings.STATIC_URL}games/splav/index.html'

urlpatterns = [
    path('', views.index, name='index'),
    path('splav', RedirectView.as_view(url=SPLAV_URL, permanent=False)),
    path('splav/', RedirectView.as_view(url=SPLAV_URL, permanent=False), name='splav'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    path('site.webmanifest', views.webmanifest, name='webmanifest'),
    path('projects.json', views.projects_json, name='projects_json'),
    path('api/leaderboard', views.leaderboard, name='leaderboard'),
    path('api/leaderboard/', views.leaderboard),
    re_path(r'^i18n/projects\.(?P<lang>\w+)\.json$', views.project_translations_json, name='project_translations'),
    re_path(r'^i18n/(?P<lang>\w+)\.json$', views.translations_json, name='translations'),
]
