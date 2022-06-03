"""
Tests for the custom images API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from tiers.models import CustomImages
from tiers import serializers


CUSTOM_IMAGES_URL = reverse('tiers:customimages-list')


def detail_url(custom_images_id):
    """Create and return a custom image detail url."""
    return reverse('tiers:customimages-detail', args=[custom_images_id])


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicCustomImagesApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving custom images"""
        res = self.client.get(CUSTOM_IMAGES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCustomImagesApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_custom_images(self):
        """Test retrieving a list of custom images."""

        CustomImages.objects.create(user=self.user, name='Image1')
        CustomImages.objects.create(user=self.user, name='Image2')

        res = self.client.get(CUSTOM_IMAGES_URL)

        custom_images = CustomImages.objects.all().order_by('-name')
        serializer = serializers.BasicCustomImagesSerializer(custom_images, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_custom_images_are_limited_to_user(self):
        """Test list of custom images is limited to authenticated user."""
        user2 = create_user(email='user2@example.com')
        CustomImages.objects.create(user=user2, name='ImgCoffe')
        custom_image = CustomImages.objects.create(user=self.user, name='ImgTea')

        res = self.client.get(CUSTOM_IMAGES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], custom_image.name)
        self.assertEqual(res.data[0]['id'], custom_image.id)

    def test_update_custom_images(self):
        """Test updating a custom images"""
        custom_image = CustomImages.objects.create(user=self.user, name='ImageCoffe')

        payload = {'name': 'ImageTea'}
        url = detail_url(custom_image.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        custom_image.refresh_from_db()
        self.assertEqual(custom_image.name, payload['name'])

    def test_deleting_custom_images(self):
        """Test deleting a custom images."""
        custom_image = CustomImages.objects.create(user=self.user, name='ImageBeer')

        url = detail_url(custom_image.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        custom_image = CustomImages.objects.filter(user=self.user)
        self.assertFalse(custom_image.exists())
