"""Endpoints related to Ordering-Sims data."""

import logging
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.openapi.models import Example
from fastapi.security import OAuth2PasswordBearer

from idea_api.core.security import AccessManager, get_access_manager
from idea_api.crud.ordering_crud import OrderingCRUD, get_ordering_crud
from idea_api.schemes.ordering import OrderDetails
from idea_api.schemes.roles import RoleNames

logger = logging.getLogger(__name__)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

not_enough_privileges_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You don't have enough privileges to access this data.",
)

order_status_examples: dict[str, Example] = {
    "Cancelled": {"value": "Cancelled"},
    "In Production": {"value": "In Production"},
    "Invoiced": {"value": "Invoiced"},
    "Manifested": {"value": "Manifested"},
    "Manufacturing Invoiced": {"value": "Manufacturing Invoiced"},
    "Pending Production": {"value": "Pending Production"},
    "Production Complete": {"value": "Production Complete"},
    "Rejected": {"value": "Rejected"},
    "Ship Complete": {"value": "Ship Complete"},
    "Waiting Order Fulfillment": {"value": "Waiting Order Fulfillment"},
}


@router.get("/", response_model=list[OrderDetails])
def get_all_orders(
    token: str = Depends(oauth2_scheme),
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, gt=0),
    db: OrderingCRUD = Depends(get_ordering_crud),
    access_manager: AccessManager = Depends(get_access_manager),
):
    """Will fetch all orders

    Args:
        skip (int, optional): skip n records. Defaults to Query(0, ge=0).
        limit (int, optional): limit to n records. Defaults to Query(1000, gt=0).

    Raises:
        HTTPException: not enough privileges

    Returns:
        list[OrderDetails]: returns list, or empty lists if you are at the end
    """

    if not access_manager.check_user_privileges(token, RoleNames.ORDERING):
        raise not_enough_privileges_exception

    apps = db.get_all_orders(skip, limit)
    return apps


@router.get("/srf/{srf_number}", response_model=list[OrderDetails])
def get_order_by_srf(
    srf_number: Annotated[str, "Srf number to filter by"],
    token: str = Depends(oauth2_scheme),
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, gt=0),
    db: OrderingCRUD = Depends(get_ordering_crud),
    access_manager: AccessManager = Depends(get_access_manager),
):
    """Will fetch all the records for given srf number

    Args:
        srf_number (str): Srf number to filter by
        skip (int, optional): skip n records. Defaults to Query(0, ge=0).
        limit (int, optional): limit to n records. Defaults to Query(1000, gt=0).

    Raises:
        HTTPException: not enough privileges

    Returns:
        list[OrderDetails]: returns list, or empty lists if you are at the end
    """
    if not access_manager.check_user_privileges(token, required_action_type=RoleNames.ORDERING):
        raise not_enough_privileges_exception

    apps = db.get_by_srf(skip, limit, srf_number)
    return apps


@router.get("/order/{order_number}", response_model=list[OrderDetails])
def get_order_by_order_number(
    order_number: str,
    token: str = Depends(oauth2_scheme),
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, gt=0),
    db: OrderingCRUD = Depends(get_ordering_crud),
    access_manager: AccessManager = Depends(get_access_manager),
):
    """Returns all the orders for given order number

    Args:
        order_number (str): order number
        skip (int, optional): skip n records. Defaults to Query(0, ge=0).
        limit (int, optional): limit to n records. Defaults to Query(1000, gt=0).

    Raises:
        HTTPException: not enough privileges

    Returns:
        list[OrderDetails]: returns list, or empty lists if you are at the end
    """
    if not access_manager.check_user_privileges(token, required_action_type=RoleNames.ORDERING):
        raise not_enough_privileges_exception

    apps = db.get_by_order_number(skip, limit, order_number)
    return apps


@router.get("/status/{order_status}", response_model=list[OrderDetails])
def get_order_by_order_status(
    order_status: Annotated[str, Path(openapi_examples=order_status_examples)],
    token: str = Depends(oauth2_scheme),
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, gt=0),
    db: OrderingCRUD = Depends(get_ordering_crud),
    access_manager: AccessManager = Depends(get_access_manager),
):
    """Fetches filtered data by order status

    Args:
        order_status (str): Status of the order. Defaults to order_status_examples)].
        skip (int, optional): skip n records. Defaults to Query(0, ge=0).
        limit (int, optional): limit to n records. Defaults to Query(1000, gt=0).

    Raises:
        HTTPException: not enough privileges

    Returns:
        list[OrderDetails]: returns list, or empty lists if you are at the end
    """
    if not access_manager.check_user_privileges(token, required_action_type=RoleNames.ORDERING):
        raise not_enough_privileges_exception

    apps = db.get_by_status(skip, limit, order_status)
    return apps


@router.get("/track/{order_number}")
def get_order_tracking_link(
    order_number: str,
    token: str = Depends(oauth2_scheme),
    db: OrderingCRUD = Depends(get_ordering_crud),
    access_manager: AccessManager = Depends(get_access_manager),
) -> Optional[str]:
    """Will return tracking url for given order number

    Args:
        order_number (str): order number

    Raises:
        HTTPException: not enough privileges

    Returns:
        Optional[str]: Returns empty null or url to the order tracking
    """
    if not access_manager.check_user_privileges(token, required_action_type=RoleNames.ORDERING):
        raise not_enough_privileges_exception
    tracking_link = db.get_track_url_by_order_number(order_number)
    return tracking_link
