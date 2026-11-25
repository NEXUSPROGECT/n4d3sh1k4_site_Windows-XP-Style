from django.db import migrations


TRANSLATIONS = {
    'ru': {
        'desktop.leaderboard': 'Рекорды',
        'desktop.leaderboard.bar': 'Рекорды - SPLAV',
        'leaderboard.loading': 'Загрузка рекордов...',
        'leaderboard.empty': 'Пока нет рекордов. Сыграйте в «Сплав»!',
        'leaderboard.error': 'Не удалось загрузить рекорды',
        'leaderboard.refresh': 'Обновить',
        'leaderboard.hint': 'Имя задаётся в игре «Сплав» при первом запуске.',
        'leaderboard.player': 'Игрок',
        'leaderboard.score': 'Счёт',
        'leaderboard.level': 'Уровень',
    },
    'en': {
        'desktop.leaderboard': 'Leaderboard',
        'desktop.leaderboard.bar': 'Leaderboard - SPLAV',
        'leaderboard.loading': 'Loading scores...',
        'leaderboard.empty': 'No scores yet. Play Splav!',
        'leaderboard.error': 'Could not load scores',
        'leaderboard.refresh': 'Refresh',
        'leaderboard.hint': 'Set your name in Splav on first launch.',
        'leaderboard.player': 'Player',
        'leaderboard.score': 'Score',
        'leaderboard.level': 'Level',
    },
    'uk': {
        'desktop.leaderboard': 'Рекорди',
        'desktop.leaderboard.bar': 'Рекорди - SPLAV',
        'leaderboard.loading': 'Завантаження рекордів...',
        'leaderboard.empty': 'Поки немає рекордів. Зіграйте у «Сплав»!',
        'leaderboard.error': 'Не вдалося завантажити рекорди',
        'leaderboard.refresh': 'Оновити',
        'leaderboard.hint': 'Ім\'я задається у грі «Сплав» під час першого запуску.',
        'leaderboard.player': 'Гравець',
        'leaderboard.score': 'Рахунок',
        'leaderboard.level': 'Рівень',
    },
}


def add_translations(apps, schema_editor):
    Translation = apps.get_model('portfolio', 'Translation')
    for language, values in TRANSLATIONS.items():
        for key, value in values.items():
            Translation.objects.get_or_create(
                language=language,
                key=key,
                defaults={'value': value},
            )


def remove_translations(apps, schema_editor):
    Translation = apps.get_model('portfolio', 'Translation')
    for values in TRANSLATIONS.values():
        Translation.objects.filter(key__in=values.keys()).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0008_leaderboardentry'),
    ]

    operations = [
        migrations.RunPython(add_translations, remove_translations),
    ]
