# Generated by Django 3.2.8 on 2022-04-16 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_book_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name'], 'verbose_name': 'Автор', 'verbose_name_plural': 'Авторы'},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['id'], 'verbose_name': 'Книга', 'verbose_name_plural': 'Книги'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['title'], 'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterField(
            model_name='book',
            name='year',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='Год'),
        ),
    ]