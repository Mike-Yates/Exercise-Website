# Generated by Django 3.1.7 on 2021-04-08 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0006_auto_20210408_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='exercise_name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='sportsxp',
            name='american_football',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sportsxp',
            name='basketball',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sportsxp',
            name='cardio',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sportsxp',
            name='climbing',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sportsxp',
            name='cross_training',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sportsxp',
            name='dance',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sportsxp',
            name='gymnastics',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sportsxp',
            name='hiking',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sportsxp',
            name='soccer',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sportsxp',
            name='strength_training',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sportsxp',
            name='swimming',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sportsxp',
            name='yoga',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
