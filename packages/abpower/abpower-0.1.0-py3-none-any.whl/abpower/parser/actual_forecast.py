import logging
import pytz
from .base import BaseParser
from bs4 import BeautifulSoup
from abpower.data.actual_forecast import ActualForecast, HourEndActualForecast
from datetime import datetime, timezone, timedelta


logger = logging.getLogger(__name__)


class ActualForecastParser(BaseParser):
    """
    Parser class for the System Marginal Price page.
    """

    path = "Market/Reports/ActualForecastWMRQHReportServlet"

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

    def parse_hour_end_actual_forecasts(
        self, b: BeautifulSoup
    ) -> list[HourEndActualForecast]:
        """Extract the actual / forecast entries."""
        logger.debug(f"Parsing hour end actual / forecast entries...")

        # Find the string "Date (HE)", then get the enclosing table.
        table = b.find(string="Date (HE)").find_parent("table")
        hour_end_actual_forecasts = []

        # Iterate over the rows, skipping the first one.
        for tr in table.find_all("tr")[1:]:
            (
                hour_end,
                forecast_pool_price,
                actual_posted_pool_price,
                forecast_ail,
                actual_ail,
                difference,
            ) = list(tr.strings)

            # The values can be a '-' if they're not available. If this
            # is the case, set them to 'None'. Otherwise, cast them to
            # the correct values..
            if forecast_pool_price == "-":
                forecast_pool_price = None
            else:
                forecast_pool_price = float(forecast_pool_price)

            if actual_posted_pool_price == "-":
                actual_posted_pool_price = None
            else:
                actual_posted_pool_price = float(actual_posted_pool_price)

            if forecast_ail == "-":
                forecast_ail = None
            else:
                # On this page, "," is used as a number separator.
                # No, I don't know why either.
                forecast_ail = float(forecast_ail.replace(",", ""))

            if actual_ail == "-":
                actual_ail = None
            else:
                actual_ail = float(actual_ail.replace(",", ""))

            if difference == "-":
                difference = None
            else:
                # It's fair to assume the difference would also use commas.
                # However, that would mean a difference of over 10,000MW.
                # If that was the case, there probably wouldn't be a power
                # grid left to run this on. Or serve the AESO website.
                difference = int(difference.replace(",", ""))

            # Convert the hour end into an actual timestamp.
            hour_end = self.create_hour_end_timestamp(hour_end)

            hour_end_actual_forecasts.append(
                HourEndActualForecast(
                    b=b,
                    hour_end=hour_end,
                    forecast_pool_price=forecast_pool_price,
                    actual_posted_pool_price=actual_posted_pool_price,
                    forecast_ail=forecast_ail,
                    actual_ail=actual_ail,
                    difference=difference,
                )
            )

        return hour_end_actual_forecasts

    def parse(self, b: BeautifulSoup) -> ActualForecast:
        """Parse the Actual / Forecast page."""
        logger.debug(f"Parsing actual / forecast...")

        now = datetime.now(tz=timezone.utc)

        # Build the main object...
        o = ActualForecast(
            b=b, timestamp=now, hour_ends=self.parse_hour_end_actual_forecasts(b)
        )

        logger.debug(f"Parsed actual / forecast.")

        # ...and return it.
        return o
