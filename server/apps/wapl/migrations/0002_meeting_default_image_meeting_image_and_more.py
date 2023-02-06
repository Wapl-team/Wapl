# Generated by Django 4.1.6 on 2023-02-06 17:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wapl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='default_image',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='image',
            field=models.ImageField(blank=True, upload_to='team_profile'),
        ),
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
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='plans', to='wapl.meeting'),
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_share', models.BooleanField()),
                ('meeting', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='meeting_shares', to='wapl.meeting')),
                ('plan', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='plan_shares', to='wapl.privateplan')),
            ],
        ),
    ]