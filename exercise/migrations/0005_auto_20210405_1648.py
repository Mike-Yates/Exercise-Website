# Generated by Django 3.1.7 on 2021-04-05 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0004_auto_20210330_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='height',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='weight',
            field=models.IntegerField(default=0),
        ),
    ]
