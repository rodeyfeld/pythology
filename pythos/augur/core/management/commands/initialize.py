from django.core.management.base import BaseCommand

from core.factories import ConfigOptionFactory, InternalIntegrationFactory, UserFactory
from core.models import IntegrationConfigOption


INTERNAL_INTEGRATION_NAME = 'oracle'


class Command(BaseCommand):

    help = "Initializes database for testing purposes"
    def handle(self, *args, **options):
        # if no superuser exists, create it

        if not UserFactory._meta.model.objects.filter(is_superuser=True):
            UserFactory.create(username="admin", email="admin@augur.com", password="admin", is_superuser=True)


        if not InternalIntegrationFactory._meta.model.objects.filter(name=INTERNAL_INTEGRATION_NAME):
            internal_integration = InternalIntegrationFactory.create(
                name=INTERNAL_INTEGRATION_NAME,
                
            )
            
            generic_endpoint_config, _ = IntegrationConfigOption.get_or_create(
                key=ConfigOptionFactory._meta.model.ConfigFieldChoices.GENERIC_ENDPOINT,
                value="http://127.0.0.1:7777"
            )
            stac_endpoint_config, _ = IntegrationConfigOption.get_or_create(
                key=ConfigOptionFactory._meta.model.ConfigFieldChoices.STAC_ENDPOINT,
                value="http://127.0.0.1:7777/attendPast"
            )

            internal_integration.config_options.add(generic_endpoint_config)
            internal_integration.config_options.add(stac_endpoint_config)
            
