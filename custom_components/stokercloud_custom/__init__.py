"""The StokerCloud Custom integration."""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_USERNAME, API_URL, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up StokerCloud Custom from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    coordinator = StokerCloudDataUpdateCoordinator(hass, entry)
    
    await coordinator.async_config_entry_first_refresh()
    
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


class StokerCloudDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching StokerCloud data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        """Initialize."""
        self.username = entry.data[CONF_USERNAME]
        self.session = async_get_clientsession(hass)
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        url = API_URL.format(username=self.username)
        
        try:
            async with self.session.get(url, timeout=10) as response:
                if response.status != 200:
                    raise UpdateFailed(f"Error communicating with API: {response.status}")
                
                data = await response.json()
                
                if "jsondata" not in data:
                    raise UpdateFailed("Invalid data received from API")
                
                return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
