# Generated by Django 5.0.6 on 2024-06-08 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_lat_networkcoverage_x_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkcoverage',
            name='operator',
            field=models.IntegerField(max_length=100),
        ),
        migrations.AlterField(
            model_name='networkcoverage',
            name='x',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='networkcoverage',
            name='y',
            field=models.IntegerField(),
        ),
    ]