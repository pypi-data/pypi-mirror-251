import logging
import pytz
import re
from .base import BaseParser
from bs4 import BeautifulSoup
from abpower.data.hourly_available_capability import (
    HourlyAvailableCapability,
    GenerationHourlyAvailableCapability,
    HourEndHourlyAvailableCapability,
)
from datetime import datetime, timezone, timedelta


logger = logging.getLogger(__name__)


class HourlyAvailableCapabilityParser(BaseParser):
    """
    Parser class for the 7 Days Hourly Available Capability page.
    """

    path = "Market/Reports/SevenDaysHourlyAvailableCapabilityReportServlet"

    def create_hour_end_timestamp(self, date: str, hour: int) -> datetime:
        """Create a datetime object for the 'hour end' value."""

        # Get the actual current time.
        now = datetime.now(pytz.timezone("America/Edmonton"))

        # Parse out the day, month and year (the right way this time!).
        day, month, year = date.split("-")

        # Unfortunately, it uses month names instead of numbers.
        month = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12,
        }.get(month)

        # Do the whole "hour 24 is hour 0 thing".
        if hour == 24:
            hour = 23
            advance_hour = True
        else:
            advance_hour = False

        dt = datetime(
            year=int(year),
            month=int(month),
            day=int(day),
            hour=hour,
            minute=0,
            tzinfo=now.tzinfo,
        )

        if advance_hour:
            dt = dt + timedelta(hours=1)

        return dt

    def parse_generation_hourly_available_capability(
        self, b: BeautifulSoup
    ) -> list[GenerationHourlyAvailableCapability]:
        """Extract the hourly available capability by generation type."""
        logger.debug(f"Parsing hourly available capability by generation type...")

        # Find the string "Hour Ending", then get the enclosing table.
        table = b.find(string="Hour Ending").find_parent("table")

        generation_types = []
        hour_ends = []
        current_type = None
        current_mc = None

        # Iterate over the rows, skipping the first one.
        for tr in table.find_all("tr")[1:]:
            if "colspan" in tr.td.attrs:
                # Each section is ended with a blank row, which we can find by
                # looking for the 'colspan' attribute it has set.
                continue

            if "rowspan" in tr.td.attrs:
                # In each section there's a cell with the generation type and
                # maximum capability of that type, which we can find by looking
                # for the 'rowspan' attribute it has set.

                # Set the current generation type.
                # If it was already set, finish off the previous type.
                if current_type:
                    logger.debug(f"Finished parsing '{current_type}'.")
                    generation_types.append(
                        GenerationHourlyAvailableCapability(
                            b=tr,
                            generation_type=current_type,
                            hour_ends=hour_ends,
                            mc=current_mc,
                        )
                    )

                    hour_ends = []

                current_type = tr.td.br.previous.text.lower().capitalize()

                logger.debug(f"Found generation type '{current_type}'.")

                # Get the maximum capability.
                current_mc = int(re.search(r"\s?([0-9]+)", tr.td.em.text).groups()[0])

                # Strip off the first cell.
                values = [td.text for td in tr.find_all("td")[1:]]

            else:
                values = list(tr.strings)

            # Pop the date off the front.
            date = values.pop(0)

            # Strip the % sign off the values and convert them to floats.
            values = [float(value.removesuffix("%")) for value in values]

            percentages = list(zip(range(1, 25), values))

            hour_ends += [
                HourEndHourlyAvailableCapability(
                    b=tr,
                    hour_end=self.create_hour_end_timestamp(date=date, hour=hour),
                    percentage=percentage,
                )
                for hour, percentage in percentages
            ]

        return generation_types

    def parse_timestamp(self, b: BeautifulSoup) -> datetime:
        """Extract and convert the "Last Update" timestamp."""

        # Look for the string "Last Updated", and extract the timestamp from it.
        last_update = b.find(string=re.compile("^Last Updated")).split(": ")[1]

        year, month, day = last_update.split(" ")[0].split("/")
        hour, minute, second = last_update.split(" ")[1].split(":")

        # Convert the timestamp into a datetime object.
        # The timezone will (hopefully, AESO?) always be "America/Edmonton".
        timestamp = datetime(
            year=int(year),
            month=int(month),
            day=int(day),
            hour=int(hour),
            minute=int(minute),
            second=int(second),
            tzinfo=pytz.timezone("America/Edmonton"),
        )

        return timestamp

    def parse(self, b: BeautifulSoup) -> HourlyAvailableCapability:
        """Parse the 7 Days Hourly Available Capability page."""
        logger.debug(f"Parsing 7 days hourly available capability...")

        now = datetime.now(tz=timezone.utc)

        # Build the main object...
        o = HourlyAvailableCapability(
            b=b,
            timestamp=now,
            last_updated=self.parse_timestamp(b),
            generation_types=self.parse_generation_hourly_available_capability(b),
        )

        logger.debug(f"Parsed 7 days hourly available capability.")

        # ...and return it.
        return o
