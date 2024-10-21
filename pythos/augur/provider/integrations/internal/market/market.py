

import requests
from core.models import IntegrationConfigOption
from feasibility_finder.factories import FeasibilityOrderFactory
from provider.factories import OrderFactory
from provider.integrations.integration import InteractiveProvider
from provider.integrations.internal.market.schema import MarketTaskingOrderRequestSchema, MarketTaskingOrderResponseSchema
from provider.models import Order


class InteractiveMarket(InteractiveProvider):

    def task_order(self, feasibility_result):
        order = OrderFactory.create(
            name=feasibility_result.feasibility_finder.imagery_request.name,
            provider_integration=self.provider_integration,
        )
        feasibility_order = FeasibilityOrderFactory.create(
            order=order,
            feasibility_result=feasibility_result
        )
        payload = MarketTaskingOrderRequestSchema(
            geometry="some geom",
            imaging_mode="SPOTLIGHT",
            task_name="test name",
            satellite_ids="",
            start_date=feasibility_result.start_date,
            end_date=feasibility_result.end_date,
        )
        task_endpoint = self.config_options.get(key=IntegrationConfigOption.ConfigFieldChoices.TASK_ENDPOINT)
        url = task_endpoint.value
        response = requests.post(url=url, json=payload.model_dump_json())
        data = response.json()
        market_tasking_order_response = MarketTaskingOrderResponseSchema(
            id=data['id'],
            properties=data['properties'],
        )        
        order.external_id = market_tasking_order_response.id
        order.status = Order.Status.ORDERED 
        order.save()

        feasibility_order.metadata = market_tasking_order_response.properties
        feasibility_order.save()
        return order
        



    def feasibility_search():
        pass


    def archive_search():
        pass


    def task_order_status():
        pass


    def task_download():
        pass
