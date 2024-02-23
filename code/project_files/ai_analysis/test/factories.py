import factory
from faker import Faker
from ..models import ArticleAnalysisResults
import random

fake = Faker()


class ArticleAnalysisResultsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ArticleAnalysisResults

    article_url = factory.LazyFunction(lambda: fake.url())
    article_text_md5 = factory.LazyFunction(lambda: fake.md5())
    sentence_results = factory.LazyFunction(
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
