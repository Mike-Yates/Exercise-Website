# Generated by Django 3.1.7 on 2021-04-08 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_post', models.CharField(default='', max_length=500)),
                ('blog_user', models.CharField(default='', max_length=200)),
                ('date_published', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='SportsXP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('basketball', models.PositiveIntegerField(default=0)),
                ('cross_training', models.PositiveIntegerField(default=0)),
                ('cardio', models.PositiveIntegerField(default=0)),
                ('strength_training', models.PositiveIntegerField(default=0)),
                ('climbing', models.PositiveIntegerField(default=0)),
                ('soccer', models.PositiveIntegerField(default=0)),
                ('american_football', models.PositiveIntegerField(default=0)),
                ('dance', models.PositiveIntegerField(default=0)),
                ('gymnastics', models.PositiveIntegerField(default=0)),
                ('hiking', models.PositiveIntegerField(default=0)),
                ('swimming', models.PositiveIntegerField(default=0)),
                ('yoga', models.PositiveIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_login', models.BooleanField(default=True)),
                ('bio', models.TextField(default='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_name', models.CharField(default='', max_length=200)),
                ('reps', models.PositiveIntegerField(default=0)),
                ('sets', models.PositiveIntegerField(default=0)),
                ('weight_in_pounds', models.PositiveIntegerField(default=0)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
