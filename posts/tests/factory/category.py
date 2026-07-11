import factory

from posts.models import Category


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category

    name = factory.Sequence(
        lambda n: f"Category {n}"
    )