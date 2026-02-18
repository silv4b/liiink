from django.test import TestCase, Client
from django.urls import reverse
from links.tests.factory import UserFactory, LinkFactory


class PublicProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory(username="testuser")
        self.user.set_password("testpass123")
        self.user.save()
        LinkFactory(user=self.user, title="Test Link", url="https://example.com")
        self.url = reverse("public_profile", args=["testuser"])

    def test_public_profile_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Link")

    def test_public_profile_nonexistent_user(self):
        response = self.client.get(reverse("public_profile", args=["nonexistent"]))
        self.assertEqual(response.status_code, 404)
