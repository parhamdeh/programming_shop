import factory

from utils.tests import faker
from users.models import BaseUserModel
from utils.models import BaseModel


from django.utils import timezone
from phonenumber_field.phonenumber import PhoneNumber


class BaseUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BaseUserModel
    
     
    username = factory.Sequence(lambda n: f"user{n}")
    phone = factory.Sequence(
        lambda n: PhoneNumber.from_string(
            phone_number=f"0912000{n:04}",
            region="IR",
        )
    )
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')


class SuperUserFactory(BaseUserFactory):

    is_staff = True

    is_superuser = True