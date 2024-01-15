import logging
import json
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass, field, fields, asdict
from datetime import datetime
from typing import Any, Type


logger = logging.getLogger(__name__)


@dataclass
class OutputMixin:
    @property
    def as_dict(self) -> dict:
        """
        Return the object as a dictionary, but filter/convert some of the values first.
        """

        def convert(t: str, v: Any) -> str | int | float:
            """Convert values if needed."""
            if type(v) is datetime:
                # Convert datetime objects to strings.
                return v.isoformat()

            return v

        def dict_factory(fs: list) -> dict:
            """Filter out some of the values that are returned."""
            d = {}

            for k, v in fs:
                if k == "b":
                    # Don't include the BeautifulSoup parser object.
                    continue

                # Add the value after converting it.
                d[k] = convert(k, v)

            return d

        return asdict(self, dict_factory=dict_factory)

    @property
    def as_json(self) -> str:
        """
        Return the object in JSON format.
        """

        return json.dumps(self.as_dict)


@dataclass
class Data(OutputMixin):
    """
    Base class to represent data objects.
    """

    # Keep a parser in each one.
    b: BeautifulSoup | Tag = field(repr=False)
