import logging
try:
    import ujson as json  # type: ignore # noqa
except ImportError:
    import json

from .events import EventHandler, AsyncEventHandler
from .models import User

API_VERSION = "v1"


class BaseClient:
    def __init__(self,
                 token: str,
                 widget_id: str = None,
                 longpool_timeout: int = 1,
                 logging_level: int = logging.INFO,
                 is_async: bool = False
                 ) -> None:
        """Donatello API BaseClient

            :param token: Donatello API token
            :param widget_id: Donatello widget ID
            :param longpool_timeout: Long polling timeout
            :param logging_level: Logging level

            :type token: str
            :type widget_id: str
            :type longpool_timeout: int
            :type logging_level: int

            :return: BaseClient
            :rtype: BaseClient

            :raises Exception: If API returns error
        """
        self._token = token
        self._widget_id = widget_id
        self._longpool_timeout = longpool_timeout

        # URLs
        self._api_url = f"https://donatello.to/api/{API_VERSION}/"
        self._widget_url = f"https://donatello.to/widget/{widget_id}/token/{token}/"

        # Logging
        self._logger = logging.getLogger("donatello")
        self._logger.setLevel(logging_level)

        if is_async:
            self._on_ready = AsyncEventHandler()
            self._on_donate = AsyncEventHandler()
            self._on_error = AsyncEventHandler()
            import aiohttp
            self._session = aiohttp.ClientSession(json_serialize=json.dumps)
        else:
            self._on_ready = EventHandler()
            self._on_donate = EventHandler()
            self._on_error = EventHandler()
            import requests
            self._session = requests.Session()

        # Long polling
        if not widget_id:
            self._logger.warning(
                "Widget ID is not specified. You can't use long polling.")
            self._is_long_polling = False
        else:
            self._is_long_polling = True
            self._longpool_timeout = longpool_timeout

        self._stop_long_polling = False

        self._headers = {"X-Token": self._token}
        self._session.headers.update(self._headers)

        self._user: User = None

    @property
    def nickname(self) -> str:
        """Client nickname"""
        return self._user.nickname

    @property
    def public_id(self) -> str:
        """Client public ID"""
        return self._user.public_id

    @property
    def page(self) -> str:
        """Client page"""
        return self._user.page

    @property
    def is_active(self) -> bool:
        """Client activity"""
        return self._user.is_active

    @property
    def is_public(self) -> bool:
        """Client public status"""
        return self._user.is_public

    @property
    def donates(self) -> list:
        """Client donates"""
        return self._user.donates

    @property
    def created_at(self) -> str:
        """Client created at"""
        return self

    def on_ready(self, listener):
        """Decorator for client event"""
        self._on_ready.add_listener(listener)
        return listener

    def on_donate(self, listener):
        """Decorator for donate event"""
        self._on_donate.add_listener(listener)
        return listener

    def on_error(self, listener):
        """Decorator for error event"""
        self._on_error.add_listener(listener)
        return listener

    def remove_client_listener(self, listener):
        """Remove client event listener"""
        self._on_ready.listeners.remove(listener)

    def remove_donate_listener(self, listener):
        """Remove donate event listener"""
        self._on_donate.listeners.remove(listener)

    def remove_error_listener(self, listener):
        """Remove error event listener"""
        self._on_error.listeners.remove(listener)

    def __str__(self) -> str:
        return f"Donatello API wrapper API version: {API_VERSION}"

    def __repr__(self) -> str:
        return f"Donatello API wrapper API version: {API_VERSION}"
