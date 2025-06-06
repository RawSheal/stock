# Generated by Django 5.2.1 on 2025-05-13 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_issued_colour_production_issued_colour_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='issued',
            name='remarks',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='production_issued',
            name='remarks',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='production_return',
            name='remarks',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='remarks',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
