# Generated by Django 2.0.13 on 2019-11-15 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_auto_20191115_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='is_check_article',
            field=models.CharField(default='0', max_length=2),
        ),
        migrations.AlterField(
            model_name='comment',
            name='is_check_comment',
            field=models.CharField(default='0', max_length=2),
        ),
    ]
