from pydantic import BaseModel, ValidationError, field_validator
from typing import List, Optional

class ItemPayload(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    tags: Optional[List[str]] = None

    @field_validator("name")
    @classmethod
    def name_len(cls, v):
        if not (1 <= len(v) <= 100):
            raise ValueError("name length 1..100 required")
        return v

    @field_validator("price")
    @classmethod
    def price_gt_zero(cls, v):
        if v <= 0:
            raise ValueError("price must be > 0")
        return v

    @field_validator("description")
    @classmethod
    def desc_len(cls, v):
        if v is not None and len(v) > 500:
            raise ValueError("description <= 500")
        return v

    @field_validator("tags")
    @classmethod
    def tags_rule(cls, v):
        if v is not None and len(v) > 10:
            raise ValueError("max 10 tags")
        return v
