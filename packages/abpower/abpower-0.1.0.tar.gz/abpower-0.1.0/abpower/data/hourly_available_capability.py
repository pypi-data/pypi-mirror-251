import logging
from dataclasses import dataclass
from datetime import datetime
from .base import Data


logger = logging.getLogger(__name__)


@dataclass
class HourEndHourlyAvailableCapability(Data):
    """
    Class to represent an entry in the Daily Average Pool Price data.
    """

    hour_end: datetime
    percentage: float


@dataclass
class GenerationHourlyAvailableCapability(Data):
    """
    Class to represent the available capability for a given generation type.
    """

    generation_type: str
    hour_ends: list[HourEndHourlyAvailableCapability]
    mc: int


@dataclass
class HourlyAvailableCapability(Data):
    """
    Class to represent values from the 7 Days Hourly Available Capability page.
    """

    timestamp: datetime

    last_updated: datetime

    generation_types: list[GenerationHourlyAvailableCapability]
