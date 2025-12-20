"""Pydantic ordering models"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrderDetails(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    srf_number: Optional[str]
    order_number: Optional[str]
    bu_id: Optional[int]
    tracking_link: Optional[str]
    service_tags: Optional[str]
    order_status: Optional[str]
    order_date: Optional[date]
    cancel_date: Optional[date]
    cancel_reason: Optional[str]
    estimated_ship_date: Optional[date]
    shipped_date: Optional[date]
    estimated_delivery_date: Optional[date]
    delivery_date: Optional[date]
    revised_ship_date: Optional[date]
    revised_delivery_date: Optional[date]
    delivery_status: Optional[str]
