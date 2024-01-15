import logging
import requests
from typing import Type, Self
from bs4 import BeautifulSoup
from abpower.data import Data
from abpower.exceptions import RequestError


logger = logging.getLogger(__name__)
BASE_URL = "http://ets.aeso.ca/ets_web/ip"


class BaseParser:
    """
    Base parser class for other parser to inherit from.
    """

    _session: requests.Session | None = None

    path = ""
    data_type: Type[Data] = Data

    @property
    def url(self) -> str:
        """Return a URL for the parser."""
        return f"{BASE_URL}/{self.path}"

    @property
    def session(self) -> requests.Session:
        """
        Create a 'Session' object.

        This is mostly a pass-through right now, but allows us to adjust things like
        headers in future if we need to.
        """
        if not self._session:
            # Create a session object and store it.
            self._session = requests.Session()

        return self._session

    def parse(self, b: BeautifulSoup) -> Type[Self]:
        """Parse and return a data object."""
        return self.data_type(b=b)

    def get(self, params: dict = None) -> Type[Self]:
        """
        Get and return a parsed data object for the parser.

        The 'params' argument is currently unused, at least in the base parser.
        """
        # Get the HTML for the page.
        try:
            response = self.session.get(self.url)
            response.raise_for_status()

        except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
        ) as e:
            raise RequestError(f"Failed to request '{self.url}': {e}", o=e)

        # Parse the page with BeautifulSoup.
        b = BeautifulSoup(response.text, "html.parser")

        # Return the parsed version of the page.
        return self.parse(b)
