# Generated by Django 5.1 on 2024-08-12 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffeechat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coffeechatrequest',
            name='letterToSenior',
            field=models.TextField(blank=True, null=True),
        ),
    ]
