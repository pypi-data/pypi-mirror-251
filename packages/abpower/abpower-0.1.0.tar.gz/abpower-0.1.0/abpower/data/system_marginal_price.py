import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from .base import Data
from abpower.exceptions import ParseError


logger = logging.getLogger(__name__)


@dataclass
class ProjectedPrice(Data):
    """
    Class to represent a price in the System Marginal Price data.
    """

    hour_end: datetime
    as_of: datetime
    price: float


@dataclass
class CurrentProjectedPrice(ProjectedPrice):
    """
    Class to represent the current projected pool price.
    """

    pass


@dataclass
class HistoricalProjectedPrice(ProjectedPrice):
    """
    Class to represent a historical projected pool price.
    """

    volume: int


@dataclass
class SystemMarginalPrice(Data):
    """
    Class to represent values from the System Marginal Price page.
    """

    timestamp: datetime

    current: CurrentProjectedPrice
    historical: list[HistoricalProjectedPrice]
