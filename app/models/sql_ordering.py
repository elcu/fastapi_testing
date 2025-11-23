"""SQL orm models for Ordering_Sims data pulls"""

from __future__ import annotations

from datetime import date
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from idea_api.db.database import Base


class SrfOrderDetails(Base):
    """Represents monthly capex costs in database"""

    __tablename__ = "V_iDEAAPI_SRF_Order_Details"  # table name in the database

    srf_number: Mapped[Optional[str]]
    order_number: Mapped[Optional[str]] = mapped_column(primary_key=True, nullable=True)
    bu_id: Mapped[Optional[int]]
    tracking_link: Mapped[Optional[str]]
    service_tags: Mapped[Optional[str]]
    order_status: Mapped[Optional[str]]
    order_date: Mapped[Optional[date]]
    cancel_date: Mapped[Optional[date]]
    cancel_reason: Mapped[Optional[str]]
    estimated_ship_date: Mapped[Optional[date]]
    shipped_date: Mapped[Optional[date]]
    estimated_delivery_date: Mapped[Optional[date]]
    delivery_date: Mapped[Optional[date]]
    revised_ship_date: Mapped[Optional[date]]
    revised_delivery_date: Mapped[Optional[date]]
    delivery_status: Mapped[Optional[str]]
