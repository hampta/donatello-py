try:
    import ujson as json  # type: ignore # noqa
except ImportError:
    import json

import asyncio
import logging

from .base import BaseClient
from .models import ClientList, DonateList, LongpoolDonate, User

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s: %(message)s", level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)


class AsyncDonatello(BaseClient):
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

            Longpoll::

                >>> from donatello.client import Donatello
                >>> from donatello.models import LongpoolDonate
                >>> client = Donatello("your_token", "widget_id")

                >>> @client.on_ready # On client event
                >>> async def on_ready():
                >>>     user = await client.get_me()
                >>>     print(f"Client name: {user.nickname}")
                >>>     print(f"Total donates: {user.donates.total_amount}")

                >>> @client.on_donate # On donate event
                >>> async def on_donate(donate: LongpoolDonate):
                >>>     print("------- NEW DONATE -------")
                >>>     print(f"Nickname: {donate.name}")
                >>>     print(f"Amount: {donate.amount} {donate.currency}")
                >>>     print(f"Message: {donate.message}")
                >>>     print(f"Date: {donate.created_at}")
                >>>     print(f"Client name: {donate.client_name}")
                >>> client.start() # Start long polling
            
            Basic Usage::

                >>> import asyncio
                >>> from donatello.client import Donatello
                >>> from donatello.models import LongpoolDonate
                >>> client = Donatello("your_token", "widget_id")

                >>> async def main():
                >>>     user = await client.get_me()
                >>>     print(f"Client name: {user.nickname}")
                >>>     print(f"Total donates: {user.donates.total_amount}")
                >>>     donates = await client.get_donates()
                >>>     print(f"Donates: {donates}")
                >>>     clients = await client.get_clients()
                >>>     print(f"Clients: {clients}")

                >>> asyncio.run(main())
        """
        super().__init__(token=token,
                         widget_id=widget_id,
                         longpool_timeout=longpool_timeout,
                         logging_level=logging_level,
                         is_async=True)

        # Long polling thread
        self._loop = asyncio.get_event_loop()

    async def _request(self,
                       method: str,
                       url: str,
                       endpoint: str,
                       **kwargs
                       ) -> dict:
        """
        
            Send request to API
            Returns :class: `dict` with response

            :param method: HTTP method
            :param url: API url
            :param endpoint: API endpoint
            :param **kwargs: Additional arguments for aiohttp.request
        """
        async with self._session.request(method, url + endpoint, **kwargs) as resp:
            data: dict = await resp.json(loads=json.loads)
            self._logger.debug(f"Response: {data}")
            if data.get("success") is False:
                await self._error_handler(data)
            return data

    async def _error_handler(self, data: dict) -> None:
        """
        
            Handle errors

            :param data: API response
            :type data: dict
        """
        self._logger.error(f"Error: {data}")
        await self._on_error.handle_event([data])

    async def get_me(self) -> User:
        """
            Get user info

            :return: User info
            :rtype: User
        """
        data = await self._request("GET", self._api_url, "me")
        self._user = User(**data)
        return self._user

    async def get_clients(self) -> ClientList:
        """
            Get clients list

            :return: Clients list
            :rtype: ClientList
        """
        data = await self._request("GET", self._api_url, "clients")
        return ClientList(**data)

    async def get_donates(self) -> DonateList:
        """
            Get donates list

            :return: Donates list
            :rtype: DonateList
        """
        data = await self._request("GET", self._api_url, "donates")
        return DonateList(**data)

    async def _long_polling(self) -> None:
        """Long polling thread"""
        self._logger.info("Long polling started")
        await self._on_ready.handle_event(await self.get_me())
        while not self._stop_long_polling:
            data = await self._request("GET", self._widget_url, "info")
            try:
                if data.get("success") is None:
                    await self._on_donate.handle_event(LongpoolDonate(**data))
                elif data.get("success") is False:
                    await self._error_handler(data)
            except Exception as e:
                await self._error_handler(data)
            await asyncio.sleep(self._longpool_timeout)
        await self.close()
        self._logger.info("Long polling stopped")

    async def _start_long_polling(self) -> None:
        """Start long polling thread"""
        self._stop_long_polling = False
        await self._long_polling()

    def start(self) -> None:
        """Start long polling"""
        if not self._is_long_polling:
            return
        self._loop.run_until_complete(self._start_long_polling())

    async def _stop(self) -> None:
        """Stop long polling"""
        if not self._is_long_polling:
            return
        self._stop_long_polling = True
        await self.close()
        self._logger.info("Long polling stopped")

    def stop(self) -> None:
        """Stop long polling"""
        self._loop.run_until_complete(self._stop())

    async def close(self) -> None:
        """Close aiohttp session"""
        await self.__session.close()

    def __del__(self) -> None:
        self._loop.run_until_complete(self.close())
