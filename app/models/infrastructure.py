"""SQL ORM Models for infrastructure data pulls"""

from typing import Optional

from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import Mapped

from app.models.base import Base


class InfrastructureVMs(Base):
    __tablename__ = "v_infra_vms"
    __table_args__ = PrimaryKeyConstraint("vm_name", "fisc_wk")

    vm_name: Mapped[str]
    fisc_wk: Mapped[str]
    fisc_yr: Mapped[Optional[str]]
    cost: Mapped[Optional[float]]
    role: Mapped[Optional[str]]
