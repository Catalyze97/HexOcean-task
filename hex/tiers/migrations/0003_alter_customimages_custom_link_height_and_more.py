# Generated by Django 4.0.5 on 2022-06-05 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiers', '0002_alter_customimages_custom_link_height_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customimages',
            name='custom_link_height',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customimages',
            name='custom_link_width',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]