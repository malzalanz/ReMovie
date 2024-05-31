# Generated by Django 4.1 on 2024-05-31 10:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_rename_average_rating_stats_avg_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='comment',
            new_name='review_text',
        ),
        migrations.AddField(
            model_name='review',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
