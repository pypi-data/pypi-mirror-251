import logging
from dataclasses import dataclass, field
from datetime import datetime
from .base import OutputMixin
from .current_supply_demand import CurrentSupplyDemand
from .actual_forecast import ActualForecast
from .daily_average_pool_price import DailyAveragePoolPrice
from .hourly_available_capability import HourlyAvailableCapability
from .pool_price import PoolPrice
from .supply_surplus import SupplySurplus
from .system_marginal_price import SystemMarginalPrice
from .peak_load_forecast import PeakLoadForecast


logger = logging.getLogger(__name__)


@dataclass
class ETS(OutputMixin):
    """
    Class to represent all current values from ETS.
    """

    timestamp: datetime

    current_supply_demand: CurrentSupplyDemand | None = field(repr=False)
    actual_forecast: ActualForecast | None = field(repr=False)
    daily_average_pool_price: DailyAveragePoolPrice | None = field(repr=False)
    hourly_available_capability: HourlyAvailableCapability | None = field(repr=False)
    pool_price: PoolPrice | None = field(repr=False)
    supply_surplus: SupplySurplus | None = field(repr=False)
    system_marginal_price: SystemMarginalPrice | None = field(repr=False)
    peak_load_forecast: PeakLoadForecast | None = field(repr=False)
