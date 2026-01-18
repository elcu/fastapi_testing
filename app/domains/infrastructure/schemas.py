"""Pydantic validation models"""

from app.core.schemas import BaseSchema

# ============================================
# Naming convention > FolderName + Purpose / Detail (e.g. InfrastructureVMsBase)


class InfrastructureVMsBase(BaseSchema):
    """Base schema that configures all fields available for the data that are being pulled from db."""

    vm_name: str
    fisc_wk: str
    fisc_yr: str | None
    cost: float | None
    role: str | None


class InfrastructureVMsBasePydantic(BaseSchema):
    """Extension of base schema that is being used in endpoint which returns Pydantic model."""

    count: int
    total: int
    skip: int
    limit: int
    data: list[InfrastructureVMsBase]


class InfrastructureVMsIn(BaseSchema):
    """Validation for incoming payload from user."""

    vm_name: list[str]
    fisc_wk: str


class InfrastructureVMsOut(BaseSchema):
    """Validation for outcoming payload to user."""

    count: int
    data: list[InfrastructureVMsBase]
