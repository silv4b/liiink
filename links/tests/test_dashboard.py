from django.test import TestCase, Client
from django.urls import reverse
from links.tests.factory import UserFactory, LinkFactory


class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.user.set_password("testpass123")
        self.user.save()
        self.url = reverse("dashboard")

    def test_dashboard_requires_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_dashboard_displays_links(self):
        self.client.login(username=self.user.username, password="testpass123")
        LinkFactory(user=self.user, title="Test Link", url="https://example.com")
        response = self.client.get(self.url)
        self.assertContains(response, "Test Link")

    def test_dashboard_add_link_success(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.post(
            self.url,
            {
                "action": "add_link",
                "title": "New Link",
                "url": "https://example.com",
                "description": "Test description",
                "icon_name": "link",
            },
        )
        self.assertRedirects(response, self.url)
        self.assertEqual(LinkFactory._meta.model.objects.count(), 1)

    def test_dashboard_add_link_without_title(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.post(
            self.url, {"action": "add_link", "title": "", "url": "https://example.com"}
        )
        self.assertEqual(LinkFactory._meta.model.objects.count(), 0)

    def test_dashboard_add_link_without_url(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.post(
            self.url, {"action": "add_link", "title": "Test Link", "url": ""}
        )
        self.assertEqual(LinkFactory._meta.model.objects.count(), 0)

    def test_dashboard_link_limit_reached(self):
        self.client.login(username=self.user.username, password="testpass123")
        for i in range(6):
            LinkFactory(
                user=self.user, title=f"Link {i}", url=f"https://example{i}.com"
            )

        response = self.client.post(
            self.url,
            {"action": "add_link", "title": "Extra Link", "url": "https://extra.com"},
        )
        self.assertEqual(LinkFactory._meta.model.objects.count(), 6)

    def test_dashboard_update_profile_color(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.post(
            self.url, {"action": "update_profile", "primary_color": "#FF0000"}
        )
        self.assertRedirects(response, self.url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.primary_color, "#FF0000")
