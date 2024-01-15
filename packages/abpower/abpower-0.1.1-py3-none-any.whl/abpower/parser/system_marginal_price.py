import logging
import re
import pytz
from .base import BaseParser
from bs4 import BeautifulSoup
from abpower.data.system_marginal_price import (
    SystemMarginalPrice,
    CurrentProjectedPrice,
    HistoricalProjectedPrice,
)
from datetime import datetime, timezone, timedelta


logger = logging.getLogger(__name__)


class SystemMarginalPriceParser(BaseParser):
    """
    Parser class for the System Marginal Price page.
    """

    path = "Market/Reports/CSMPriceReportServlet"

    def create_as_of_timestamp(self, as_of: str) -> datetime:
        """Create a datetime object for the 'as of' value."""

        # Get the actual current time.
        now = datetime.now(pytz.timezone("America/Edmonton"))

        # Create a datetime object for the passed time using
        # the above.
        dt = datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=now.hour,
            minute=now.minute,
            tzinfo=now.tzinfo,
        )

        # The time we get passed should be at most the same as the
        # actual current time. If it isn't, we need to subtract a day.
        # This should only happen if we query right at the end of a day, get
        # a time of 23:59, then the clock ticks over to the following day.
        if dt > now:
            dt = dt - timedelta(days=1)
            logger.warning(f"Adjusted 'current time' timestamp back 1 day.")

        return dt

    def create_hour_end_timestamp(self, as_of: datetime, hour_end: str) -> datetime:
        """Create a datetime object for the 'hour end' value."""

        # Get the actual current time.
        now = datetime.now(pytz.timezone("America/Edmonton"))

        # If the hour is 24, just use 23 instead and we'll advance it by an
        # hour afterwards.
        if hour_end == "24":
            hour_end = "23"
            advance_hour = True
        else:
            advance_hour = False

        # The 'hour end' value will always be in the future, so we can
        # start with the 'as of' timestamp.
        dt = datetime(
            year=as_of.year,
            month=as_of.month,
            day=as_of.day,
            hour=int(hour_end),
            minute=0,
            tzinfo=now.tzinfo,
        )

        if advance_hour:
            dt = dt + timedelta(hours=1)

        # If the new timestamp is in the past, it's because we ticked over to the
        # following day. To fix this, we add a day.
        if dt < as_of:
            dt = dt + timedelta(days=1)
            logger.warning(f"Adjusted 'hour end' timestamp forward 1 day.")

        return dt

    def parse_current_projected_price(self, b: BeautifulSoup) -> CurrentProjectedPrice:
        """Extract the current projected pool price."""
        logger.debug(f"Parsing current projected pool price...")

        # Find the string "Projected Pool Price for Hour"...
        string = b.find(string=re.compile(r"Projected Pool Price for Hour"))

        # ...and extract the values we want.
        hour_end, price, as_of = re.search(
            r"Projected Pool Price for Hour Ending ([0-9]+) is \$([0-9.]+) as of ([0-9:]+)\.",
            string,
        ).groups()

        # Turn the 'as of' value into a datetime object.
        as_of = self.create_as_of_timestamp(as_of)
        hour_end = self.create_hour_end_timestamp(as_of, hour_end)

        return CurrentProjectedPrice(
            b=b, hour_end=hour_end, as_of=as_of, price=float(price)
        )

    def parse_historical_projected_prices(
        self, b: BeautifulSoup
    ) -> list[HistoricalProjectedPrice]:
        """Extract the historical projected pool prices."""
        logger.debug(f"Parsing historical projected pool prices...")

        # Find the string "Date (HE)", then get the enclosing table.
        table = b.find(string="Date (HE)").find_parent("table")
        historical_prices = []

        # Iterate over the rows, skipping the first one.
        for tr in table.find_all("tr")[1:]:
            hour_end, as_of, price, volume = list(tr.strings)

            # Parse out the month/day/year (why, AESO? why!).
            date, hour = hour_end.split(" ")
            month, day, year = date.split("/")  # Get the actual current time.
            now = datetime.now(pytz.timezone("America/Edmonton"))

            # Do the hour switcharoo if it's 24.
            if hour == "24":
                hour = "23"
                advance_hour = True
            else:
                advance_hour = False

            hour_end = datetime(
                year=int(year),
                month=int(month),
                day=int(day),
                hour=int(hour),
                minute=0,
                tzinfo=now.tzinfo,
            )

            if advance_hour:
                hour_end = hour_end + timedelta(hours=1)

            as_of = self.create_as_of_timestamp(as_of)

            historical_prices.append(
                HistoricalProjectedPrice(
                    b=b,
                    hour_end=hour_end,
                    as_of=as_of,
                    price=float(price),
                    volume=int(volume),
                )
            )

        return historical_prices

    def parse(self, b: BeautifulSoup) -> SystemMarginalPrice:
        """Parse the System Marginal Price page."""
        logger.debug(f"Parsing system marginal price...")

        now = datetime.now(tz=timezone.utc)

        # Build the main object...
        smp = SystemMarginalPrice(
            b=b,
            timestamp=now,
            current=self.parse_current_projected_price(b),
            historical=self.parse_historical_projected_prices(b),
        )

        logger.debug(
            f"Parsed system marginal price with timestamp '{smp.current.as_of}'."
        )

        # ...and return it.
        return smp
