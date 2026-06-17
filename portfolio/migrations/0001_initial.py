import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='ID (slug)')),
                ('url', models.URLField(verbose_name='Ссылка')),
                ('link_type', models.CharField(
                    help_text='Например: GitHub Repository, Website',
                    max_length=100,
                    verbose_name='Тип ссылки',
                )),
                ('preview', models.CharField(
                    help_text='Путь к изображению: assets/projects/MyApp/1.png',
                    max_length=300,
                    verbose_name='Превью',
                )),
                ('is_mobile_app', models.BooleanField(default=False, verbose_name='Мобильное приложение')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=10, verbose_name='Язык')),
                ('key', models.CharField(max_length=200, verbose_name='Ключ')),
                ('value', models.TextField(verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Перевод',
                'verbose_name_plural': 'Переводы интерфейса',
                'ordering': ['language', 'key'],
            },
        ),
        migrations.CreateModel(
            name='ProjectTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=10, verbose_name='Язык')),
                ('title', models.CharField(max_length=300, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('project', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='translations',
                    to='portfolio.project',
                    verbose_name='Проект',
                )),
            ],
            options={
                'verbose_name': 'Перевод проекта',
                'verbose_name_plural': 'Переводы проектов',
            },
        ),
        migrations.CreateModel(
            name='ProjectScreenshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(
                    help_text='Путь к изображению: assets/projects/MyApp/2.png',
                    max_length=300,
                    verbose_name='Изображение',
                )),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('project', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='screenshots',
                    to='portfolio.project',
                    verbose_name='Проект',
                )),
            ],
            options={
                'verbose_name': 'Скриншот',
                'verbose_name_plural': 'Скриншоты',
                'ordering': ['order'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='translation',
            unique_together={('language', 'key')},
        ),
        migrations.AlterUniqueTogether(
            name='projecttranslation',
            unique_together={('project', 'language')},
        ),
    ]
