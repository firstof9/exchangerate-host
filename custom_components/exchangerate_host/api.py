"""Sample API Client."""
import asyncio
import logging
import socket
from typing import Optional

import aiohttp
import async_timeout

from .const import BASE_URL, TIMEOUT

_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class ExchangeRateHostApiClient:
    """Class for ExchangeRateHost API calls."""

    def __init__(
        self,
        username: str = None,
        password: str = None,
        session: aiohttp.ClientSession = None,
        currency: str = None,
    ) -> None:
        """Sample API Client."""
        self._username = username
        self._password = password
        self._session = session
        self._url = BASE_URL
        self._currency = currency

    async def async_get_symbols(self) -> dict:
        """Get symbol date from the API."""
        url = f"{self._url}symbols"
        data = await self.api_wrapper("get", url)
        return data["symbols"]

    async def async_get_data(self) -> dict:
        """Get data from the API."""
        url = f"{self._url}latest?base={self._currency}"
        return await self.api_wrapper("get", url)

    async def api_wrapper(
        self, method: str, url: str, data: dict = None, headers: dict = None
    ) -> dict:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(TIMEOUT):
                if method == "get":
                    response = await self._session.get(url, headers=headers)
                    return await response.json()

        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                url,
                exception,
            )

        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                url,
                exception,
            )
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                url,
                exception,
            )
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)
