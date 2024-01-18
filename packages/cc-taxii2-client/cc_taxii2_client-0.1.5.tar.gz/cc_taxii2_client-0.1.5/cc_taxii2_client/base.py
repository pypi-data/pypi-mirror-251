"""base.py"""

from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from base64 import b64encode
from requests import Session
from requests.models import Response


@dataclass
class Stix2ObjectBase(ABC):
    """Base class for STIX2.1 Objects."""


@dataclass
class EnvelopeBase(ABC):
    """Base class for TAXII2.1 Envelope objects."""


class TaxiiClient(ABC):
    """Base class for a TAXII2.1 client.

    Attributes:
        account (str): Account/User name.
        url (str): The TAXII2.1 URL.
        headers (dict[str, str]): The TAXII2.1 request headers
        session (Session): The request session.
    """

    @abstractmethod
    def __init__(self, account: str, api_key: str) -> None:
        """
        Initialize Taxii2.1 client base class.

        Args:
            account (str): Account/Username.
            api_key (str): Password/API-Key.
        """
        self.account: str = account.lower()
        auth = b64encode(f"{self.account}:{api_key}".encode()).decode()
        self.url: str = ""
        self.headers: dict[str, str] = {
            "Accept": "application/taxii+json;version=2.1",
            "Content-Type": "application/taxii+json;version=2.1",
            "Authorization": f"Basic {auth}"
        }
        self.session: Session = Session()

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}(account={repr(self.account)}, "
                f"url={repr(self.url)}, "
                f"headers={repr(self.headers)})")

    @abstractmethod
    def get_collections(self, root: str) -> list[str]:
        """Retrieve collection IDs for API root.

        Args:
            root (str): The API root.

        Returns:
            list[str]: A list of valid collecitons for given API root.
        """
        raise NotImplementedError()

    @abstractmethod
    def _taxii_request(self, root: str, collection_id: str,
                       parameters: str) -> Response:
        """Send a GET request to TAXII2.1 server with provided
        parameters and return the full response object.

        Args:
            root (str): The API root.
            collection_id (str): The Collection ID.
            parameters (str): The request URL parameters.

        Returns:
            Response: The full request response.
        """
        raise NotImplementedError()

    @abstractmethod
    def _get_json(self, root: str, collection_id: str,
                  parameters: str) -> EnvelopeBase:
        """Send a GET request to the TAXII2.1 server with provided
        parameters and return a TAXII2.1 Envelope.

        Args:
            root (str): The API root.
            collection_id (str): The Collection ID.
            parameters (str): The request URL parameters.

        Returns:
            Envelope: A wrapper for the STIX2.1 content.

        """
        raise NotImplementedError()

    # pylint: disable=too-many-arguments
    def get_stix2_objects(self, root: str, collection_id: str | None,
                          limit: int, added_after: str | None,
                          matches: dict[str, str] | None,
                          follow_pages: bool) -> list[Stix2ObjectBase]:
        """Send a GET request to the TAXII2.1 server with provided
        parameters and return a list of STIX2.1 Objects.

        Args:
            root (str): The API root.
            collection_id (str | None): The collection ID. If None, the first
                                         collection found in discovery will be
                                         used.
            limit (int): Limit of STIX2.1 Objects to return per request/page.
            added_after (str | None): Timestamp in the format  of
                                      %Y-%m-%dT%H:%M:%S.%fZ. Will only return
                                      Objects added after this datetime.
            matches (dict[str, str]) | None: Dictionary of {field: value} for
                                           match filtering. Valid fields are:
                                           id, spec_version, type, and version.
                                           Multiple values may be used for the
                                           same field seperated by a comma as
                                           a single string, e.g.
                                           {"id": "id_1,id_2"}.

            follow_pages (bool): True to return all STIX2.1 Objects in the
                                 collection paged by the limit amount,
                                 False to return only the supplied or
                                 default/max limit. Default is False.

        Returns:
            list[Stix2ObjectBase]: A list of STIX2.1 Objects from the request.
        """
        raise NotImplementedError()
