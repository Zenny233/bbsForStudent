# Generated by Django 2.0.13 on 2019-10-30 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20191030_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='code',
            field=models.CharField(default=0, max_length=20, verbose_name='验证码'),
            preserve_default=False,
        ),
    ]