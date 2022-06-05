"""Models for tiers."""
import uuid
import os

from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFill

def tier_image_file_path(instance, filename):
    """Generate file path for new tier image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'tier', filename)


class Tier(models.Model):
    """Tier object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    custom_images = models.ManyToManyField('CustomImages')

    def __str__(self):
        return self.title


class CustomImages(models.Model):
    """Custom image for filtering tiers."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(blank=True,
                              null=True,
                              upload_to=tier_image_file_path,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])])

    link_200px = ImageSpecField(source='image',
                                processors=[ResizeToFill(200, 200)],
                                format='PNG',
                                options={'quality': 70})

    link_400px = ImageSpecField(source='image',
                                processors=[ResizeToFill(400, 400)],
                                format='PNG',
                                options={'quality': 70})

    expiring_link_val = models.PositiveIntegerField(blank=True, null=True,)
    expiring_link = models.CharField(max_length=255, blank=True, null=True,)
    """Fields for custom tiers."""
    custom_expiring_link = models.CharField(max_length=255, blank=True, null=True,)
    custom_link_height = models.PositiveIntegerField(blank=True, null=True, default=0)
    custom_link_width = models.PositiveIntegerField(blank=True, null=True, default=0)
    custom_link = models.CharField(max_length=255, blank=True, null=True,)

    def __str__(self):
        return self.name
