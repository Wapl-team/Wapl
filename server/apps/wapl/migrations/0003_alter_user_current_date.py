# Generated by Django 4.1.6 on 2023-02-07 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wapl', '0002_remove_meeting_current_date_user_current_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='current_date',
            field=models.DateField(null=True),
        ),
    ]