"""Tests for API tiers."""
from django.test import TestCase
from django.urls import reverse

import tempfile
import os

from PIL import Image

from unittest.mock import patch

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
    return reverse('tiers:customimages-detail', args=[customimages_id])


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
        'custom_link_height': 200,
        'custom_link_width': 400,

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
        self.user = create_user(email='user@example.com', password='test123', is_superuser=True, is_staff=True)
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
        """Test partial update of tier."""
        description = 'Sample description'
        tier = create_tier(
            user=self.user,
            title='Sample title',
            description=description,
        )
        payload = {'title': 'New tier title'}
        url = detail_url(tier.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tier.refresh_from_db()
        self.assertEqual(tier.title, payload['title'])
        self.assertEqual(tier.description, description)
        self.assertEqual(tier.user, self.user)

    def test_tier_full_update(self):
        """Test full update of tier."""
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

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tier.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(tier, k), v)
            self.assertEqual(tier.user, self.user)

    def test_delete_tier(self):
        """Test deleting a tier successful"""
        tier = create_tier(user=self.user)

        url = detail_url(tier.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Tier.objects.filter(id=tier.id).exists())

    # def test_tiers_with_new_custom_images(self):
    #     """Test crating a custom images in tiers by normal user."""
    #     payload = {
    #         'title': 'Basic User',
    #         'description': 'Basic user account tier.',
    #         'custom_images': [{'name': 'Img'}, {'name': 'Image'}]
    #     }
    #
    #     res = self.client.post(TIERS_URL, payload, format='json')
    #
    #     self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    #     tier = models.Tier.objects.filter(user=self.user)
    #     self.assertEqual(tier.count(), 1)
    #     tiers = tier[0]
    #     self.assertEqual(tiers.custom_images.count(), 2)
    #     for customimages in payload['custom_images']:
    #         exists = tiers.custom_images.filter(
    #             name=customimages['name'],
    #             user=self.user,
    #         ).exists()
    #         self.assertTrue(exists)

    # def test_create_tier_with_existing_custom_images(self):
    #     """Test creating a tier with existing custom images."""
    #     custom_image1 = models.CustomImages.objects.create(user=self.user, name='Img1')
    #     payload = {
    #         'title': 'Basic User 2',
    #         'description': 'Basic user 2 account tier.',
    #         'custom_images': [
    #             {'name': 'Img1'},
    #             {'name': 'Image2'},
    #         ]
    #     }
    #
    #     res = self.client.post(TIERS_URL, payload, format='json')
    #
    #     self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    #     tiers = models.Tier.objects.filter(user=self.user)
    #     self.assertEqual(tiers.count(), 1)
    #     tiers = tiers[0]
    #     self.assertEqual(tiers.custom_images.count(), 2)
    #     self.assertIn(custom_image1, tiers.custom_images.all())
    #     for custom_images in payload['custom_images']:
    #         exists = tiers.custom_images.filter(
    #             name=custom_images['name'],
    #             user=self.user,
    #         ).exists()
    #         self.assertTrue(exists)

    def test_custom_images_list_limited_to_user(self):
        """Test list of custom images are limited to authenticated user."""
        other_user = create_user(email='other@example.com', password='test123')
        create_custom_images(user=other_user)
        create_custom_images(user=self.user)

        res = self.client.get(CUSTOM_IMAGES_URL)

        customs = models.CustomImages.objects.filter(user=self.user)
        serializer = serializers.BasicCustomImagesSerializer(customs, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_a_custom_image_on_update(self):
        """Test creating a custom image on updating a tier."""
        tiers = create_tier(user=self.user)

        payload = {'custom_images': [{'name': 'Image580'}]}
        url = detail_url(tiers.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_image = models.CustomImages.objects.get(user=self.user, name='Image580')
        self.assertIn(new_image, tiers.custom_images.all())

    def test_update_tier_assign_image(self):
        """Test assigning an existing custom image when updating a tier."""
        custom_image_15 = models.CustomImages.objects.create(user=self.user, name='Img15')
        tiers = create_tier(user=self.user)
        tiers.custom_images.add(custom_image_15)

        custom_image_20 = models.CustomImages.objects.create(user=self.user, name='Img20')
        payload = {'custom_images': [{'name': 'Img20'}]}
        url = detail_url(tiers.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(custom_image_20, tiers.custom_images.all())
        self.assertNotIn(custom_image_15, tiers.custom_images.all())

    def test_clear_tiers_custom_images(self):
        """Test clearing a tiers custom images."""
        custom_img = models.CustomImages.objects.create(user=self.user, name='Img1')
        tiers = create_tier(user=self.user)
        tiers.custom_images.add(custom_img)

        payload = {'custom_images': []}
        url = detail_url(tiers.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(tiers.custom_images.count(), 0)


class UploadImageTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'password123'
        )
        self.client.force_authenticate(self.user)
        self.customimages = create_custom_images(user=self.user)

    def tearDown(self):
        self.customimages.image.delete()

    def test_upload_image(self):
        """test"""
        url = image_upload_url(self.customimages.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.customimages.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.customimages.image.path))
