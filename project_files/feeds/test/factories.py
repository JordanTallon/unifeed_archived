import factory
from faker import Faker
from ..models import Feed

fake = Faker()


class FeedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Feed

    name = factory.LazyFunction(lambda: fake.catch_phrase())
    link = factory.LazyFunction(lambda: fake.url())
    url = factory.LazyFunction(lambda: fake.url())
    description = factory.LazyFunction(lambda: fake.paragraph())
    image_url = factory.LazyFunction(lambda: fake.image_url())
    author = factory.LazyFunction(lambda: fake.name())
    last_updated = factory.LazyFunction(lambda: fake.date_time())
