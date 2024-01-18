"""utils.py"""

from __future__ import annotations
from typing import Generator
from .core import CCIndicator


def _search(
        field: str, keyword: str,
        indicators: Generator[list[CCIndicator], None,
                              None]) -> list[CCIndicator]:
    """Search for field defined keyword in data yielded by the Indicator
    generator.
    Args:
        field (str): Indicator field to search.
        keyword (str): Keyword to search for in indicator field.
        indicators (Generator[list[CCIndicator], None, None]): Generator
                                                               function
                                                               returning list
                                                               of Indicators.

    Returns:
        list[CCIndicator]: List of indicators with matching keyword in
                            specified field.
    """
    return [
        indicator for page in indicators if page for indicator in page
        if keyword in getattr(indicator, field, "")
    ]


def count_indicators(
        indicators: Generator[list[CCIndicator], None, None]) -> int:
    """Count the total number of Indicator objects yielded by the Indicator
    generator.

    Args:
        indicators (Generator[list[CCIndicator], None, None]): Generator
                                                               function
                                                               returning list
                                                               of Indicators.

    Returns:
        int: Total number of Indicator objects.

    """
    return sum(len(page) for page in indicators if page)


def ip_search(
        ip_address: str, indicators: Generator[list[CCIndicator], None,
                                               None]) -> list[CCIndicator]:
    """Search for IP addresses in data yielded by the Indicator generator.

    Args:
        ip_address (str): IP address to search for.
        indicators (Generator[list[CCIndicator], None, None]): Generator
                                                               function
                                                               returning list
                                                               of Indicators.

    Returns:
        list[CCIndicator]: List of Indicators with matching ip address in
                          pattern field.

    """
    return _search("pattern", ip_address, indicators)


def description_search(
        description: str, indicators: Generator[list[CCIndicator], None,
                                                None]) -> list[CCIndicator]:
    """Search for a description keyword in data yielded by the Indicator
    generator.

    Args:
        description (str): Description keyword to search for.
        indicators (Generator[list[CCIndicator], None, None]): Generator
                                                               function
                                                               returning list
                                                               of Indicators.

    Returns:
        list[CCIndicator]: List of indicators with matching ip address in
                          pattern field.

    """
    return _search("description", description, indicators)
