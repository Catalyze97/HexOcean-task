"""
Test for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create and return new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_crete_user_with_email_successful(self):
        """Testing creating a user with an email, password and permissions is successful."""
        email = 'test@example.com'
        password = 'password123'
        account_plan = 'bp'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            account_plan=account_plan,

        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.account_plan, account_plan)

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raiser_error(self):
        """Test that creating a user without an email raised ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_new_user_without_perm_raiser_error(self):
        """Test that creating a user without a permissions """
        account_plan = ''
        user = get_user_model().objects.create_user(
            email='email@example.com',
            password='password123',
            account_plan='bp',
        )
        self.assertNotEqual(user.account_plan, account_plan)

    def test_create_superuser(self):
        """Test crating a superuser."""
        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
