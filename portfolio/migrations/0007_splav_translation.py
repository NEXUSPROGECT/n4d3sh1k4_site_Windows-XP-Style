from django.db import migrations


TRANSLATIONS = {
    'ru': 'Сплав',
    'en': 'Splav',
    'uk': 'Сплав',
}


def add_splav_translation(apps, schema_editor):
    Translation = apps.get_model('portfolio', 'Translation')
    for language, value in TRANSLATIONS.items():
        Translation.objects.update_or_create(
            language=language,
            key='desktop.splav',
            defaults={'value': value},
        )


def remove_splav_translation(apps, schema_editor):
    Translation = apps.get_model('portfolio', 'Translation')
    Translation.objects.filter(key='desktop.splav').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0006_og_and_multilang_translations'),
    ]

    operations = [
        migrations.RunPython(add_splav_translation, remove_splav_translation),
    ]
