"""
Serializers for the user API View.
"""

from django.contrib.auth import (
    get_user_model,
    authenticate,

)
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes


class BaseUserSerializer(serializers.ModelSerializer):
    """Base user serializer for user attributes."""
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return updated user records."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserSerializer(BaseUserSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'account_plan']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}


class AdminUserSerializer(serializers.ModelSerializer):
    """Admin user can update every field"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'account_plan']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}


class NormalUserSerializer(serializers.ModelSerializer):
    """NonAdmin user can't update account_plan"""
    class Meta:
        model = get_user_model()
        # fields = ['email', 'password', 'name' ]
        # read_only_fields = ['account_plan']
        exclude = ['account_plan']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}



class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs