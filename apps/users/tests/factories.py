import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("username")
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: make_password("pi3.1415"))
    is_staff = True
    is_superuser = True


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: make_password("SecurePass123!"))
    is_staff = False
    is_superuser = False
