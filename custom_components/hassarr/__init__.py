import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType
from homeassistant.config_entries import ConfigEntry
import homeassistant.helpers.config_validation as cv
from .services import handle_add_media
from .const import DOMAIN, SERVICE_ADD_MOVIE, SERVICE_ADD_TV_SHOW

ADD_MOVIE_SCHEMA = vol.Schema({
    vol.Required("title"): cv.string,
})

ADD_TV_SHOW_SCHEMA = vol.Schema({
    vol.Required("title"): cv.string,
})

def handle_add_movie(hass: HomeAssistant, call: ServiceCall) -> None:
    """Handle the service action to add a movie to Radarr.

    Args:
        hass (HomeAssistant): The Home Assistant instance.
        call (ServiceCall): The service call object.
    """
    handle_add_media(hass, call, "movie", "radarr")

def handle_add_tv_show(hass: HomeAssistant, call: ServiceCall) -> None:
    """Handle the service action to add a TV show to Sonarr.

    Args:
        hass (HomeAssistant): The Home Assistant instance.
        call (ServiceCall): The service call object.
    """
    handle_add_media(hass, call, "series", "sonarr")

def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Hassarr integration.

    Args:
        hass (HomeAssistant): The Home Assistant instance.
        config (ConfigType): The configuration dictionary.

    Returns:
        bool: True if setup was successful, False otherwise.
    """
    hass.services.register(DOMAIN, SERVICE_ADD_MOVIE, lambda call: handle_add_movie(hass, call), schema=ADD_MOVIE_SCHEMA)
    hass.services.register(DOMAIN, SERVICE_ADD_TV_SHOW, lambda call: handle_add_tv_show(hass, call), schema=ADD_TV_SHOW_SCHEMA)

    # Return boolean to indicate that initialization was successful.
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Hassarr from a config entry.

    Args:
        hass (HomeAssistant): The Home Assistant instance.
        config_entry (ConfigEntry): The configuration entry.

    Returns:
        bool: True if setup was successful, False otherwise.
    """
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN] = config_entry.data

    # Register services
    hass.services.async_register(DOMAIN, SERVICE_ADD_MOVIE, lambda call: handle_add_movie(hass, call), schema=ADD_MOVIE_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_ADD_TV_SHOW, lambda call: handle_add_tv_show(hass, call), schema=ADD_TV_SHOW_SCHEMA)

    return True