import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='Аватарка')),
            ],
            options={
                'verbose_name': 'Настройки сайта',
                'verbose_name_plural': 'Настройки сайта',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='preview_image',
            field=models.ImageField(blank=True, null=True, upload_to='projects/', verbose_name='Превью (загрузить)'),
        ),
        migrations.AlterField(
            model_name='project',
            name='preview',
            field=models.CharField(
                blank=True, max_length=300, verbose_name='Превью (старый путь)',
                help_text='Автозаполняется при импорте. Используй поле ниже для загрузки.',
            ),
        ),
        migrations.AddField(
            model_name='projectscreenshot',
            name='image_file',
            field=models.ImageField(blank=True, null=True, upload_to='screenshots/', verbose_name='Изображение (загрузить)'),
        ),
        migrations.AlterField(
            model_name='projectscreenshot',
            name='image',
            field=models.CharField(blank=True, max_length=300, verbose_name='Изображение (старый путь)'),
        ),
    ]
