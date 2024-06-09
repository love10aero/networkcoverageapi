# Generated by Django 5.0.6 on 2024-06-08 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='networkcoverage',
            old_name='x',
            new_name='lat',
        ),
        migrations.RenameField(
            model_name='networkcoverage',
            old_name='y',
            new_name='long',
        ),
        migrations.AlterField(
            model_name='networkcoverage',
            name='fourG',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='networkcoverage',
            name='threeG',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='networkcoverage',
            name='twoG',
            field=models.BooleanField(),
        ),
    ]
