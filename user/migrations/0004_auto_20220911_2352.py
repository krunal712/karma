# Generated by Django 3.2.15 on 2022-09-11 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20220911_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='login',
            name='createdDate',
        ),
        migrations.RemoveField(
            model_name='users',
            name='email',
        ),
    ]
