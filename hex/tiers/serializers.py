"""
Serializers for tiers API.
"""
from rest_framework import serializers

from tiers.models import Tier
from core.models import User


class TierSerializer(serializers.ModelSerializer):
    """Serializer for Tiers"""

    class Meta:
        model = Tier
        fields = ['id', 'title', 'description', 'link']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a tier."""

        tiers = Tier.objects.create(**validated_data)
        return tiers

    def update(self, instance, validated_data):
        """Update tiers"""
        tiers = super().update(instance, validated_data)
        return tiers


class TierDetailSerializer(TierSerializer.Meta):
    """Serializer for tier detail view"""
    class Meta:
        model = Tier
        fields = TierSerializer.Meta.fields + ['image']


class TierImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to tiers."""
    class Meta:
        model = Tier
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}


