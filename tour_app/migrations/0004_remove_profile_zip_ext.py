# Generated by Django 3.2.7 on 2021-12-09 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour_app', '0003_auto_20211209_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='zip_ext',
        ),
    ]
