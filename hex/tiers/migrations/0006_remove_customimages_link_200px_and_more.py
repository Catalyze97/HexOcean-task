# Generated by Django 4.0.5 on 2022-06-05 13:59

import django.core.validators
from django.db import migrations, models
import tiers.models


class Migration(migrations.Migration):

    dependencies = [
        ('tiers', '0005_alter_customimages_custom_expiring_link_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customimages',
            name='link_200px',
        ),
        migrations.RemoveField(
            model_name='customimages',
            name='link_400px',
        ),
        migrations.RemoveField(
            model_name='customimages',
            name='link_original',
        ),
        migrations.AlterField(
            model_name='customimages',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=tiers.models.tier_image_file_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png'])]),
        ),
    ]
