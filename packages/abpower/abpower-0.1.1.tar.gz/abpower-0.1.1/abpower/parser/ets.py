import logging
from abpower.data import (
    CurrentSupplyDemand,
    ActualForecast,
    DailyAveragePoolPrice,
    HourlyAvailableCapability,
    PoolPrice,
    SupplySurplus,
    SystemMarginalPrice,
    ETS,
)
from . import (
    CurrentSupplyDemandParser,
    ActualForecastParser,
    DailyAveragePoolPriceParser,
    HourlyAvailableCapabilityParser,
    PoolPriceParser,
    SupplySurplusParser,
    SystemMarginalPriceParser,
)
from datetime import datetime, timezone


logger = logging.getLogger(__name__)


class ETSParser:
    """
    Parser class for all available parts of the ETS site.

    This isn't a parser like the others - this one collects all the others
    into one object.
    """

    def get_current_supply_demand(self) -> CurrentSupplyDemand:
        """Get the Current Supply Demand values."""
        parser = CurrentSupplyDemandParser()

        return parser.get()

    def get_actual_forecast(self) -> ActualForecast:
        """Get the Actual / Forecast values."""
        parser = ActualForecastParser()

        return parser.get()

    def get_daily_average_pool_price(self) -> DailyAveragePoolPrice:
        """Get the Daily Average Pool Price values."""
        parser = DailyAveragePoolPriceParser()

        return parser.get()

    def get_hourly_available_capability(self) -> HourlyAvailableCapability:
        """Get the 7 Day Hourly Availavble Capability values."""
        parser = HourlyAvailableCapabilityParser()

        return parser.get()

    def get_pool_price(self) -> PoolPrice:
        """Get the Pool Price values."""
        parser = PoolPriceParser()

        return parser.get()

    def get_supply_surplus(self) -> SupplySurplus:
        """Get the Supply Surplus values."""
        parser = SupplySurplusParser()

        return parser.get()

    def get_system_marginal_price(self) -> SystemMarginalPrice:
        """Get the System Marginal Price values."""
        parser = SystemMarginalPriceParser()

        return parser.get()

    def get(self, query: tuple | list = None) -> ETS:
        """Return all available parts of the ETS site."""
        logger.debug(f"Parsing ETS...")

        now = datetime.now(tz=timezone.utc)

        queries = {
            "current-supply-demand": self.get_current_supply_demand,
            "actual-forecast": self.get_actual_forecast,
            "daily-average-pool-price": self.get_daily_average_pool_price,
            "hourly-available-capability": self.get_hourly_available_capability,
            "pool-price": self.get_pool_price,
            "supply-surplus": self.get_supply_surplus,
            "system-marginal-price": self.get_system_marginal_price
        }

        values = {}

        # Query requested data.
        for name, func in queries.items():
            if not query or name in query or "all" in query:
                logger.debug(
                    f"Querying '{name}'..."
                )
                values[name.replace("-", "_")] = func()
            else:
                logger.debug(
                    f"Skipping '{name}'..."
                )
                values[name.replace("-", "_")] = None

        # Build the main object...
        o = ETS(
            timestamp=now,
            **values
        )

        logger.debug(f"Parsed ETS at '{o.timestamp}'.")

        # ...and return it.
        return o
