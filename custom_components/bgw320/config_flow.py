import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, CONF_HOST, DEFAULT_HOST
from .api import BGW320Client

class BGW320ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_HOST])
            self._abort_if_unique_id_configured()

            session = async_get_clientsession(self.hass)
            client = BGW320Client(user_input[CONF_HOST], session)

            if await client.test_connection():
                return self.async_create_entry(
                    title=f"AT&T BGW320-505 ({user_input[CONF_HOST]})",
                    data=user_input
                )
            errors["base"] = "cannot_connect"

        data_schema = vol.Schema({
            vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )
