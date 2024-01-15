import logging
import re
import dateparser
from .base import BaseParser
from bs4 import BeautifulSoup
from abpower.data.current_supply_demand import (
    CurrentSupplyDemand,
    Summary,
    Generation,
    Interchange,
    Asset,
)
from datetime import datetime, timezone


logger = logging.getLogger(__name__)

# Mapping of summary values.
summary_map = {
    "Alberta Total Net Generation": "alberta_total_net_generation",
    "Net Actual Interchange": "net_actual_interchange",
    "Alberta Internal Load (AIL)": "alberta_internal_load",
    "Net-To-Grid Generation": "net_to_grid_generation",
    "Contingency Reserve Required": "contingency_reserve_required",
    "Dispatched Contingency Reserve (DCR)": "dispatched_contingency_reserve",
    "Dispatched Contingency Reserve -Gen": "dispatched_contingency_reserve_gen",
    "Dispatched Contingency Reserve -Other": "dispatched_contingency_reserve_other",
    "LSSi Armed Dispatch": "lssi_armed_dispatch",
    "LSSi Offered Volume": "lssi_offered_volume",
}


class CurrentSupplyDemandParser(BaseParser):
    """
    Parser class for the Current Supply Demand page.
    """

    path = "Market/Reports/CSDReportServlet"

    def parse_summary(self, b: BeautifulSoup) -> Summary:
        """Extract values from the 'Summary' table."""
        logger.debug(f"Parsing summary table...")

        # Look for the string "SUMMARY", then get the enclosing table.
        table = b.find(string="SUMMARY").find_parent("table")
        values = {}

        # Iterate over the values in the mapping above, find them in the table,
        # and then convert them to integers.
        for source, destination in summary_map.items():
            values[destination] = int(table.find(string=source).next.text)

        # Return all the summary values.
        return Summary(b=table, **values)

    def parse_generation(self, b: BeautifulSoup) -> list[Generation]:
        """Extract values from the 'Generation' table."""
        logger.debug(f"Parsing generation table...")

        # Look for the string "GENERATION", then get the enclosing table.
        table = b.find(string="GENERATION").find_parent("table")
        values = []

        # Iterate over all the <tr> tags in the table except the first two,
        # since they're the header and the column names.
        for generation_type in table.find_all("tr")[2:]:
            # Extract the generation type and the values.
            name, mc, tng, dcr = list(generation_type.strings)

            # Create and append an object for each generation type.
            values.append(
                Generation(b=table, name=name, mc=int(mc), tng=int(tng), dcr=int(dcr))
            )

        # Return all the generation values.
        return values

    def parse_interchange(self, b: BeautifulSoup) -> list[Interchange]:
        """Extract values from the 'Interchange' table."""
        logger.debug(f"Parsing interchange table...")

        # Look for the string "INTERCHANGE", then get the enclosing table.
        table = b.find(string="INTERCHANGE").find_parent("table")
        values = []

        # Iterate over all the <tr> tags in the table, ignoring the first 2
        # since they're the header and the column names.
        for interchange in table.find_all("tr")[2:]:
            # Extract the interchange name and the actual flow.
            name, actual_flow = list(interchange.strings)

            # Create and append an object for each interchange.
            values.append(Interchange(b=table, name=name, actual_flow=int(actual_flow)))

        # Return all the interchanges.
        return values

    def parse_assets(self, b: BeautifulSoup) -> list[Asset]:
        """Extract values from the assets tables."""
        logger.debug(f"Parsing assets tables...")

        # Look for the string "ASSET", then get the enclosing table.
        table = b.find(string="ASSET").find_parent("table").find_parent("table")
        values = []

        # Look for tables with borders, then iterate over each of them.
        for group in table.find_all("table", attrs={"border": 1}):
            # Get the title for the table, and format it a bit.
            name = group.b.text.lower().capitalize()
            logger.debug(f"-> Found '{name}'.")

            sub_type = None
            assets = []

            # Iterate over all the <tr> tags in the table, ignoring the first 1
            # since it's the header.
            for tr in group.find_all("tr")[1:]:
                # Check the if 'bgcolor' attribute is set on the row.
                if "bgcolor" in tr.attrs:
                    bgcolor = tr.attrs["bgcolor"]

                    if bgcolor == "#CEE3F6":
                        # These rows have the "sub type". At present this only
                        # seems to be present for the "GAS" table, but we'll do
                        # it for all tables for future compatibility.
                        sub_type = tr.text
                        logger.debug(f"   -> Found '{sub_type}' sub-type.")

                    else:
                        # These rows are the column headers, we can ignore them.
                        continue

                elif "bgcolor" in tr.td.attrs:
                    # AESO uses the 'bgcolor' attribute on <tr> _and_ <td>
                    # tags, so we can ignore rows where the first cell has
                    # a 'bgcolor' attribute.
                    continue

                else:
                    # Extract the name and the generation values.
                    asset_name, mc, tng, dcr = list(tr.strings)

                    # If we have a sub type corrently set, append it to
                    # the main generation type.
                    if sub_type:
                        generation_type = f"{name} - {sub_type}"
                    else:
                        generation_type = name

                    # Finally, build the object and convert the values to
                    # integers.
                    assets.append(
                        Asset(
                            b=tr,
                            generation_type=generation_type,
                            name=asset_name,
                            mc=int(mc),
                            tng=int(tng),
                            dcr=int(dcr),
                        )
                    )

            logger.debug(f"   Found {len(assets)} assets for '{name}'.")

            # Add the asset to the list.
            values += assets

        # Return all the assets.
        return values

    def parse_timestamp(self, b: BeautifulSoup) -> datetime:
        """Extract and convert the "Last Update" timestamp."""

        # Look for the string "Last Update", and extract the timestamp from it.
        last_update = b.find(string=re.compile("^Last Update")).split(" : ")[1]

        # Convert the timestamp into a datetime object.
        # The timezone will (hopefully, AESO?) always be "America/Edmonton".
        timestamp = dateparser.parse(
            last_update,
            settings={"TIMEZONE": "America/Edmonton", "RETURN_AS_TIMEZONE_AWARE": True},
        )

        return timestamp

    def parse(self, b: BeautifulSoup) -> CurrentSupplyDemand:
        """Parse the Current Supply Demand page."""
        logger.debug(f"Parsing current supply demand...")

        now = datetime.now(tz=timezone.utc)

        # Build the main object...
        o = CurrentSupplyDemand(
            b=b,
            timestamp=now,
            last_update=self.parse_timestamp(b),
            summary=self.parse_summary(b),
            generation=self.parse_generation(b),
            interchange=self.parse_interchange(b),
            assets=self.parse_assets(b),
        )

        logger.debug(f"Parsed current supply demand with timestamp '{o.last_update}'.")

        # ...and return it.
        return o
