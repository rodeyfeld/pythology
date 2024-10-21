import random
import factory
import factory.fuzzy
import factory.random
from core.models import ImageryRequest, IntegrationConfigOption, InternalIntegration, Organization, User




class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Faker("word")
    

class ConfigOptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IntegrationConfigOption
    
    key = factory.fuzzy.FuzzyChoice(IntegrationConfigOption.ConfigFieldChoices, getter=lambda c: c[0])
    value = factory.Faker("word")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    name = factory.Faker("word")
    username = factory.lazy_attribute(lambda o: f"{o.name}_{random.randint(0,99999999)}")
    organization = factory.SubFactory(OrganizationFactory)
    email = factory.lazy_attribute(lambda o: f"{o.username}@{o.organization.name if o.organization else 'spacemail.com'}")

class ImageryRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ImageryRequest

    user = factory.SubFactory(UserFactory)
    name = factory.Faker("word")
    geometry = factory.Faker("word")


class InternalIntegrationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InternalIntegration

    name = factory.Faker("word")
    