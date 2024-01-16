import logging
import pytz
from .base import BaseParser
from bs4 import BeautifulSoup
from abpower.data.daily_average_pool_price import (
    DailyAveragePoolPrice,
    DayAveragePoolPrice,
)
from datetime import datetime, timezone


logger = logging.getLogger(__name__)


class DailyAveragePoolPriceParser(BaseParser):
    """
    Parser class for the System Marginal Price page.
    """

    path = "Market/Reports/DailyAveragePoolPriceReportServlet"

    def create_timestamp(self, date: str) -> datetime:
        """Create a datetime object for the timestamp value."""

        # Get the actual current time.
        now = datetime.now(pytz.timezone("America/Edmonton"))

        # Parse out the month/day/year (sigh).
        month, day, year = date.split("/")

        dt = datetime(
            year=int(year),
            month=int(month),
            day=int(day),
            hour=0,
            minute=0,
            tzinfo=now.tzinfo,
        )

        return dt

    def parse_daily_average_pool_prices(
        self, b: BeautifulSoup
    ) -> list[DayAveragePoolPrice]:
        """Extract the daily average pool prices."""
        logger.debug(f"Parsing daily average pool prices...")

        # Find the string "Date (HE)", then get the enclosing table.
        table = b.find(string="Date").find_parent("table")
        days = []

        # Iterate over the rows, skipping the first two.
        for tr in table.find_all("tr")[2:]:
            (
                date,
                daily_average,
                daily_on_peak_average,
                daily_off_peak_average,
                rolling_average,
                rolling_on_peak_average,
                rolling_off_peak_average,
            ) = list(tr.strings)

            # Cast the values to the correct types.
            # These are historical, so they shouldn't be missing.
            daily_average = float(daily_average)
            daily_on_peak_average = float(daily_on_peak_average)
            daily_off_peak_average = float(daily_off_peak_average)
            rolling_average = float(rolling_average)
            rolling_on_peak_average = float(rolling_on_peak_average)
            rolling_off_peak_average = float(rolling_off_peak_average)

            # Convert the date into an actual timestamp.
            date = self.create_timestamp(date)

            days.append(
                DayAveragePoolPrice(
                    b=tr,
                    date=date,
                    daily_average=daily_average,
                    daily_on_peak_average=daily_on_peak_average,
                    daily_off_peak_average=daily_off_peak_average,
                    rolling_average=rolling_average,
                    rolling_on_peak_average=rolling_on_peak_average,
                    rolling_off_peak_average=rolling_off_peak_average,
                )
            )

        return days

    def parse(self, b: BeautifulSoup) -> DailyAveragePoolPrice:
        """Parse the Daily Average Pool Price page."""
        logger.debug(f"Parsing daily average pool price...")

        now = datetime.now(tz=timezone.utc)

        # Build the main object...
        o = DailyAveragePoolPrice(
            b=b, timestamp=now, days=self.parse_daily_average_pool_prices(b)
        )

        logger.debug(f"Parsed pool price.")

        # ...and return it.
        return o
