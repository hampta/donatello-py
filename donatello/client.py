try:
    import ujson as json  # type: ignore # noqa
except ImportError:
    import json

import logging
import threading
import time
from typing import Union

from .base import BaseClient
from .models import ClientList, DonateList, LongpoolDonate, User

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s: %(message)s", level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)


class Donatello(BaseClient):

    def __init__(self,
                 token: str,
                 widget_id: str = None,
                 longpool_timeout: int = 1,
                 logging_level: int = logging.INFO
        ) -> None:
        """Donatello API wrapper

            :param token: Donatello API token
            :param widget_id: Donatello widget ID
            :param longpool_timeout: Long polling timeout
            :param logging_level: Logging level

            :type token: str
            :type widget_id: str
            :type longpool_timeout: int
            :type logging_level: int

            :return: Donatello API wrapper
            :rtype: Donatello

            :raises Exception: If API returns error

            Basic Usage::

                >>> from donatello.client import Donatello
                >>> from donatello.models import LongpoolDonate, User
                >>> client = Donatello("your_token", "widget_id")

                >>> print(client.get_me()) # Get user info
                >>> print(client.get_donates()) # Get donates
                >>> print(client.get_clients()) # Get clients

                >>> @client.on_ready # On client event
                >>> def on_ready(client: User):
                >>>     print(f"Client name: {client.nickname}")
                >>>     print(f"Total donates: {client.donates.total_amount}")

                >>> @client.on_donate # On donate event
                >>> def on_donate(donate: LongpoolDonate):
                >>>     print("------- NEW DONATE -------")
                >>>     print(f"Nickname: {donate.name}")
                >>>     print(f"Amount: {donate.amount} {donate.currency}")
                >>>     print(f"Message: {donate.message}")
                >>>     print(f"Date: {donate.created_at}")
                >>>     print(f"Client name: {donate.client_name}")
                >>> client.start() # Start long polling

        """
        super().__init__(token=token,
                         widget_id=widget_id,
                         longpool_timeout=longpool_timeout,
                         logging_level=logging_level,
                         is_async=False)

    def _request(self,
                 method: str,
                 url: str,
                 endpoint: str,
                 **kwargs
        ) -> dict:
        """Make a request to API
            Returns :class: `dict` with response

            :param method: HTTP method
            :param url: API url
            :param endpoint: API endpoint
            :param **kwargs: Additional arguments for requests.request
        """
        resp = self._session.request(
            method, url + endpoint, **kwargs)
        data: dict = json.loads(resp.text)
        self._logger.debug(f"Response: {data}")
        if data.get("success") is False:
            self._error_handler(data)
        return data

    def _error_handler(self, message: Union[str, dict]) -> None:
        """Handle errors
            :param message: Error message
        """
        self._on_error.handle_event([message])
        self._logger.error(message)

    def get_me(self) -> User:
        """Get user info
            Returns :class: `User` with user info
        """
        self._user = User(**self._request("GET", self._api_url, "me"))
        return self._user

    def get_donates(self, page: int = 0, per_page: int = 20) -> DonateList:
        """Get donates
            Returns :class: `DonateList` with donates
        """
        return DonateList(**self._request("GET", self._api_url, "donates", params={
            "page": page,
            "size": per_page
        }))

    def get_clients(self) -> ClientList:
        """Get clients
            Returns :class: `ClientList` with clients
        """
        return ClientList(**self._request("GET", self._api_url, "clients"))

    def _long_polling(self) -> None:
        """Long polling method"""
        self._logger.info("Long polling started.")
        self._on_ready.handle_event(self.get_me())
        while not self._stop_long_polling:
            try:
                resp = self._request("GET", self._widget_url, "info")
                if resp.get("clientName"):
                    self._on_donate.handle_event([LongpoolDonate(**resp)])
                elif not resp.get("success"):
                    self._error_handler(resp)
            except Exception as e:
                self._error_handler(e)
            time.sleep(self._longpool_timeout)

    def start(self) -> None:
        """Start long polling"""
        if self._is_long_polling:
            threading.Thread(target=self._long_polling).start()
        else:
            self._logger.warning(
                "Long polling is disabled. You can't use on_donate, on_error events.")
            self._logger.warning(
                "You can enable long polling by specifying widget ID in constructor.")

    def stop(self) -> None:
        """Stop long polling"""
        self._stop_long_polling = True
        self._logger.info("Long polling stopped.")

    def __del__(self) -> None:
        self.stop()