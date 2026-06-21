from django.test import TestCase
from django.contrib.auth.models import User
from .models import Scan, UrlScan


class ScanModelTest(TestCase):
    """Tests for the database models."""

    def setUp(self):
        # runs before each test: create a user to work with
        self.user = User.objects.create_user(username="tester", password="pass12345")

    def test_scan_is_created(self):
        # create a file scan and check it is saved correctly
        scan = Scan.objects.create(
            user=self.user,
            file_name="virus.exe",
            file_hash="abc123",
            verdict="Clean",
        )
        self.assertEqual(scan.file_name, "virus.exe")
        self.assertEqual(Scan.objects.count(), 1)

    def test_badge_class_for_verdicts(self):
        # the badge_class() method should return the right CSS class
        clean = Scan.objects.create(user=self.user, file_name="a", file_hash="h", verdict="Clean")
        danger = Scan.objects.create(user=self.user, file_name="b", file_hash="h", verdict="Dangerous (3 engines)")
        unknown = Scan.objects.create(user=self.user, file_name="c", file_hash="h", verdict="Unknown")

        self.assertEqual(clean.badge_class(), "badge-clean")
        self.assertEqual(danger.badge_class(), "badge-danger")
        self.assertEqual(unknown.badge_class(), "badge-unknown")


class HomePageTest(TestCase):
    """Tests for the home page access control."""

    def test_home_requires_login(self):
        # a guest visiting "/" should be redirected (to the login page)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_home_works_when_logged_in(self):
        # a logged-in user should see the page (status 200 = OK)
        User.objects.create_user(username="tester", password="pass12345")
        self.client.login(username="tester", password="pass12345")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)