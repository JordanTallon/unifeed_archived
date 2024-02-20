import factory
import factory.fuzzy
from django.utils import timezone
from faker import Faker
from ..models import Feed, UserFeed, FeedFolder

fake = Faker()


class FeedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Feed

    name = factory.LazyFunction(lambda: fake.catch_phrase())
    link = factory.LazyFunction(lambda: fake.url())
    url = factory.LazyFunction(lambda: fake.url())
    description = factory.LazyFunction(lambda: fake.paragraph())
    image_url = factory.LazyFunction(lambda: fake.image_url())
    publisher = factory.LazyFunction(lambda: fake.name())
    last_updated = factory.LazyFunction(
        lambda: timezone.make_aware(fake.date_time()))


class FeedFolderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FeedFolder

    name = factory.LazyFunction(lambda: fake.catch_phrase())


class UserFeedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Feed

    name = factory.LazyFunction(lambda: fake.catch_phrase())
    description = factory.LazyFunction(lambda: fake.paragraph())

    folder = factory.SubFactory(FeedFolderFactory)
    feed = factory.SubFactory(FeedFactory)
