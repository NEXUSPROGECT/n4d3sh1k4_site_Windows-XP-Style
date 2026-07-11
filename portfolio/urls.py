from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    path('projects.json', views.projects_json, name='projects_json'),
    re_path(r'^i18n/projects\.(?P<lang>\w+)\.json$', views.project_translations_json, name='project_translations'),
    re_path(r'^i18n/(?P<lang>\w+)\.json$', views.translations_json, name='translations'),
]
