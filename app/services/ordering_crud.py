"""Crud module acting as a core for ordering-sims."""

import logging
from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from idea_api.db.connections import get_012_ordering_orm
from idea_api.models.sql_ordering import SrfOrderDetails

logger = logging.getLogger(__name__)


class OrderingCRUD:
    """CLass responsible for user CRUD operations."""

    def __init__(self, db: Session) -> None:
        """This method depends on the ORM SQLalchemy session and will not work with different connection.

        Args:
            db (Session): Database session object that will be used, preferably from generator function.
        """
        self.db = db

    def get_all_orders(self, skip: int, limit: int) -> list[SrfOrderDetails]:
        """Get all orders

        Args:
            skip (int): offset, number of rows to skip
            limit (int): limit returned rows

        Returns:
            Optional[list[SrfOrderDetails]]: returns orders or if there are none returns None
        """
        with self.db as session:
            apps: list[SrfOrderDetails] = (
                session.query(SrfOrderDetails)
                .order_by(SrfOrderDetails.order_number)
                .offset(skip)
                .limit(limit)
                .all()
            )
        return apps

    def get_by_srf(self, skip: int, limit: int, srf_number: str) -> list[SrfOrderDetails]:
        with self.db as session:
            apps: list[SrfOrderDetails] = (
                session.query(SrfOrderDetails)
                .order_by(SrfOrderDetails.order_number)
                .where(SrfOrderDetails.srf_number == srf_number)
                .offset(skip)
                .limit(limit)
                .all()
            )
        return apps

    def get_by_order_number(
        self, skip: int, limit: int, order_number: str
    ) -> list[SrfOrderDetails]:
        with self.db as session:
            apps: list[SrfOrderDetails] = (
                session.query(SrfOrderDetails)
                .order_by(SrfOrderDetails.order_number)
                .where(SrfOrderDetails.order_number == order_number)
                .offset(skip)
                .limit(limit)
                .all()
            )
        return apps

    def get_by_status(self, skip: int, limit: int, status: str) -> list[SrfOrderDetails]:
        with self.db as session:
            apps: list[SrfOrderDetails] = (
                session.query(SrfOrderDetails)
                .order_by(SrfOrderDetails.order_number)
                .where(SrfOrderDetails.order_status == status)
                .offset(skip)
                .limit(limit)
                .all()
            )
        return apps

    def get_track_url_by_order_number(self, order_number: str) -> Optional[str]:
        with self.db as session:
            app_url = session.scalar(
                select(SrfOrderDetails.tracking_link).where(
                    SrfOrderDetails.order_number == order_number
                )
            )
        logger.info("%s", app_url)

        if not app_url:
            return None

        return app_url


async def get_ordering_crud(db: Session = Depends(get_012_ordering_orm)) -> OrderingCRUD:
    """Factory method for OrderingCRUD

    Args:
        db (Session, optional): Dependency injection of needed DB. Defaults to Depends(get_test_db).

    Returns:
        OrderingCRUD: High level CRUD object interface for User database operations.
    """
    return OrderingCRUD(db)
