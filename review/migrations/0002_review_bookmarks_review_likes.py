# Generated by Django 5.0.7 on 2024-07-30 11:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("review", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="bookmarks",
            field=models.ManyToManyField(
                blank=True, related_name="review_bookmarks", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="review",
            name="likes",
            field=models.ManyToManyField(
                blank=True, related_name="review_likes", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
