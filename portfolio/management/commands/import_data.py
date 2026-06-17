import json
from pathlib import Path
from django.core.management.base import BaseCommand
from portfolio.models import Translation, Project, ProjectScreenshot, ProjectTranslation


class Command(BaseCommand):
    help = 'Import translations and projects from JSON files (one-time migration)'

    def handle(self, *args, **options):
        base = Path('.')
        self._import_ui_translations(base)
        self._import_projects(base)
        self._import_project_translations(base)
        self.stdout.write(self.style.SUCCESS('Import completed successfully'))

    def _import_ui_translations(self, base):
        for lang in ['en', 'ru']:
            path = base / 'i18n' / f'{lang}.json'
            if not path.exists():
                self.stdout.write(self.style.WARNING(f'Not found: {path}'))
                continue
            with open(path, encoding='utf-8-sig') as f:
                data = json.load(f)
            count = 0
            for key, value in data.items():
                Translation.objects.update_or_create(
                    language=lang, key=key, defaults={'value': value}
                )
                count += 1
            self.stdout.write(f'UI translations [{lang}]: {count} keys')

    def _import_projects(self, base):
        path = base / 'projects.json'
        if not path.exists():
            self.stdout.write(self.style.WARNING(f'Not found: {path}'))
            return
        with open(path, encoding='utf-8-sig') as f:
            projects = json.load(f)
        for i, p in enumerate(projects):
            project, _ = Project.objects.update_or_create(
                slug=p['id'],
                defaults={
                    'url': p['url'],
                    'link_type': p['linkType'],
                    'preview': p['preview'],
                    'is_mobile_app': p['isMobileApp'],
                    'order': i,
                },
            )
            project.screenshots.all().delete()
            for j, img in enumerate(p.get('screenshots', [])):
                ProjectScreenshot.objects.create(project=project, image=img, order=j)
        self.stdout.write(f'Projects: {len(projects)} imported')

    def _import_project_translations(self, base):
        for lang in ['en', 'ru']:
            path = base / 'i18n' / f'projects.{lang}.json'
            if not path.exists():
                self.stdout.write(self.style.WARNING(f'Not found: {path}'))
                continue
            with open(path, encoding='utf-8-sig') as f:
                data = json.load(f)
            for project in Project.objects.all():
                title = data.get(f'project.{project.slug}.title', project.slug)
                description = data.get(f'project.{project.slug}.description', '')
                ProjectTranslation.objects.update_or_create(
                    project=project, language=lang,
                    defaults={'title': title, 'description': description},
                )
            self.stdout.write(f'Project translations [{lang}]: done')
