# Generated by Django 4.2.3 on 2023-07-19 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_remove_readbook_user_id_book_date_marked'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]