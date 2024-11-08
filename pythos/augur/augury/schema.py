from typing import Any
from ninja import Schema
from pydantic import Json

class DreamStatusResponseSchema(Schema):
    status: str

class DreamDetailsRequestSchema(Schema):
    dream_id: int

class DreamDetailsResponseSchema(Schema):
    study_name: str
    study_id: int
    study_status: str
    dream_status: str

class DreamDivineRequestSchema(Schema):
    dream_id: int

class DreamCreateSchema(Schema):
    study_name: str
    study_conf: dict[str, Any]