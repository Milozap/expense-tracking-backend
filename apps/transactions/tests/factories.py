import factory

from apps.categories.models import Category
from apps.categories.tests.factories import CategoryFactory
from apps.transactions.models import Transaction
from apps.users.factories import SuperUserFactory


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    date = factory.Faker("date")
    amount = factory.Faker("pydecimal", left_digits=6, right_digits=2)
    description = factory.Faker("sentence")
    type = factory.Iterator([t for (t, _) in Category.TYPE_CHOICES])
    user_id = factory.SubFactory(SuperUserFactory)
    category = factory.SubFactory(CategoryFactory)
