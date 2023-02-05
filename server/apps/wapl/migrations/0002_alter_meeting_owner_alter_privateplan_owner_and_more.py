# Generated by Django 4.1.6 on 2023-02-04 11:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wapl', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='meetings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='privateplan',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='plans', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='publicplan',
            name='meetings',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='plans', to='wapl.meeting'),
        ),
    ]