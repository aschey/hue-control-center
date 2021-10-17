from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant


async def async_setup(hass: HomeAssistant, config: ConfigEntry):
    hass.states.async_set("hello_state.world", "test")

    # Return boolean to indicate that initialization was successful.
    return True
