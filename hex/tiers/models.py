"""Models for tiers."""
import uuid
import os

from django.db import models
from django.conf import settings


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
    image = models.ImageField(blank=True, null=True, upload_to=tier_image_file_path)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title
