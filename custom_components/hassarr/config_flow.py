from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN

class HassarrConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=self._get_schema())

        # Validate user input
        errors = {}
        if not user_input.get("radarr_url") or not user_input.get("radarr_api_key") or not user_input.get("radarr_quality_profile_name"):
            errors["base"] = "missing_radarr_info"
        if not user_input.get("sonarr_url") or not user_input.get("sonarr_api_key") or not user_input.get("sonarr_quality_profile_name"):
            errors["base"] = "missing_sonarr_info"

        if errors:
            return self.async_show_form(step_id="user", data_schema=self._get_schema(), errors=errors)

        # Create the entry
        return self.async_create_entry(title="Hassarr", data=user_input)

    @staticmethod
    def _get_schema():
        return vol.Schema({
            vol.Required("radarr_url"): str,
            vol.Required("radarr_api_key"): str,
            vol.Required("radarr_quality_profile_name"): str,
            vol.Required("sonarr_url"): str,
            vol.Required("sonarr_api_key"): str,
            vol.Required("sonarr_quality_profile_name"): str
        })