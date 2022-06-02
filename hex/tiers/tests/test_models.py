from django.test import TestCase
from unittest.mock import patch
from tiers import models
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_tier(self):
        """Test creating a tier is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        tiers = models.Tier.objects.create(
            user=user,
            title='Sample tier name',
            description='Sample tier description.',
        )

        self.assertEqual(str(tiers), tiers.title)

    @patch('tiers.models.uuid.uuid4')
    def test_tier_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.tier_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/tier/{uuid}.jpg')