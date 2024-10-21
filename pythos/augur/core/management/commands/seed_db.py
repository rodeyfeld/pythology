import random
from django.core.management.base import BaseCommand, CommandError

from core.factories import ImageryRequestFactory, OrganizationFactory, UserFactory
from core.models import User
from feasibility_finder.factories import FeasibilityFinderFactory, FeasibilityResultFactory
from provider.factories import ConfigOptionFactory, ProviderFactory, ProviderIntegrationFactory


class Command(BaseCommand):

    help = "Initializes database for testing purposes"
    def handle(self, *args, **options):

        # create 5 random organizations, at least one active
        organizations = OrganizationFactory.create_batch(1)
        organizations += OrganizationFactory.create_batch(4, is_active=random.choice((True, False)))

        # create 50 random users, 10 with no organization
        users = UserFactory.create_batch(10, organization=None)
        for _ in range(40):
            users.append(UserFactory.create(organization=random.choice(organizations)))


        imagery_requests = []
        for _ in range(1000):
            imagery_requests.append(ImageryRequestFactory.create(user=random.choice(users)))


        providers = ProviderFactory.create_batch(10)
        provider_integrations = []
        for provider in providers:
            provider_integrations.append(ProviderIntegrationFactory.create(provider=provider))
        

        feasibility_finders = []
        for imagery_request in imagery_requests:
            feasibility_finders.append(FeasibilityFinderFactory.create(imagery_request=imagery_request))
        

        feasibility_results = []
        for feasibility_finder in feasibility_finders:
            for provider_integration in provider_integrations:
                if random.random() <= .8:
                    feasibility_results.append(FeasibilityResultFactory(feasibility_finder=feasibility_finder, provider_integration=provider_integration))