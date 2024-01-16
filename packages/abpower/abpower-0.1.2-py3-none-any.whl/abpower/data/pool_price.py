import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from .base import Data
from abpower.exceptions import ParseError


logger = logging.getLogger(__name__)


@dataclass
class HourEndPoolPrice(Data):
    """
    Class to represent a price in the pool price data.
    """

    hour_end: datetime
    price: float | None
    rolling_average: float | None
    ail_demand: int | None


@dataclass
class PoolPrice(Data):
    """
    Class to represent values from the Pool Price page.
    """

    timestamp: datetime

    hour_ends: list[HourEndPoolPrice]
