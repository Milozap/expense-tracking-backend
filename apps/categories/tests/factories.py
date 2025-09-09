import uuid

import factory
from django.utils.text import slugify

from apps.categories.models import Category


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")
    type = factory.Iterator([t for (t, _) in Category.TYPE_CHOICES])
    parent = None
    slug = factory.LazyAttribute(
        lambda o: f"test-{slugify(o.name)}-{uuid.uuid4().hex[:8]}"
    )
    color = factory.Faker("hex_color")
