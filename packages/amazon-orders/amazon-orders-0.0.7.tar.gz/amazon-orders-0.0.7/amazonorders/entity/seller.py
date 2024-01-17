import logging
from typing import Optional

from bs4 import Tag

from amazonorders.entity.parsable import Parsable
from amazonorders.session import BASE_URL

__author__ = "Alex Laird"
__copyright__ = "Copyright 2024, Alex Laird"
__version__ = "0.0.7"

logger = logging.getLogger(__name__)


class Seller(Parsable):
    def __init__(self,
                 parsed: Tag) -> None:
        super().__init__(parsed)

        self.name: str = self.safe_parse(self._parse_name)
        self.link: Optional[str] = self.safe_parse(self._parse_link)

    def __repr__(self) -> str:
        return "<Seller: \"{}\">".format(self.name)

    def __str__(self) -> str:  # pragma: no cover
        return "Seller: \"{}\"".format(self.name)

    def _parse_name(self) -> str:
        tag = self.parsed.find("a")
        if not tag:
            tag = self.parsed.find("span")
        value = tag.text
        if "Sold by:" in value:
            value = value.split("Sold by:")[1]
        return value.strip()

    def _parse_link(self) -> Optional[str]:
        tag = self.parsed.find("a")
        if tag:
            return "{}{}".format(BASE_URL, tag.attrs["href"])
        else:
            return None
