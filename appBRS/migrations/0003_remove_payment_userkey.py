# Generated by Django 3.1.4 on 2021-06-24 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appBRS', '0002_auto_20210624_1556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='userKey',
        ),
    ]
