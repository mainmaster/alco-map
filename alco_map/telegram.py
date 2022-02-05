from facet import ServiceMixin
from siotelegram import HTTPxTelegramApi

from alco_map.database import Database
from alco_map.common import alco_map_backoff


class Telegram(ServiceMixin):

    def __init__(self, token: str, database: Database):
        self.token = token
        self.db = database
        self.api = None

    @property
    def dependencies(self):
        return [
            self.db,
        ]

    async def start(self):
        self.api = HTTPxTelegramApi(self.token)
        self.add_task(self._background())

    async def stop(self):
        await self.api.close()

    async def _background(self):
        while True:
            await self.process_updates()

    @alco_map_backoff(inteval=1, max_time=300)
    async def process_updates(self):
        updates = await self.api.get_updates()
        for update in updates["result"]:
            message = update["message"]
            location = message.get("location")
            if not location:
                continue

            stores = await self.db.get_nearest_stores(
                latitude=location["latitude"],
                longitude=location["longitude"],
            )
            if not stores:
                continue

            store_location = stores[0].get_location()
            await self.api.send_message(
                chat_id=message["chat"]["id"],
                latitude=store_location["latitude"],
                longitude=store_location["longitude"],
            )
