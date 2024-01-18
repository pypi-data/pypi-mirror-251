"""exceptions.py"""

from __future__ import annotations


class TaxiiError(Exception):
    """Base error class for TaxiiClient.

    Args:
        msg (str): Human readable string describing the exception.

    Attributes:
        msg (str): Human readable string describing the exception.

    """

    def __init__(self, msg: str) -> None:
        """Initialize TaxiiError base class.

        Args:
            msg (str): Human readable string describing the exception.

        """
        self.msg = msg


class TaxiiCollectionError(TaxiiError):
    """TaxiiClient Collection error."""


class TaxiiConnectionError(TaxiiError):
    """TaxiiClient connection error."""


class TaxiiAuthorizationError(TaxiiError):
    """TaxiiClient authorization error."""


class TaxiiDatetimeError(TaxiiError):
    """TaxiiClient datetime error."""


class TaxiiFilterError(TaxiiError):
    """TaxiiClient filter error."""
