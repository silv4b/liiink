from django.test import TestCase, Client
from django.urls import reverse
from links.tests.factory import UserFactory


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.user.set_password("testpass123")
        self.user.save()
        self.url = reverse("profile")

    def test_profile_requires_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_profile_displays_settings(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "primary_color")

    def test_profile_update_color(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.post(
            self.url, {"primary_color": "#00FF00", "theme_preference": "dark"}
        )
        self.assertRedirects(response, self.url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.primary_color, "#00FF00")

    def test_profile_update_theme(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.post(
            self.url, {"primary_color": "#000000", "theme_preference": "light"}
        )
        self.assertRedirects(response, self.url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.theme_preference, "light")

    def test_profile_invalid_theme_ignored(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.post(self.url, {"theme_preference": "invalid"})
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.profile.theme_preference, "invalid")
