from utils.tests import faker
from .users import BaseUserFactory
from users.models import UserProfileModel
import factory


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfileModel
    

    user = factory.SubFactory(BaseUserFactory)
    posts_count = factory.LazyAttribute(lambda _: 0)
    subscription_count = factory.LazyAttribute(lambda _: 0)
    subscriber_count = factory.LazyAttribute(lambda _: 0)
    bio = factory.LazyAttribute(lambda _: f"{faker.unique.company()}")