import logging
import bpython
import click
from pathlib import Path
from rich.logging import RichHandler
from rich.console import Console
from abpower.parser import (
    CurrentSupplyDemandParser,
    SystemMarginalPriceParser,
    PoolPriceParser,
    ActualForecastParser,
    DailyAveragePoolPriceParser,
    SupplySurplusParser,
    HourlyAvailableCapabilityParser,
    ETSParser,
)


FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
logger = logging.getLogger("abpower")
console = Console()
stderr = Console(stderr=True)


@click.group
@click.option("-d", "--debug", is_flag=True, help="Debug logging")
def main(debug: bool):
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled.")


@main.command
@click.option(
    "-o",
    "--output",
    type=click.Choice(["json"], case_sensitive=False),
    default="json",
    help="Output type",
    show_default=True,
)
@click.option("-w", "--write-to-file", help="Write output to file")
@click.option(
    "-q",
    "--query",
    multiple=True,
    type=click.Choice(
        [
            "current-supply-demand",
            "actual-forecast",
            "daily-average-pool-price",
            "hourly-available-capability",
            "pool-price",
            "supply-surplus",
            "system-marginal-price",
            "all",
        ]
    ),
    default=["all"],
    help="Query for a specific set of data.",
)
def get(output: str, write_to_file: str, query: tuple):
    logger.debug(f"Querying: {query}")
    logger.debug(f"Output type '{output}' requested.")

    parser = ETSParser()
    data = parser.get(query=query)

    if output == "json":
        if not write_to_file or write_to_file == "-":
            logger.info(f"Writing as '{output}' to stdout...")
            console.print(data.as_json)

        else:
            path = Path(write_to_file)

            logger.info(f"Writing as '{output}' to '{path}'...")
            with open(path, "w") as fp:
                fp.write(data.as_json)
