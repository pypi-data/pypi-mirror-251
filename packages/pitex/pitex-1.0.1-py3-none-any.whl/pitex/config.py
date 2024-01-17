from typing import Optional
from enum import Enum

import pytex.package as package


class PageType(Enum):
    """Enum for the page type of the document.

    Args:
        Enum (str): The page type of the document.
    """

    A4 = "a4"
    """A4 page type."""
    A5 = "a5"
    """A5 page type."""
    LETTER = "letter"
    """Letter page type."""


class LatexConfig:
    page_type: Optional[PageType]
    page_numbering: bool
    packages: list[package.Package]

    def __init__(
        self,
        page_type: PageType = PageType.A4,
        page_numbering: bool = False,
        packages: list[str] = [],
    ):
        self.page_type = page_type
        self.page_numbering = page_numbering
        self.packages = list(map(package.Package, packages))

    def add_package(self, name: str, options: list[str] = []):
        self.packages.append(package.Package(name, options))

        return self

    def add_packages(self, names: list[str]):
        self.packages.extend(list(map(package.Package, names, [[] for _ in names])))

        return self
