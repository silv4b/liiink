from django.test import TestCase, Client
from django.urls import reverse
from links.tests.factory import UserFactory
from django.contrib.auth.models import User


class DeleteAccountViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.user.set_password("testpass123")
        self.user.save()
        self.url = reverse("delete_account")

    def test_delete_account_requires_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_delete_account_get_renders_template(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "links/delete_account.html")

    def test_delete_account_without_password(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.post(self.url, {"password": ""})
        self.assertRedirects(response, reverse("profile"))

    def test_delete_account_wrong_password(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.post(self.url, {"password": "wrongpassword"})
        self.assertRedirects(response, reverse("profile"))

    def test_delete_account_success(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.post(self.url, {"password": "testpass123"})
        self.assertRedirects(response, reverse("home"))
        self.assertFalse(User.objects.filter(username=self.user.username).exists())

    def test_delete_account_ajax_without_password(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.post(
            self.url, {"password": ""}, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertIn("senha", data["error"].lower())

    def test_delete_account_ajax_wrong_password(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.post(
            self.url,
            {"password": "wrongpassword"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data["success"])

    def test_delete_account_ajax_success(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.post(
            self.url,
            {"password": "testpass123"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("sucesso", data["message"].lower())
        self.assertFalse(User.objects.filter(username=self.user.username).exists())
