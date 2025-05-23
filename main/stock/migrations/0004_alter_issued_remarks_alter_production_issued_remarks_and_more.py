# Generated by Django 5.2.1 on 2025-05-13 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_issued_remarks_production_issued_remarks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issued',
            name='remarks',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='production_issued',
            name='remarks',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='production_return',
            name='remarks',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='remarks',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
