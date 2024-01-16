import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from .base import Data
from abpower.exceptions import ParseError


logger = logging.getLogger(__name__)


@dataclass
class BaseGeneration(Data):
    """
    Base class for objects that have generation values.
    See http://ets.aeso.ca/Market/Reports/Manual/HelpText/current-CSD-metadata.pdf.

    * mc - Maximum capability in MW
    * tng - Total net generation in MW
    * dcr - Dispatched (and accepted) contingency reserve
    """

    mc: int
    tng: int
    dcr: int


@dataclass
class Summary(Data):
    """
    Class to represent the "SUMMARY" table.
    """

    alberta_total_net_generation: int
    net_actual_interchange: int
    alberta_internal_load: int
    net_to_grid_generation: int
    contingency_reserve_required: int
    dispatched_contingency_reserve: int
    dispatched_contingency_reserve_gen: int
    dispatched_contingency_reserve_other: int
    lssi_armed_dispatch: int
    lssi_offered_volume: int


@dataclass
class Generation(BaseGeneration):
    """
    Class to represent the per-type generation totals in the "GENERATION" table.
    """

    name: str


@dataclass
class Interchange(Data):
    """
    Class to represent the interchanges in the "INTERCHANGES" tables.
    """

    name: str
    actual_flow: int


@dataclass
class Asset(BaseGeneration):
    """
    Class to represent the generation assets.
    """

    generation_type: str

    # We get passed a name, but we'll adjust it in post-init processing.
    name: str

    # We extract the asset code from the name in post-init processing.
    asset_code: str = field(init=False)

    def __post_init__(self):
        # Extract the asset code.

        try:
            self.asset_code, self.name, extras = re.search(
                r"(.*)\s\(([A-Z0-9]+)\)([\*\^])?", self.name
            ).groups()

        except AttributeError as e:
            raise ParseError(f"Failed to parse name '{self.name}': {e}", o=e)

        logger.debug(f"Name: {self.name} Code: {self.asset_code} Extras: {extras}")


@dataclass
class CurrentSupplyDemand(Data):
    """
    Class to represent the overall page values.
    """

    timestamp: datetime

    last_update: datetime

    summary: Summary
    generation: list[Generation]
    interchange: list[Interchange]
    assets: list[Asset]
