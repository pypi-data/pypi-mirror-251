import logging
import bpython
import pytz
from .base import BaseParser
from bs4 import BeautifulSoup
from abpower.data.supply_surplus import (
    HourEndSupplySurplus,
    SupplySurplus,
)
from datetime import datetime, timezone, timedelta


logger = logging.getLogger(__name__)


class SupplySurplusParser(BaseParser):
    """
    Parser class for the System Marginal Price page.
    """

    path = "Market/Reports/SupplySurplusReportServlet"

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

    def parse_hour_end_supply_surpluses(
        self, b: BeautifulSoup
    ) -> list[HourEndSupplySurplus]:
        """Extract the supply surpluses."""
        logger.debug(f"Parsing hour end supply surpluses...")

        # Find the string "Date (HE)", then get the enclosing table.
        table = b.find(string="Date (HE)").find_parent("table")
        hour_end_supply_surpluses = []

        # Iterate over the rows, skipping the first one.
        for tr in table.find_all("tr")[1:]:
            hour_end, status = list(tr.strings)

            # The status can be a '-' if no value is available. If this
            # is the case, set it to None. Otherwise, cast it to an integer.
            if status == "-":
                status = None
            else:
                status = int(status)

            # Convert the hour end into an actual timestamp.
            hour_end = self.create_hour_end_timestamp(hour_end)

            hour_end_supply_surpluses.append(
                HourEndSupplySurplus(b=b, hour_end=hour_end, status=status)
            )

        return hour_end_supply_surpluses

    def parse(self, b: BeautifulSoup) -> SupplySurplus:
        """Parse the Supply Surplus page."""
        logger.debug(f"Parsing supply surplus...")

        now = datetime.now(tz=timezone.utc)

        # Build the main object...
        o = SupplySurplus(
            b=b, timestamp=now, hour_ends=self.parse_hour_end_supply_surpluses(b)
        )

        logger.debug(f"Parsed supply surplus.")

        # ...and return it.
        return o
