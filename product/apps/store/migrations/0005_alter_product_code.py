# Generated by Django 4.0 on 2021-12-20 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rename_first_name_provider_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(max_length=12, unique=True, verbose_name='Código'),
        ),
    ]
