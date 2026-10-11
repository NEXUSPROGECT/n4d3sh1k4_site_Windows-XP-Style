from django.db import migrations


def add_og_and_uk_translations(apps, schema_editor):
    Translation = apps.get_model('portfolio', 'Translation')

    translations_data = [
        # --- English (en) OG tags ---
        {
            'language': 'en',
            'key': 'og.title',
            'value': 'Mihail Krivosheev — Backend & Android Developer',
        },
        {
            'language': 'en',
            'key': 'og.description',
            'value': 'Software Engineer specializing in Java/Spring, Android, and Linux systems. Portfolio, pet projects, and contacts.',
        },

        # --- Russian (ru) OG tags ---
        {
            'language': 'ru',
            'key': 'og.title',
            'value': 'Михаил Кривошеев — Backend & Android Developer',
        },
        {
            'language': 'ru',
            'key': 'og.description',
            'value': 'Backend-разработчик на Java/Spring, Android и Linux. Портфолио проектов и контакты.',
        },

        # --- Ukrainian (uk) OG tags ---
        {
            'language': 'uk',
            'key': 'og.title',
            'value': 'Михайло Кривошеєв — Backend & Android Developer',
        },
        {
            'language': 'uk',
            'key': 'og.description',
            'value': 'Backend-розробник на Java/Spring, Android та Linux. Портфоліо проєктів та контакти.',
        },

        # --- Ukrainian (uk) UI translations ---
        {
            'language': 'uk',
            'key': 'loader.loading',
            'value': 'Завантаження ресурсів...',
        },
        {
            'language': 'uk',
            'key': 'loader.title',
            'value': 'Завантаження',
        },
        {
            'language': 'uk',
            'key': 'desktop.projects',
            'value': 'Проєкти',
        },
        {
            'language': 'uk',
            'key': 'desktop.profile',
            'value': 'Профіль',
        },
        {
            'language': 'uk',
            'key': 'desktop.about',
            'value': 'Про мене.txt',
        },
        {
            'language': 'uk',
            'key': 'desktop.about.bar',
            'value': 'Про мене.txt - Блокнот',
        },
        {
            'language': 'uk',
            'key': 'desktop.projects.bar',
            'value': 'Мої Проєкти',
        },
        {
            'language': 'uk',
            'key': 'desktop.profile.bar',
            'value': 'Профіль',
        },
        {
            'language': 'uk',
            'key': 'desktop.start',
            'value': 'Пуск',
        },
        {
            'language': 'uk',
            'key': 'profile.name',
            'value': 'Михайло Кривошеєв',
        },
        {
            'language': 'uk',
            'key': 'about.text',
            'value': 'Привіт 👋 я backend/Android-розробник, який любить створювати чисті та надійні системи. Крім основних компетенцій, на яких я намагаюся зосередитися, у мене багато інших навичок: Python, Java/Kotlin, C#, SQL та бази даних, інфраструктура та DevOps, мережева інженерія.',
        },
        {
            'language': 'uk',
            'key': 'projects.empty',
            'value': 'Виберіть проєкт для перегляду деталей',
        },
        {
            'language': 'uk',
            'key': 'startmenu.language',
            'value': 'Мова ▶',
        },
        {
            'language': 'uk',
            'key': 'desktop.github',
            'value': 'GitHub',
        },
        {
            'language': 'uk',
            'key': 'footer.text',
            'value': 'У стилі Windows XP',
        },
        {
            'language': 'uk',
            'key': 'viewer.title',
            'value': 'Перегляд зображень',
        },
    ]

    for item in translations_data:
        Translation.objects.update_or_create(
            language=item['language'],
            key=item['key'],
            defaults={'value': item['value']},
        )


def remove_og_and_uk_translations(apps, schema_editor):
    Translation = apps.get_model('portfolio', 'Translation')
    Translation.objects.filter(key__in=['og.title', 'og.description']).delete()
    Translation.objects.filter(language='uk').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_sociallink'),
    ]

    operations = [
        migrations.RunPython(add_og_and_uk_translations, remove_og_and_uk_translations),
    ]
