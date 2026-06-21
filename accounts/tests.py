from django.test import TestCase
from django.contrib.auth.models import User


class RegistrationTest(TestCase):
    """Tests for user registration."""

    def test_user_can_register(self):
        # send a POST to the register page with valid data
        response = self.client.post("/accounts/register/", {
            "username": "newuser",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
        })
        # after successful registration the user should exist in the database
        self.assertTrue(User.objects.filter(username="newuser").exists())