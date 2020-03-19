from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Profile


class ProfileCreation(TestCase):
    """Test the model Profile"""

    def create_user(self):
        """Create a user for testing purpose"""
        user_info = {
            "username": "test_user",
            "email": "user@test.com",
            "password": "test_user_password"}
        return User.objects.create_user(**user_info)


    def test_profile_creation(self):
        """Test if a user and a profile are created"""
        user = self.create_user()
        self.assertIsInstance(user, User)
        self.assertIsInstance(user.profile, Profile)
        self.assertEqual(user.profile.__str__(), user.username)
