import datetime
import random
import factory
import factory.fuzzy

from core.factories import ImageryRequestFactory
from feasibility_finder.models import FeasibilityFinder, FeasibilityOrder, FeasibilityResult
from provider.factories import OrderFactory, ProviderFactory, ProviderIntegrationFactory


class FeasibilityFinderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FeasibilityFinder


    start_date = factory.LazyFunction(
        lambda: (datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(days=random.randint(1, 3)))
    )
    end_date = factory.LazyAttribute(
        lambda o: o.start_date + datetime.timedelta(days=random.randint(1, 3))
    )
    imagery_request = factory.SubFactory(ImageryRequestFactory)
    

class FeasibilityResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FeasibilityResult

    feasibility_finder = factory.SubFactory(FeasibilityFinderFactory)
    provider = factory.SubFactory(ProviderFactory)
    confidence_score = factory.fuzzy.FuzzyFloat(0, 100)

class FeasibilityOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FeasibilityOrder

    feasibility_result = factory.SubFactory(FeasibilityResultFactory)
    order = factory.SubFactory(OrderFactory)
    