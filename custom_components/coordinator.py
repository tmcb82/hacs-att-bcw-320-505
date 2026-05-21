import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .api import BGW320Client
from .const import DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

class BGW320DataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, client: BGW320Client):
        self.client = client
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )

    async def _async_update_data(self):
        try:
            return await self.client.fetch_data()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")