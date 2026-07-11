import factory
from posts.models import Comments, FavoritPost, Post

from posts.tests.factory.category import CategoryFactory
from users.tests.factories.users import BaseUserFactory

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(BaseUserFactory)

    category = factory.SubFactory(
        CategoryFactory
    )

    title = factory.Sequence(
        lambda n: f"Post {n}"
    )

    content = factory.Faker("paragraph")

    is_premium = False


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comments

    author = factory.SubFactory(BaseUserFactory)

    post = factory.SubFactory(PostFactory)

    content = factory.Faker("sentence")


class FavoritePostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FavoritPost

    user = factory.SubFactory(BaseUserFactory)

    post = factory.SubFactory(PostFactory)