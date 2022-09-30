# Generated by Django 3.2.15 on 2022-09-11 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_products_thumbnailimage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='login',
            options={'verbose_name_plural': 'Login'},
        ),
        migrations.AlterModelOptions(
            name='shippingaddress',
            options={'verbose_name_plural': 'ShippingAddress'},
        ),
        migrations.AddField(
            model_name='category',
            name='thumbnailImage',
            field=models.ImageField(default='', upload_to='images/'),
        ),
    ]