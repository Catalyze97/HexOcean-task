from unittest.mock import patch
from tiers import models


@patch('core.models.uuid.uuid4')
def test_tier_file_name_uuid(self, mock_uuid):
    """Test generating image path."""
    uuid = 'test-uuid'
    mock_uuid.return_value = uuid
    file_path = models.tier_image_file_path(None, 'example.jpg')

    self.assertEqual(file_path, f'uploads/tier/{uuid}.jpg')