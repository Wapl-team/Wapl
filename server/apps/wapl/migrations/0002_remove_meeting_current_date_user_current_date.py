# Generated by Django 4.1.6 on 2023-02-07 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wapl', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='current_date',
        ),
        migrations.AddField(
            model_name='user',
            name='current_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]