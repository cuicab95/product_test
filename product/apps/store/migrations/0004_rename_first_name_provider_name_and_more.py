# Generated by Django 4.0 on 2021-12-19 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_order_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='provider',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='last_name',
        ),
    ]
