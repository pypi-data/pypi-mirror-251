"""This module contains functions for querying the database for analysis objects."""
from .. import session, select
from doplaydo.dodata_core.models import (
    Die,
    Wafer,
    Project,
    Analysis,
    DeviceData,
    Device,
    Cell,
)
from collections.abc import Sequence
from sqlalchemy.sql import ColumnElement
from sqlmodel.sql.expression import SelectOfScalar


def _get_analyses_joined_query() -> SelectOfScalar[Analysis]:
    return select(Analysis).join(DeviceData).join(Device).join(Die).join(Wafer)


def get_analyses_by_query(
    *clauses: ColumnElement[bool],
) -> Sequence[Analysis]:
    """Query the database for device data and return DeviceData and its raw data.

    Args:
        clauses: sql expressions such as `dd.Cell.name == "RibLoss"`.
    """
    statement = _get_analyses_joined_query()

    for clause in clauses:
        statement = statement.where(clause)

    _analyses = session.exec(statement).all()

    return _analyses


def get_analyses_for_device_data(
    project_name: str,
    device_name: str,
    wafer_name: str | None = None,
    die_x: int | None = None,
    die_y: int | None = None,
) -> Sequence[Analysis]:
    """Get all analyses for device_data.

    Args:
        project_name: The name of the project.
        device_name: The name of the device.
        wafer_name: The name of the wafer.
        die_x: The x coordinate of the die.
        die_y: The y coordinate of the die.
    """
    query = (
        select(DeviceData)
        .join(Device)
        .join(Cell, Device.cell_id == Cell.id)
        .join(Project)
        .where(Project.name == project_name)
        .where(Device.name == device_name)
    )

    if die_x is not None or die_y is not None:
        query = query.join(Die, DeviceData.die_id == Die.id)

        if die_x is not None:
            query = query.where(Die.x == die_x)

        if die_y is not None:
            query = query.where(Die.y == die_y)

    if wafer_name:
        query = query.join(Wafer).where(Wafer.name == wafer_name)

    device_data = session.exec(query).all()
    if not device_data:
        raise LookupError("Could not find device_data in the database.")

    return session.exec(
        select(Analysis).where(Analysis.device_data_id.in_([d.id for d in device_data]))
    ).all()


def get_analyses_for_die(
    project_name: str,
    wafer_name: str,
    die_x: int,
    die_y: int,
) -> Sequence[Analysis]:
    """Get all analyses for a die.

    Args:
        project_name: The name of the project.
        wafer_name: The name of the wafer.
        die_x: The x coordinate of the die.
        die_y: The y coordinate of the die.
    """
    die = session.exec(
        select(Die)
        .join(Wafer)
        .join(Project)
        .where(Wafer.name == wafer_name)
        .where(Project.name == project_name)
        .where(Die.x == die_x)
        .where(Die.y == die_y)
    ).one_or_none()
    if not die:
        raise LookupError("Could not find die in the database.")
    return session.exec(
        select(Analysis).join(Die, Analysis.die_id == Die.id).where(Die.id == die.id)
    ).all()


def get_analyses_for_wafer(
    project_name: str,
    wafer_name: str,
) -> Sequence[Analysis]:
    """Get all analyses for a wafer.

    Args:
        project_name: The name of the project.
        wafer_name: The name of the wafer.
    """
    wafer = session.exec(
        select(Wafer)
        .join(Project)
        .where(Wafer.name == wafer_name)
        .where(Project.name == project_name)
    ).one_or_none()
    if not wafer:
        raise LookupError("Could not find wafer in the database.")

    return session.exec(
        select(Analysis)
        .join(Wafer, Analysis.wafer_id == Wafer.id)
        .where(Wafer.id == wafer.id)
    ).all()
