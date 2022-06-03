"""Tests for API tiers."""
from django.test import TestCase
from django.urls import reverse

from unittest.mock import patch

from tiers import models
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

TIERS_URL = reverse('tiers:tier-list')


def detail_url(tier_id):
    """Create and return a tier detail URL."""
    return reverse('tiers:tiers-detail', args=[tier_id])


def create_tier(user, **params):
    """Create and return a sample tier."""
    defaults = {
        'title': 'Sample tier title.',
        'description': 'Sample description',
    }
    defaults.update(params)

    tier = models.Tier.objects.create(user=user, **defaults)
    return tier


class PrivateTiersApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'password123',
        )
        self.client.force_authenticate(self.user)
        self.tiers = create_tier(user=self.user)

    def test_tiers_with_new_custom_images(self):
        """Test crating a custom images by tiers"""
        payload = {
            'title': 'Basic User',
            'description': 'Basic user account tier.',
            'custom_images': [
                {'name': 'Image1'},
                {'name': 'Image2'},
            ]
        }
        res = self.client.post(TIERS_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        tiers = models.Tier.objects.filter(user=self.user)
        self.assertEqual(tiers.count(), 1)
        tiers = tiers[0]
        self.assertEqual(tiers.custom_images.count(), 2)
        for custom_images in payload['custom_images']:
            exists = tiers.custom_images.filter(
                name=custom_images['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)

    def test_create_tier_with_existing_custom_images(self):
        """Test creating a tier with existing custom images."""
        custom_image1 = models.CustomImages.objects.create(user=self.user, name='Img1')
        payload = {
            'title': 'Basic User 2',
            'description': 'Basic user 2 account tier.',
            'custom_images': [
                {'name': 'Img1'},
                {'name': 'Image2'},
            ]
        }

        res = self.client.post(TIERS_URL, payload, formay='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        tiers = models.Tier.objects.filter(user=self.user)
        self.assertEqual(tiers.count(), 1)
        tiers = tiers[0]
        self.assertEqual(tiers.custom_images.count(), 2)
        self.assertIn(custom_image1, tiers.custom_images.all())
        for custom_images in payload['custom_images']:
            exists = tiers.custom_images.filter(
                name=custom_images['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)