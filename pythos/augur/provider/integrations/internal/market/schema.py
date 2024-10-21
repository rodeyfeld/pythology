from datetime import datetime
from ninja import Schema


class MarketTaskingOrderRequestSchema(Schema):
    geometry: str
    imaging_mode: str 
    task_name: str
    satellite_ids: str
    start_date: datetime
    end_date: datetime

class MarketTaskingOrderResponseSchema(Schema):
    id: str
    properties: str