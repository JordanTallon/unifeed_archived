import factory
from faker import Faker
from ..models import PoliticalBiasAnalysis

fake = Faker()


class PoliticalBiasAnalysisFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PoliticalBiasAnalysis

    article_url = factory.LazyFunction(lambda: fake.url())
    article_text_md5 = factory.LazyFunction(lambda: fake.md5())
    political_bias = factory.LazyFunction(
        lambda: fake.random_int(min=1, max=100))
