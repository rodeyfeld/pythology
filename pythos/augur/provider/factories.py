import factory
import factory.fuzzy

from provider.models import Collection, Order, Provider, ProviderIntegration

class ProviderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Provider

    name = factory.Faker("word")

class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    name = factory.Faker("word")

class ProviderIntegrationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProviderIntegration

    name = factory.Faker("word")
    provider = factory.SubFactory(ProviderFactory)
    
class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    name = factory.Faker("word")
    provider_integration = factory.SubFactory(ProviderIntegrationFactory)
    