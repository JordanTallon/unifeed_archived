import factory
from faker import Faker
from django.utils import timezone
from ..models import Article
from feeds.test.factories import FeedFactory

fake = Faker()


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    title = factory.LazyFunction(lambda: fake.catch_phrase())
    link = factory.LazyFunction(lambda: fake.url())
    description = factory.LazyFunction(lambda: fake.paragraph())
    image_url = factory.LazyFunction(lambda: fake.image_url())
    author = factory.LazyFunction(lambda: fake.name())
    publish_datetime = factory.LazyFunction(
        lambda: timezone.make_aware(fake.date_time()))
    feed = factory.SubFactory(FeedFactory)
