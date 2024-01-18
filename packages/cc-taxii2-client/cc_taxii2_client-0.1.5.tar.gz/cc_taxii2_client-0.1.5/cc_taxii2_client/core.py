"""core.py"""

from __future__ import annotations
from typing import Generator
from datetime import datetime
from json import loads
from json.decoder import JSONDecodeError
from dataclasses import dataclass
from requests.models import Response
from requests.exceptions import RequestException
from .base import TaxiiClient
from .base import Stix2ObjectBase, EnvelopeBase
from .exceptions import (TaxiiCollectionError, TaxiiConnectionError,
                         TaxiiAuthorizationError, TaxiiDatetimeError,
                         TaxiiFilterError)


# pylint: disable=too-many-instance-attributes
@dataclass
class CCIndicator(Stix2ObjectBase):
    """CloudCover STIX2.1 Indicator object."""
    created: str
    description: str
    id: str
    modified: str
    name: str
    pattern: str
    pattern_type: str
    pattern_version: str
    spec_version: str
    type: str
    valid_from: str


@dataclass
class Envelope(EnvelopeBase):
    """TAXII2.1 Envelope object."""
    objects: list[dict[str, str]] | None = None
    more: bool | None = None
    next: str | None = None


class CCTaxiiClient(TaxiiClient):
    """CloudCover TAXII2.1 client.

    Attributes:
        account (str): Account/Username.
        url (str): The CloudCover TAXII2.1 URL.
        headers (dict[str, str]): The TAXII2.1 request headers
        session (Session): The request session.
    """

    def __init__(self, account: str, api_key: str) -> None:
        super().__init__(account, api_key)
        self.url: str = "https://taxii2.cloudcover.net"

    def get_collections(self, root: str = "api") -> list[str]:
        """Retrieve collection IDs for API root.

        Args:
            root (str): The API root.

        Returns:
            list[str]: A list of valid collecitons for given API root.
        """
        try:
            collections: list[str] = list(
                map(
                    lambda item: item["id"],
                    loads(
                        self.session.get(
                            f"{self.url}/{root}/collections/",
                            headers=self.headers).text)["collections"]))
        except RequestException as exc:
            raise TaxiiConnectionError(
                "Could not connect to the TAXII2 server.") from exc
        except JSONDecodeError as exc:
            raise TaxiiAuthorizationError("Unknown credentials.") from exc
        except (AttributeError, KeyError) as exc:
            raise TaxiiCollectionError("No Collections found.") from exc
        return collections

    def _taxii_request(self, root: str, collection_id: str,
                       parameters: str) -> Response:
        """Send a GET request to TAXII2.1 server with provided
        parameters and return the full response object.

        Args:
            root (str): The API root.
            collection_id (str): The collection ID.
            parameters (str): The request URL parameters.

        Returns:
            Response: The full request response.
        """
        try:
            response = self.session.get(
                f"{self.url}/{root}/collections"
                f"/{collection_id}/{parameters}",
                headers=self.headers)
        except RequestException as exc:
            raise TaxiiConnectionError(
                "Could not connect to the TAXII2.1 server.") from exc
        return response

    def _get_json(self, root: str, collection_id: str,
                  parameters: str) -> Envelope:
        """Send a GET request to the TAXII2.1 server with provided
        parameters and return a TAXII2.1 Envelope.

        Args:
            root (str): The API root.
            collection_id (str): The Collection ID.
            parameters (str): The request URL parameters.

        Returns:
            Envelope: A wrapper for the STIX2.1 content.
        """
        try:
            response = self._taxii_request(root, collection_id, parameters)
            response_json = Envelope(**loads(response.text))
        except JSONDecodeError as exc:
            raise TaxiiAuthorizationError("Unknown credentials.") from exc
        except TypeError as exc:
            raise TaxiiConnectionError(
                "Could not connect to the TAXII2.1 server.") from exc
        return response_json

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-locals
    def get_cc_indicators_generator(
        self,
        collection_id: str | None = None,
        limit: int = 1000,
        private: bool = False,
        added_after: str | None = None,
        matches: dict[str, str] | None = None,
        follow_pages: bool = False
    ) -> Generator[list[CCIndicator], None, None]:
        """Send a GET request to the TAXII2.1 server with provided
        parameters and generate a list of CloudCover STIX2.1 Indicator Objects.

        Args:
            collection_id (str | None): The collection ID. If None, the first
                                        collection found in discovery will be
                                        used.
            limit (int): Limit of CloudCover STIX2.1 Indicator objects to
                         return per request/page, server default/max is 1000.
            private (bool): True to use the account API root, False to
                            use the public API root. Default it False.
            added_after (str | None): Timestamp in the format  of
                                      %Y-%m-%dT%H:%M:%S.%fZ. Will only return
                                      Indicators added after this datetime.
                                      Default None will return all Indicators.
            matches (dict[str, str]) | None: Dictionary of {field: value} for
                                           match filtering. Valid fields are:
                                           id, spec_version, type, and version.
                                           Multiple values may be used for the
                                           same field seperated by a comma as
                                           a single string, e.g.
                                           {"id": "id_1,id_2"}.
            follow_pages (bool): True to return all Indicators in the
                                 collection paged by the limit amount,
                                 False to return only the supplied or
                                 default/max limit. Default is False.

        YIELDS:
            Generator[list[CCIndicator], None, None]: A list of CloudCover
                                                      STIX2.1 Indicators
                                                      Objects from the request.
        """
        root = self.account if private else "api"
        match_fields = ["id", "spec_version", "type", "version"]
        objects_string = f"objects/?limit={limit}"
        if added_after:
            try:
                datetime.strptime(added_after, '%Y-%m-%dT%H:%M:%S.%fZ')
                objects_string += "&added_after=" + added_after
            except ValueError as exc:
                raise TaxiiDatetimeError(
                    "Invalid datetime format. Expected %Y-%m-%dT%H:%M:%S.%fZ"
                ) from exc
        if matches:
            if not all(key in match_fields for key in matches.keys()):
                raise TaxiiFilterError("Illegal filter match field.")
            for k, v in matches.items():
                match_string = f"&match[{k}]={v}"
                objects_string += match_string

        try:
            collection = (collection_id
                          if collection_id else self.get_collections(root)[0])
            if not follow_pages:
                response_json = self._get_json(root, collection,
                                               objects_string)
                if not response_json:
                    return
                if isinstance(response_json.objects, list):
                    yield [CCIndicator(**_) for _ in response_json.objects]
                    return
        except (AttributeError, KeyError) as exc:
            raise TaxiiCollectionError("Collection does not exist.") from exc

        next_string = ""
        while True:
            try:
                parameters = objects_string + next_string
                response_json = self._get_json(root, collection, parameters)
                if not response_json:
                    break
                if isinstance(response_json.objects, list):
                    yield [CCIndicator(**_) for _ in response_json.objects]
                if not response_json.more:
                    break
                next_id = response_json.next
                next_string = f"&next={next_id}"
            except (AttributeError, KeyError) as exc:
                raise TaxiiCollectionError(
                    "Collection does not exist.") from exc
        return
