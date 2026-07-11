from users.models import OtpCode
from users.tests.factories.users import BaseUserFactory

import factory


class OtpFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = OtpCode

    user = factory.SubFactory(
        BaseUserFactory
    )

    code = factory.Faker(
        "numerify",
        text="######",
    )

    is_used = False