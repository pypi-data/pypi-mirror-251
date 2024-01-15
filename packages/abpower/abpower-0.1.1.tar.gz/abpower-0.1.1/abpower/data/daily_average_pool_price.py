import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from .base import Data
from abpower.exceptions import ParseError


logger = logging.getLogger(__name__)


@dataclass
class DayAveragePoolPrice(Data):
    """
    Class to represent an entry in the Daily Average Pool Price data.
    """

    date: datetime
    daily_average: float
    daily_on_peak_average: float
    daily_off_peak_average: float
    rolling_average: float
    rolling_on_peak_average: float
    rolling_off_peak_average: float


@dataclass
class DailyAveragePoolPrice(Data):
    """
    Class to represent values from the Daily Average Pool Price page.
    """

    timestamp: datetime

    days: list[DayAveragePoolPrice]
