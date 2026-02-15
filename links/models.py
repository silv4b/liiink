from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_max_links(user):
    if Link.objects.filter(user=user).count() >= 6:
        raise ValidationError("You can only have up to 6 links.")


class Profile(models.Model):
    THEME_CHOICES = [
        ("light", "Light"),
        ("dark", "Dark"),
        ("system", "System"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    primary_color = models.CharField(max_length=7, default="#7c3aed")  # Hex color
    theme_preference = models.CharField(
        max_length=10, choices=THEME_CHOICES, default="system"
    )

    def __str__(self):
        return f"Profile of {self.user.username}"


class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="links")
    title = models.CharField(max_length=100)
    url = models.URLField(max_length=500)
    description = models.CharField(max_length=200, blank=True, null=True)
    icon_name = models.CharField(max_length=50, default="link")  # Lucide icon name
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Only check on creation
            validate_max_links(self.user)
        super().save(*args, **kwargs)
