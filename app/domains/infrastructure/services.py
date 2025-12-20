"""Service module."""

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.domains.infrastructure import models, schemas
from app.utils import formatter

# ============================================
# Naming convention of functions > Same as endpoint's function name (e.g. get_all)


async def get_all(
    db_session: AsyncSession,
) -> list[models.InfrastructureVMs]:
    """
    Returns all VMs.

    Returns:
        list: List of ORM models. Each element representing one row in table.
    """
    try:
        result = await db_session.execute(select(models.InfrastructureVMs))
        result_scalars = result.scalars().all()
        return result_scalars
    except Exception as e:
        msg = "Error fetching data from database"
        logger.error(formatter.format_error(e, msg))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=msg,
        )


async def post_vms(
    db_session: AsyncSession,
    request: schemas.InfrastructureVMsIn,  # Pydantic validates the incoming payload before the function run
) -> list[schemas.InfrastructureVMsOut]:
    """
    Returns VMs specified in body of request for particular fisc_wk.

    Returns:
        list: returns pydantic validated and serialized response XXXXXXXXXList of ORM models. Each element representing one row in table.
    """
    try:
        stmt = (
            select(models.InfrastructureVMs)
            .where(models.InfrastructureVMs.vm_name.in_(request.vm_name))
            .where(models.InfrastructureVMs.fisc_wk == request.fisc_wk)
        )
        result = await db_session.execute(stmt)
        result_scalars = result.scalars().all()
        # assert print(isinstance(request, schemas.InfrastructureVMsIn))
        # print(result_scalars)

        result_pydantic = schemas.InfrastructureVMsOut(
            total_count=len(result_scalars),
            data=[schemas.InfrastructureVMsAll.model_validate(vm) for vm in result_scalars],
        )

        # apps_pydantic = [PydIccrMonthlyCost.model_validate(app).model_dump() for app in apps]

        print(result_pydantic)
        # total_count=1 data=[InfrastructureVMsAll(vm_name='vm_1', fisc_wk='2026-W01', fisc_yr='FY26', cost=1000.0, role='SQL')]

        return result_pydantic
        # dictt = {}
        # dictt["data"] = result_scalars
        # return dictt

    except Exception as e:
        msg = "Error fetching data from database"
        logger.error(formatter.format_error(e, msg))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=msg,
        )


# msg = str(e).replace("\n", "\n    ")
# logger.error(f"Error fetching data from database:\n    {msg}")

# Add try catch error here in the services, like:

# async def fetch_all_documents(self, collection_name: str) -> list[dict[str, Any]]:
#     """
#     Fetch all documents from a collection

#     Args:
#         collection_name (str): Name of the collection to fetch documents from

#     Returns:
#         documents: List of documents in the collection
#     """
#     try:
#         collection_ref = self.firestore_client.collection(collection_name)
#         docs = collection_ref.stream()
#         return [doc_dict async for doc in docs if (doc_dict := doc.to_dict()) is not None]
#     except Exception as ex:
#         logger.error("Error fetching documents from collection")
#         logger.debug(str(ex))
#         raise ex


#   def get_current_fisc_month(self) -> str:
#         """Returns most current fiscal month from DB

#         Returns:
#             str: current fiscal month in format <2026-M01>
#         """
#         with self.db as session:
#             latest_app: Optional[IccrMonthlyCosts] = (
#                 session.query(IccrMonthlyCosts)
#                 .order_by(IccrMonthlyCosts.fisc_yr.desc(), IccrMonthlyCosts.fisc_mth.desc())
#                 .first()
#             )
#         if not latest_app:
#             empty_db_error = HTTPException(
#                 status.HTTP_503_SERVICE_UNAVAILABLE,
#                 "There are no items in database, if the problem persist please contact idea team",
#             )
#             logger.error(empty_db_error.detail)
#             raise empty_db_error
#         latest_app_pydantic = IccrTable.model_validate(latest_app)
#         return latest_app_pydantic.fisc_mth


# result = await db_session.execute(select(models.InfrastructureVMs))
# vms = result.scalars().all()
# return vms

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# class OrderingCRUD:
#     """CLass responsible for user CRUD operations."""

#     def __init__(self, db: Session) -> None:
#         """This method depends on the ORM SQLalchemy session and will not work with different connection.

#         Args:
#             db (Session): Database session object that will be used, preferably from generator function.
#         """
#         self.db = db

#     def get_all_orders(self, skip: int, limit: int) -> list[SrfOrderDetails]:
#         """Get all orders

#         Args:
#             skip (int): offset, number of rows to skip
#             limit (int): limit returned rows

#         Returns:
#             Optional[list[SrfOrderDetails]]: returns orders or if there are none returns None
#         """
#         with self.db as session:
#             apps: list[SrfOrderDetails] = session.query(SrfOrderDetails).order_by(SrfOrderDetails.order_number).offset(skip).limit(limit).all()
#         return apps

#     def get_by_srf(self, skip: int, limit: int, srf_number: str) -> list[SrfOrderDetails]:
#         with self.db as session:
#             apps: list[SrfOrderDetails] = (
#                 session.query(SrfOrderDetails)
#                 .order_by(SrfOrderDetails.order_number)
#                 .where(SrfOrderDetails.srf_number == srf_number)
#                 .offset(skip)
#                 .limit(limit)
#                 .all()
#             )
#         return apps

#     def get_by_order_number(self, skip: int, limit: int, order_number: str) -> list[SrfOrderDetails]:
#         with self.db as session:
#             apps: list[SrfOrderDetails] = (
#                 session.query(SrfOrderDetails)
#                 .order_by(SrfOrderDetails.order_number)
#                 .where(SrfOrderDetails.order_number == order_number)
#                 .offset(skip)
#                 .limit(limit)
#                 .all()
#             )
#         return apps

#     def get_by_status(self, skip: int, limit: int, status: str) -> list[SrfOrderDetails]:
#         with self.db as session:
#             apps: list[SrfOrderDetails] = (
#                 session.query(SrfOrderDetails)
#                 .order_by(SrfOrderDetails.order_number)
#                 .where(SrfOrderDetails.order_status == status)
#                 .offset(skip)
#                 .limit(limit)
#                 .all()
#             )
#         return apps

#     def get_track_url_by_order_number(self, order_number: str) -> Optional[str]:
#         with self.db as session:
#             app_url = session.scalar(select(SrfOrderDetails.tracking_link).where(SrfOrderDetails.order_number == order_number))
#         logger.info("%s", app_url)

#         if not app_url:
#             return None

#         return app_url


# async def get_ordering_crud(db: Session = Depends(get_012_ordering_orm)) -> OrderingCRUD:
#     """Factory method for OrderingCRUD

#     Args:
#         db (Session, optional): Dependency injection of needed DB. Defaults to Depends(get_test_db).

#     Returns:
#         OrderingCRUD: High level CRUD object interface for User database operations.
#     """
#     return OrderingCRUD(db)
