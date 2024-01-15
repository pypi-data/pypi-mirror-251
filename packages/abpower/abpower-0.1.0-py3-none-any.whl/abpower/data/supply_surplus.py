import logging
from dataclasses import dataclass
from datetime import datetime
from .base import Data


logger = logging.getLogger(__name__)


@dataclass
class HourEndSupplySurplus(Data):
    """
    Class to represent an entry in the Daily Average Pool Price data.
    """

    hour_end: datetime
    status: int


@dataclass
class SupplySurplus(Data):
    """
    Class to represent values from the Supply Surplus page.
    """

    timestamp: datetime

    hour_ends: list[HourEndSupplySurplus]
