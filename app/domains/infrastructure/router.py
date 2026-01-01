from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.domains.infrastructure import models, schemas, services

router = APIRouter(prefix="/infrastructure", tags=["Infrastructure"])

# ============================================
# Naming convention of functions > method + endpoint (e.g. post_vm)

# ============================================
# Two possibilities on how to approach the endpoints
#     ^ get_all() calls service get_all() which returns an ORM object, and endpoint validates and serializes it with pydantic by using response_model = schema to validate on
#     ^ get_vms()


# TODO: Implement total count of VMs returned
@router.get(
    "/all",
    response_model=list[schemas.InfrastructureVMsAll],  # Validate returned ORM model by using Pydantic schema and serialize ORM object
    summary="Returns a list of all VMs in the environment",
)
async def get_all(
    db_session: Annotated[AsyncSession, Depends(get_session)],
) -> list[models.InfrastructureVMs]:

    return await services.get_all(db_session)


@router.post(
    "/vms",
    response_model=schemas.InfrastructureVMsOut,  # Service already validates the model, however response_model also generates documentation, serializes do json etc. FastAPI also doesn't know what is returned from service, it enforces the contract at the endpoint layer. It protects API boundary
    summary="Returns a single or a list of VMs",
)
async def post_vms(
    # vm: Annotated[list[str], Query(title="dwqdwqdq", description="USE THIS FOR DESCRIPTION IN DOCS ")],§
    request: schemas.InfrastructureVMsIn,  # Annotated[list[str], Query(min_length=1)],
    # app_id: Annotated[list[int], Query(min_length=1)],
    # fisc_wk: Annotated[str, Query(openapi_examples={"fiscal month": {"value": "2026-M01"}})],
    db_session: Annotated[AsyncSession, Depends(get_session)],
) -> schemas.InfrastructureVMsOut:

    return await services.post_vms(db_session, request)
