import factory
import factory.fuzzy
from django.utils import timezone
from faker import Faker
from ..models import Feed, UserFeed, FeedFolder

fake = Faker()


class FeedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Feed

    name = factory.LazyFunction(lambda: fake.catch_phrase()[:15])
    link = factory.LazyFunction(lambda: fake.url())
    url = factory.LazyFunction(lambda: fake.url())
    description = factory.LazyFunction(lambda: fake.paragraph())
    image_url = factory.LazyFunction(lambda: fake.image_url())
    publisher = factory.LazyFunction(lambda: fake.name())
    last_updated = factory.LazyFunction(
        lambda: timezone.make_aware(fake.date_time()))

    # Add 2 fake articles to each fake feed
    articles = factory.RelatedFactoryList(
        'articles.test.factories.ArticleFactory', factory_related_name='feed', size=2)


class FeedFolderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FeedFolder

    name = factory.LazyFunction(lambda: fake.catch_phrase()[:15])


class UserFeedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserFeed

    # must be defined when calling to create the factory
    user = None
    name = factory.LazyFunction(lambda: fake.catch_phrase()[:15])
    description = factory.LazyFunction(lambda: fake.paragraph())

    folder = factory.SubFactory(
        FeedFolderFactory, user=factory.SelfAttribute('..user'))
    feed = factory.SubFactory(FeedFactory)
