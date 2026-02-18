from django.test import TestCase, Client
from django.urls import reverse
from links.tests.factory import UserFactory
import json


class SetThemePreferenceViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.user.set_password("testpass123")
        self.user.save()
        self.url = reverse("set_theme_preference")

    def test_set_theme_requires_login(self):
        response = self.client.post(
            self.url, json.dumps({"theme": "dark"}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 302)

    def test_set_theme_success(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.post(
            self.url, json.dumps({"theme": "dark"}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["theme"], "dark")

    def test_set_theme_invalid_theme(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.post(
            self.url, json.dumps({"theme": "invalid"}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data["success"])

    def test_set_theme_missing_theme(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.post(
            self.url, json.dumps({}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
