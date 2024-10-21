from typing import List
from ninja import Router

from feasibility_finder.models import FeasibilityResult
from provider.integrations.integration import get_interactive_providers
from provider.schema import ProviderIntegrationOrderRequestSchema, ProviderIntegrationOrderResponseSchema, ProviderIntegrationSchema, ProviderSchema
from .models import Provider, ProviderIntegration

router = Router(tags=["providers"])


@router.get('/', response=List[ProviderSchema])
def list_all_providers(request):
    queryset = Provider.objects.all()
    return list(queryset)
    
@router.get('/id/{provider_id}', response=ProviderSchema)
def list_provider_by_id(request, provider_id):
    queryset = Provider.objects.get(id=provider_id)
    return queryset

@router.get('/integrations', response=List[ProviderIntegrationSchema])
def list_all_provider_integrations(request):
    queryset = ProviderIntegration.objects.all()
    return list(queryset)
    
@router.get('/integrations/id/provider_integration/{provider_integration_id}', response=ProviderIntegrationSchema)
def list_provider_integration_by_id(request, provider_integration_id):
    queryset = ProviderIntegration.objects.get(id=provider_integration_id)
    return queryset

@router.get('/integrations/id/provider/{provider_id}', response=ProviderIntegrationSchema)
def list_provider_integrations_by_provider_id(request, provider_id):
    queryset = ProviderIntegration.objects.filter(provider_id=provider_id)
    return queryset



@router.post('/integrations/order/tasking', response=ProviderIntegrationOrderResponseSchema)
def provider_integration_order(request, order_request_schema: ProviderIntegrationOrderRequestSchema):
    queryset = ProviderIntegration.objects.filter(name=order_request_schema.provider_integration_name).first()
    interactive_provider = get_interactive_providers()[queryset.name](queryset)
    feasbility_result = FeasibilityResult.objects.get(pk=order_request_schema.feasibility_result_id)
    order = interactive_provider.task_order(feasbility_result)

    response = ProviderIntegrationOrderResponseSchema(
        status=order.status
    )
    return response
