import datetime
import random
import factory
import factory.fuzzy

from archive_finder.models import ArchiveFinder, ArchiveOrder, ArchiveResult
from provider.factories import OrderFactory, CollectionFactory
from django.contrib.gis.geos import Point

class ArchiveFinderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ArchiveFinder


    start_date = factory.LazyFunction(
        lambda: (datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(days=random.randint(1, 3)))
    )
    end_date = factory.LazyAttribute(
        lambda o: o.start_date + datetime.timedelta(days=random.randint(1, 3))
    )
    geometry = factory.LazyFunction(Point(0, 0))
    
class ArchiveResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ArchiveResult

    archive_finder = factory.SubFactory(ArchiveFinderFactory)
    collection = factory.SubFactory(CollectionFactory)

    start_date = factory.LazyAttribute(
        lambda o: o.archive_finder.start_date + datetime.timedelta(seconds=random.randint(1, 3))
    )
    end_date = factory.LazyAttribute(
        lambda o: o.start_date + datetime.timedelta(seconds=random.randint(1, 3))
    )

class ArchiveOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ArchiveOrder

    order = factory.SubFactory(OrderFactory)
    archive_result = factory.SubFactory(ArchiveResultFactory)
    