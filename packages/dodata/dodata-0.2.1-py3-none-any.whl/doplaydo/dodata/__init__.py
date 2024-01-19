"""Initiates the module."""
# isort:skip_file
# ruff: noqa: E402

from .config import get_settings
from doplaydo.dodata_core.models import (
    Project,
    Cell,
    Device,
    Die,
    Wafer,
    DeviceData,
    Analysis,
)
from sqlalchemy.orm import aliased
from sqlmodel import and_, or_, select

ParentCell = aliased(Cell)

settings = get_settings()
from .engine import get_session

session = get_session()
from .db.common import attribute_filter
from .db.device_data import get_data_by_query

from .api.device_data import get_data_by_id
from .api import analysis, cell, device, device_data, project

__version__ = "0.2.1"

# ruff: noqa: D101
__all__ = [
    "Analysis",
    "Cell",
    "Device",
    "DeviceData",
    "Die",
    "ParentCell",
    "Project",
    "Wafer",
    "analysis",
    "and_",
    "attribute_filter",
    "cell",
    "device",
    "device_data",
    "get_data_by_id",
    "get_data_by_query",
    "or_",
    "project",
    "select",
    "session",
    "settings",
]
