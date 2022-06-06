"""
Serializers for tiers API.
"""
from rest_framework import serializers

from tiers.models import (
    Tier,
    CustomImages,
)


class BaseCustomImagesSerializer(serializers.ModelSerializer):
    """Base serializer for Custom Images serializers."""
    class Meta:
        model = CustomImages
        fields = ['id', 'name']
        read_only_fields = ['id']


class BasicCustomImagesSerializer(BaseCustomImagesSerializer):
    """Serializer of custom images for basic tier account."""
    link_200px = serializers.ImageField(read_only=True)

    class Meta(BaseCustomImagesSerializer.Meta):
        fields = BaseCustomImagesSerializer.Meta.fields + ['link_200px']


class PremiumCustomImagesSerializer(BaseCustomImagesSerializer):
    """Serializer of custom images for premium tier account."""
    link_200px = serializers.ImageField(read_only=True)
    link_400px = serializers.ImageField(read_only=True)

    class Meta(BaseCustomImagesSerializer.Meta):
        fields = BaseCustomImagesSerializer.Meta.fields + ['image',
                                                           'link_200px',
                                                           'link_400px']


class EnterpriseCustomImagesSerializer(BaseCustomImagesSerializer):
    """Serializer of custom images for enterprise tier account."""
    link_200px = serializers.ImageField(read_only=True)
    link_400px = serializers.ImageField(read_only=True)

    class Meta(BaseCustomImagesSerializer.Meta):
        fields = BaseCustomImagesSerializer.Meta.fields + ['link_200px',
                                                           'link_400px',
                                                           'expiring_link_val',
                                                           'expiring_link']

        read_only_fields = ['expiring_link']


class AdminCustomImagesSerializer(BaseCustomImagesSerializer):
    """Serializer of custom images for admin custom tier account."""
    custom_link = serializers.ImageField(read_only=True)

    class Meta(BaseCustomImagesSerializer.Meta):
        fields = BaseCustomImagesSerializer.Meta.fields + ['custom_expiring_link',
                                                           'custom_link',
                                                           'image']


class TierSerializer(serializers.ModelSerializer):
    """Serializer for Tiers"""
    custom_images = BaseCustomImagesSerializer(many=True, required=False)

    class Meta:
        model = Tier
        fields = ['id', 'title', 'description', 'custom_images']
        read_only_fields = ['__all__']

    def _get_or_create_custom_images(self, customimages, tiers):
        """Handle getting or creating custom images as needed."""
        auth_user = self.context['request'].user
        for custom_image in customimages:
            custom_images_obj, created = CustomImages.objects.get_or_create(
                user=auth_user,
                **custom_image,
            )
            tiers.custom_images.add(custom_images_obj)

    def create(self, validated_data):
        """Create a tier."""
        custom_images = validated_data.pop('custom_images', [])
        tiers = Tier.objects.create(**validated_data)
        self._get_or_create_custom_images(custom_images, tiers)

        return tiers

    def update(self, instance, validated_data):
        """Update tiers"""
        custom_images = validated_data.pop('custom_images', None)

        if custom_images is not None:
            instance.custom_images.clear()
            self._get_or_create_custom_images(custom_images, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class TierDetailSerializer(TierSerializer):
    """Serializer for tier detail view"""

    class Meta(TierSerializer.Meta):
        model = Tier
        fields = TierSerializer.Meta.fields


class CustomImagesImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to custom images."""

    class Meta:
        model = CustomImages
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}
