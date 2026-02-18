import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from links.models import Profile, Link


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    primary_color = "#7c3aed"
    theme_preference = "system"


class LinkFactory(DjangoModelFactory):
    class Meta:
        model = Link

    user = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: f"Link {n}")
    url = factory.LazyAttribute(lambda obj: f"https://example{obj.id}.com")
    description = ""
    icon_name = "link"
