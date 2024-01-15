import logging
import pytz
from .base import BaseParser
from bs4 import BeautifulSoup
from abpower.data.pool_price import PoolPrice, HourEndPoolPrice
from datetime import datetime, timezone, timedelta


logger = logging.getLogger(__name__)


class PoolPriceParser(BaseParser):
    """
    Parser class for the System Marginal Price page.
    """

    path = "Market/Reports/SMPriceReportServlet"

    def create_hour_end_timestamp(self, hour_end: str) -> datetime:
        """Create a datetime object for the 'hour end' value."""

        # Get the actual current time.
        now = datetime.now(pytz.timezone("America/Edmonton"))

        # Parse out the month/day/year (?!?).
        date, hour = hour_end.split(" ")
        month, day, year = date.split("/")

        # Even better, here 24 is used instead of 00. When this happens,
        # just use 23 instead and we'll advance it by an hour afterwards.
        if hour == "24":
            hour = "23"
            advance_hour = True
        else:
            advance_hour = False

        dt = datetime(
            year=int(year),
            month=int(month),
            day=int(day),
            hour=int(hour),
            minute=0,
            tzinfo=now.tzinfo,
        )

        if advance_hour:
            dt = dt + timedelta(hours=1)

        return dt

    def parse_hour_end_pool_prices(self, b: BeautifulSoup) -> list[HourEndPoolPrice]:
        """Extract the historical projected pool prices."""
        logger.debug(f"Parsing hour end pool prices...")

        # Find the string "Date (HE)", then get the enclosing table.
        table = b.find(string="Date (HE)").find_parent("table")
        hour_end_prices = []

        # Iterate over the rows, skipping the first one.
        for tr in table.find_all("tr")[1:]:
            hour_end, price, rolling_average, ail_demand = list(tr.strings)

            # The price, rolling average and demand can all be a '-' if no
            # values are available. If this is the case, set them to 'None'.
            # Otherwise, cast them to the correct values.
            if price == "-":
                price = None
            else:
                price = float(price)

            if rolling_average == "-":
                rolling_average = None
            else:
                rolling_average = float(rolling_average)

            if ail_demand == "-":
                ail_demand = None
            else:
                # The website lists these with one decimal place, which
                # always seems to be a 0, so just assume it's an integer
                # like everywhere else.
                ail_demand = int(ail_demand.split(".")[0])

            # Convert the hour end into an actual timestamp.
            hour_end = self.create_hour_end_timestamp(hour_end)

            hour_end_prices.append(
                HourEndPoolPrice(
                    b=b,
                    hour_end=hour_end,
                    price=price,
                    rolling_average=rolling_average,
                    ail_demand=ail_demand,
                )
            )

        return hour_end_prices

    def parse(self, b: BeautifulSoup) -> PoolPrice:
        """Parse the Pool Price page."""
        logger.debug(f"Parsing pool price...")

        now = datetime.now(tz=timezone.utc)

        # Build the main object...
        o = PoolPrice(b=b, timestamp=now, hour_ends=self.parse_hour_end_pool_prices(b))

        logger.debug(f"Parsed pool price.")

        # ...and return it.
        return o
