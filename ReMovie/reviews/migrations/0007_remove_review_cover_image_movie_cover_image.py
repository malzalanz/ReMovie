# Generated by Django 4.1 on 2024-05-31 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_rename_comment_review_review_text_review_cover_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='cover_image',
        ),
        migrations.AddField(
            model_name='movie',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
