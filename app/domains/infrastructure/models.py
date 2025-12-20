"""SQL ORM Models for data pulls from db"""

from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import Mapped

from app.core.database import Base

# ============================================
# Naming convention > FolderName + TableDescription (e.g. InfrastructureVMs)


class InfrastructureVMs(Base):
    __tablename__ = "v_infra_vms"
    __table_args__ = (PrimaryKeyConstraint("vm_name", "fisc_wk"),)  # Must be in tuple format with comma

    vm_name: Mapped[str]
    fisc_wk: Mapped[str]
    fisc_yr: Mapped[str | None]
    cost: Mapped[float | None]
    role: Mapped[str | None]
