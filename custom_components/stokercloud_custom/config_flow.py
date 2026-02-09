"""Config flow for StokerCloud Custom integration."""
import logging
import voluptuous as vol
import aiohttp

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_USERNAME, API_URL

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, data: dict):
    """Validate the user input allows us to connect."""
    username = data[CONF_USERNAME]
    url = API_URL.format(username=username)
    
    session = async_get_clientsession(hass)
    
    try:
        async with session.get(url, timeout=10) as response:
            if response.status != 200:
                raise ValueError("Cannot connect to StokerCloud API")
            
            json_data = await response.json()
            
            if "jsondata" not in json_data:
                raise ValueError("Invalid response from StokerCloud API")
            
            return {"title": f"StokerCloud ({username})"}
    except Exception as err:
        _LOGGER.error("Error connecting to StokerCloud: %s", err)
        raise


class StokerCloudConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for StokerCloud Custom."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                
                await self.async_set_unique_id(user_input[CONF_USERNAME])
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(title=info["title"], data=user_input)
            except ValueError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        data_schema = vol.Schema(
            {
                vol.Required(CONF_USERNAME): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
