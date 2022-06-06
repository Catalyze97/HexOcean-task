"""Tests for API tiers."""
from django.test import TestCase
from django.urls import reverse

import tempfile
import os

from PIL import Image

from tiers import models
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from tiers import serializers

TIERS_URL = reverse('tiers:tier-list')
CUSTOM_IMAGES_URL = reverse('tiers:customimages-list')


def detail_url(tier_id):
    """Create and return a tier detail URL."""
    return reverse('tiers:tier-detail', args=[tier_id])


def image_upload_url(customimages_id):
    """Create and return a custom images upload url."""
    return reverse('tiers:customimages-upload-image', args=[customimages_id])


def create_tier(user, **params):
    """Create and return a sample tier."""
    defaults = {
        'title': 'Sample tier title.',
        'description': 'Sample description',
    }
    defaults.update(params)

    tier = models.Tier.objects.create(user=user, **defaults)
    return tier


def create_custom_images(user, **params):
    """Create and return a sample custom images model."""
    defaults = {
        'name': 'Image1',
        'image': '',
        'expiring_link_val': 50,
        'expiring_link': '',
        'custom_expiring_link': '',
    }
    defaults.update(params)

    custom_img = models.CustomImages.objects.create(user=user, **defaults)
    return custom_img


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicTiersAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(TIERS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTiersApiTests(TestCase):

    def setUp(self):
        self.user = create_user(email='user@example.com',
                                password='test123',
                                is_superuser=True,
                                is_staff=True)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tiers(self):
        """Test retrieving a list of tiers."""
        create_tier(user=self.user)
        create_tier(user=self.user)

        res = self.client.get(TIERS_URL)

        tiers = models.Tier.objects.all().order_by('-id')
        serializer = serializers.TierSerializer(tiers, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_tier_detail(self):
        """Test get tier detail."""
        tiers = create_tier(user=self.user)

        url = detail_url(tiers.id)
        res = self.client.get(url)

        serializer = serializers.TierDetailSerializer(tiers)
        self.assertEqual(res.data, serializer.data)

    def test_create_tier(self):
        """Test block creating a tier by normal users."""
        payload = {
            'title': 'Premium tier',
            'description': 'Simple description'
        }
        res = self.client.post(TIERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_tier_partial_update(self):
        """Test forbidden partial update of tier for normal users."""
        description = 'Sample description'
        tier = create_tier(
            user=self.user,
            title='Sample title',
            description=description,
        )
        payload = {'title': 'New tier title'}
        url = detail_url(tier.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        tier.refresh_from_db()
        self.assertNotEqual(tier.title, payload['title'])
        self.assertEqual(tier.description, description)
        self.assertEqual(tier.user, self.user)

    def test_tier_full_update(self):
        """Test full update of tier is forbidden for normal users."""
        tier = create_tier(
            user=self.user,
            title='Sample title',
            description='Sample description',
        )
        payload = {
            'title': 'New title',
            'description': 'New description'
        }
        url = detail_url(tier.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        tier.refresh_from_db()
        for k, v in payload.items():
            self.assertNotEqual(getattr(tier, k), v)
            self.assertEqual(tier.user, self.user)

    def test_delete_tier(self):
        """Test deleting a tier is refused to normal users."""
        tier = create_tier(user=self.user)
        url = detail_url(tier.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_custom_images_list_limited_to_user(self):
        """Test list of custom images are limited to authenticated user."""
        other_user = create_user(email='other@example.com', password='test123')
        create_custom_images(user=other_user)
        create_custom_images(user=self.user)

        res = self.client.get(CUSTOM_IMAGES_URL)

        customs = models.CustomImages.objects.filter(user=self.user)
        serializer = serializers.BasicCustomImagesSerializer(customs,
                                                             many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_clear_tiers_custom_images(self):
        """Test clearing a tiers custom images
            is forbidden for normal users."""
        custom_img = models.CustomImages.objects.create(user=self.user,
                                                        name='Img1')
        tiers = create_tier(user=self.user)
        tiers.custom_images.add(custom_img)

        payload = {'custom_images': []}
        url = detail_url(tiers.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(tiers.custom_images.count(), 1)


class UploadImageTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'password123'
        )
        self.client.force_authenticate(self.user)
        self.CustomImages = create_custom_images(user=self.user)

    def tearDown(self):
        self.CustomImages.image.delete()

    def test_upload_image(self):
        """test creating and uploading image."""
        url = image_upload_url(self.CustomImages.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='PNG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.CustomImages.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.CustomImages.image.path))
