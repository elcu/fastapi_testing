"""Pydantic validation models"""

from app.core.schemas import BaseSchema

# ============================================
# Naming convention > FolderName + RouterEndpoint (e.g. InfrastructureVMsAll)


class InfrastructureVMsAll(BaseSchema):

    vm_name: str
    fisc_wk: str
    fisc_yr: str | None
    cost: float | None
    role: str | None


class InfrastructureVMsIn(BaseSchema):

    vm_name: list[str]
    fisc_wk: str


class InfrastructureVMsOut(BaseSchema):

    total_count: int
    data: list[InfrastructureVMsAll]
