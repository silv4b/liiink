from django.test import TestCase, Client
from django.urls import reverse
from links.tests.factory import UserFactory, LinkFactory


class DeleteLinkViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.user.set_password("testpass123")
        self.user.save()
        self.link = LinkFactory(
            user=self.user, title="Test Link", url="https://example.com"
        )
        self.url = reverse("delete_link", args=[self.link.id])

    def test_delete_link_requires_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_delete_link_success(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("dashboard"))
        self.assertEqual(LinkFactory._meta.model.objects.count(), 0)

    def test_delete_link_wrong_user(self):
        other_user = UserFactory(username="other")
        other_user.set_password("otherpass123")
        other_user.save()
        self.client.login(username="other", password="otherpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)


class EditLinkViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.user.set_password("testpass123")
        self.user.save()
        self.link = LinkFactory(
            user=self.user, title="Old Title", url="https://old.com"
        )
        self.url = reverse("edit_link", args=[self.link.id])

    def test_edit_link_requires_login(self):
        response = self.client.post(
            self.url, {"title": "New", "url": "https://new.com"}
        )
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_edit_link_success(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.post(
            self.url,
            {
                "title": "New Title",
                "url": "https://new.com",
                "description": "New description",
                "icon_name": "star",
            },
        )
        self.assertRedirects(response, reverse("dashboard"))
        self.link.refresh_from_db()
        self.assertEqual(self.link.title, "New Title")
        self.assertEqual(self.link.url, "https://new.com")

    def test_edit_link_without_title(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.post(self.url, {"title": "", "url": "https://new.com"})
        self.link.refresh_from_db()
        self.assertEqual(self.link.title, "Old Title")

    def test_edit_link_without_url(self):
        self.client.login(username=self.user.username, password="testpass123")
        response = self.client.post(self.url, {"title": "New Title", "url": ""})
        self.link.refresh_from_db()
        self.assertEqual(self.link.url, "https://old.com")
