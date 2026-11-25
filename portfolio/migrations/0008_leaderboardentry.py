from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0007_splav_translation'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaderboardEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.UUIDField(unique=True, verbose_name='ID игрока')),
                ('name', models.CharField(max_length=32, verbose_name='Имя')),
                ('score', models.PositiveIntegerField(default=0, verbose_name='Счёт')),
                ('level', models.PositiveSmallIntegerField(default=1, verbose_name='Уровень')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={
                'verbose_name': 'Рекорд',
                'verbose_name_plural': 'Таблица рекордов',
                'ordering': ['-score', 'updated_at'],
                'indexes': [models.Index(fields=['-score', 'updated_at'], name='portfolio_lb_score_idx')],
            },
        ),
    ]
