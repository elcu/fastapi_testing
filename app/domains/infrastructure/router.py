from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.domains.infrastructure import models, schemas, services

router = APIRouter(prefix="/infrastructure", tags=["Infrastructure"])

# ============================================
# Naming convention of functions > method + endpoint separated by underscores (e.g. get_vms_all). ORM / Pydantic suffixes should be dropped, as these are used only to detail the differences between the endpoints

# ============================================
# Two possibilities on how to approach the endpoints
#     ^ vms-all-orm calls service which returns an ORM object, and endpoint validates and serializes it with pydantic by using response_model = schema to validate on
#     ^ vms-all-pydantic / vms-filter-pydantic endpoints use ORM only for db calls. Service directly validates returned db data based on Pydantic's model


# ====== Most simple endpoint - service returns ORM object that is being validated using FastAPI's response_model paramater, which uses Pydantic model defined by us
@router.get(
    "/vms-all-orm",
    response_model=list[
        schemas.InfrastructureVMsBase
    ],  # Validate returned ORM model by using Pydantic model that we have defined, serialize ORM object, create documentation etc.
    summary="Returns a list of all VMs in the environment using the ORM object",
)
async def get_vms_all_orm(
    db_session: Annotated[AsyncSession, Depends(get_session)],
) -> list[models.InfrastructureVMs]:

    return await services.get_vms_all_orm(db_session)


# ====== Validation of endpoint is done directly in service using the Pydantic model that we have defined. ORM is being used only for a db call
@router.get(
    "/vms-all-pydantic",
    response_model=schemas.InfrastructureVMsBasePydantic,  # Service already validates the model, however FastAPI's response_model parameter also generates documentation, serializes to json etc. FastAPI also doesn't know what is returned from service, it enforces the contract at the endpoint layer. It protects API boundary
    summary="Returns a list of all VMs in the environment for specified fiscal week using the Pydantic object, along with metadata",
)
async def get_vms_all_pydantic(
    db_session: Annotated[AsyncSession, Depends(get_session)],
    fisc_wk: Annotated[str, Query(example="2030-W01")],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=10000)] = 100,
) -> schemas.InfrastructureVMsBasePydantic:

    return await services.get_vms_all_pydantic(db_session, fisc_wk, skip, limit)


# ====== Validation of endpoint is done directly in service using the Pydantic model that we have defined. ORM is being used only for a db call
@router.post(
    "/vms-filter-pydantic",
    response_model=schemas.InfrastructureVMsOut,  # Service already validates the model, however FastAPI's response_model parameter also generates documentation, serializes to json etc. FastAPI also doesn't know what is returned from service, it enforces the contract at the endpoint layer. It protects API boundary
    summary="Returns a single or a list of VMs along with metadata",
)
async def post_vms_filter_pydantic(
    db_session: Annotated[AsyncSession, Depends(get_session)],
    request: schemas.InfrastructureVMsIn,
) -> schemas.InfrastructureVMsOut:

    return await services.post_vms_filter_pydantic(db_session, request)
