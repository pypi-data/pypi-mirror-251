import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from .base import Data
from abpower.exceptions import ParseError


logger = logging.getLogger(__name__)


@dataclass
class HourEndActualForecast(Data):
    """
    Class to represent an entry in the Actual / Forecast data.
    """

    hour_end: datetime
    forecast_pool_price: float | None
    actual_posted_pool_price: float | None
    forecast_ail: int | None
    actual_ail: int | None
    difference: int | None


@dataclass
class ActualForecast(Data):
    """
    Class to represent values from the Actual / Forecast page.
    """

    timestamp: datetime

    hour_ends: list[HourEndActualForecast]
