from django.core.management.base import BaseCommand

from core.factories import ConfigOptionFactory, InternalIntegrationFactory, UserFactory
from core.models import IntegrationConfigOption, InternalIntegration


INTERNAL_INTEGRATION_NAME = 'oracle'


class Command(BaseCommand):

    help = "Initializes database for testing purposes"
    def handle(self, *args, **options):
        # if no superuser exists, create it

        if not UserFactory._meta.model.objects.filter(is_superuser=True):
            UserFactory.create(username="admin", email="admin@augur.com", password="admin", is_superuser=True)


        internal_integration, _ = InternalIntegration.objects.get_or_create(
            name=INTERNAL_INTEGRATION_NAME,   
        )
        
        generic_endpoint_config, created = IntegrationConfigOption.objects.get_or_create(
            key=ConfigOptionFactory._meta.model.ConfigFieldChoices.GENERIC_ENDPOINT,
            value="http://127.0.0.1:7777"
        )
        if created:
            internal_integration.config_options.add(generic_endpoint_config)

        stac_endpoint_config, created = IntegrationConfigOption.objects.get_or_create(
            key=ConfigOptionFactory._meta.model.ConfigFieldChoices.STAC_ENDPOINT,
            value="http://127.0.0.1:7777/attendPast"
        )
        if created:
            internal_integration.config_options.add(stac_endpoint_config)
            
