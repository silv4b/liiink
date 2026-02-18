from django.test import TestCase, Client
from django.urls import reverse
from links.tests.factory import UserFactory


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.user.set_password("testpass123")
        self.user.save()

    def test_home_redirects_authenticated_user_to_dashboard(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.get(reverse("home"))
        self.assertRedirects(response, reverse("dashboard"))

    def test_home_renders_for_anonymous_user(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "links/home.html")
