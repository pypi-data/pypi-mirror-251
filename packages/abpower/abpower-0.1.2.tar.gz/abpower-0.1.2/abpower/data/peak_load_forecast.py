import logging
from dataclasses import dataclass
from datetime import datetime
from .base import Data


logger = logging.getLogger(__name__)


@dataclass
class HourEndPeakLoadForecast(Data):
    """
    Class to represent an entry in the Daily Average Pool Price data.
    """

    hour_end: datetime
    percentage: int


@dataclass
class DayPeakLoadForecast(Data):
    """
    Class to represent the available capability for a given generation type.
    """

    day: datetime
    hour_ends: list[HourEndPeakLoadForecast]


@dataclass
class PeakLoadForecast(Data):
    """
    Class to represent values from the 7 Days Hourly Available Capability page.
    """

    timestamp: datetime

    peak_demand: int
    set_on: datetime

    days: list[DayPeakLoadForecast]
