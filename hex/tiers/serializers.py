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
        fields = ['id', 'title', 'description', 'image']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a tier."""
        tiers = Tier.objects.create(**validated_data)
        return tiers

    def update(self, instance, validated_data):
        """Update tiers"""
        tiers = super().update(instance, validated_data)
        return tiers


class TierDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tier
        fields = ['id', 'title', 'description', 'link', 'image']

    # def create(self, validated_data):
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance


class TierImageSerializer(serializers.ModelSerializer):
    model = Tier
    fields = ['id', 'image']
    read_only_fields = ['id']
    extra_kwargs = {'image': {'required': True}}