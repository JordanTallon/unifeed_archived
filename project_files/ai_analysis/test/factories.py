import factory
from faker import Faker
from ..models import PoliticalBiasAnalysis
import random

fake = Faker()


class PoliticalBiasAnalysisFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PoliticalBiasAnalysis

    article_url = factory.LazyFunction(lambda: fake.url())
    article_text_md5 = factory.LazyFunction(lambda: fake.md5())
    biased_sentences = factory.LazyFunction(
        lambda: [
            {
                "text": fake.sentence(),
                "bias": {
                    "left": random.uniform(0, 1),
                    "center": random.uniform(0, 1),
                    "right": random.uniform(0, 1)
                }
            }
            for _ in range(5)
        ]
    )
