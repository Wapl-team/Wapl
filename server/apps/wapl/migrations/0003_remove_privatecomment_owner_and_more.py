# Generated by Django 4.1.6 on 2023-02-13 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wapl', '0002_privatecomment_owner_publiccomment_owner_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='privatecomment',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='publiccomment',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='replyprivatecomment',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='replypubliccomment',
            name='owner',
        ),
    ]