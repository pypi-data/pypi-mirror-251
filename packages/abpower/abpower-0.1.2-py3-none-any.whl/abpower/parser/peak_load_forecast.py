import logging
import pytz
import re
from .base import BaseParser
from bs4 import BeautifulSoup
from abpower.data.peak_load_forecast import (
    HourEndPeakLoadForecast,
    DayPeakLoadForecast,
    PeakLoadForecast
)
from datetime import datetime, timezone, timedelta


logger = logging.getLogger(__name__)


class PeakLoadForecastParser(BaseParser):
    """
    Parser class for the 7 Days Hourly Available Capability page.
    """

    path = "Market/Reports/MonthlyPeakLoadForecastReportServlet"

    def create_day_timestamp(self, date: str) -> datetime:
        """Create a datetime object for the 'day' value."""

        # Get the actual current time.
        now = datetime.now(pytz.timezone("America/Edmonton"))

        # Parse out the month, day and year.
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

    def create_hour_end_timestamp(self, date: datetime, hour_end: int) -> datetime:
        """Create a datetime object for the 'hour_end' value."""

        if hour_end == 24:
            hour_end = 23
            advance_hour = True
        else:
            advance_hour = False

        dt = datetime(
            year=date.year,
            month=date.month,
            day=date.day,
            hour=int(hour_end),
            minute=0,
            tzinfo=date.tzinfo
        )

        if advance_hour:
            dt = dt + timedelta(hours=1)

        return dt

    def parse_peak_load_forecast_days(
        self, b: BeautifulSoup
    ) -> list[DayPeakLoadForecast]:
        """
        Parse peak load forecast for each day.
        """
        logger.debug(f"Parsing peak load forecasts...")

        # Find the string "HE", then get the enclosing table.
        table = b.find(string="HE").find_parent("table")
        days = []

        # Iterate over the rows, ignoring the first one.
        for tr in table.find_all('tr')[1:]:
            cells = list(tr.strings)
            day = self.create_day_timestamp(cells[0])
            percentages = cells[1:]

            hour_ends = []

            for hour_end, percentage in zip(range(1, 25), percentages):
                hour_end = self.create_hour_end_timestamp(day, hour_end)
                percentage = int(percentage.removesuffix("%"))

                hour_ends.append(
                    HourEndPeakLoadForecast(
                        b=tr,
                        hour_end=hour_end,
                        percentage=percentage
                    )
                )

            days.append(
                DayPeakLoadForecast(
                    b=table,
                    day=day,
                    hour_ends=hour_ends
                )
            )

        return days

    def parse_month_to_date_peak_demand(self, b: BeautifulSoup) -> int:
        """
        Extract the month-to-date peak demand.
        """
        # Find the string "HE", then get the enclosing table.
        table = b.find(string=re.compile(r".*MTD Peak Demand.*")).find_parent("table")

        # Get the peak demand and return it
        return int(table.find_all('td')[1].text.strip())

    def parse_set_on(self, b: BeautifulSoup) -> datetime:
        """
        Extract the 'set on' timestamp for the peak demand.
        """
        # Find the string "HE", then get the enclosing table.
        table = b.find(string=re.compile(r".*MTD Peak Demand.*")).find_parent("table")

        # Get the 'set on' value.
        set_on = table.find_all('td')[3].text.strip()
        day, hour_end = re.match(r"([0-9/]+)\s+?HE\s+?([0-9]+)", set_on).groups()

        # Create timestamps.
        day = self.create_day_timestamp(day)
        hour_end = self.create_hour_end_timestamp(day, int(hour_end))

        return hour_end

    def parse(self, b: BeautifulSoup) -> PeakLoadForecast:
        """
        Parse the peak load forecast page.
        """
        logger.debug(f"Parsing peak load forecast...")

        now = datetime.now(tz=timezone.utc)

        # Build the main object...
        o = PeakLoadForecast(
            b=b,
            timestamp=now,
            peak_demand=self.parse_month_to_date_peak_demand(b),
            set_on=self.parse_set_on(b),
            days=self.parse_peak_load_forecast_days(b)
        )

        logger.debug(f"Parsed peak load forecast.")

        # ...and return it.
        return o
