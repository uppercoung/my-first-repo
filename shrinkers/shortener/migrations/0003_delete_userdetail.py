# Generated by Django 3.2 on 2022-08-31 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0002_userdetail'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserDetail',
        ),
    ]
