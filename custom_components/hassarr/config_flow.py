import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN

class HassarrConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("integration_type"): vol.In(["Radarr & Sonarr", "Overseerr"])
                })
            )

        self.integration_type = user_input["integration_type"]
        if self.integration_type == "Radarr & Sonarr":
            return await self.async_step_radarr_sonarr()
        else:
            return await self.async_step_overseerr()

    async def async_step_radarr_sonarr(self, user_input=None):
        if user_input is None:
            return self.async_show_form(step_id="radarr_sonarr", data_schema=self._get_radarr_sonarr_schema())

        # Validate user input
        errors = {}
        if not user_input.get("radarr_url") or not user_input.get("radarr_api_key") or not user_input.get("radarr_quality_profile_name"):
            errors["base"] = "missing_radarr_info"
        if not user_input.get("sonarr_url") or not user_input.get("sonarr_api_key") or not user_input.get("sonarr_quality_profile_name"):
            errors["base"] = "missing_sonarr_info"

        if errors:
            return self.async_show_form(step_id="radarr_sonarr", data_schema=self._get_radarr_sonarr_schema(), errors=errors)

        # Create the entry
        return self.async_create_entry(title="Hassarr", data=user_input)

    async def async_step_overseerr(self, user_input=None):
        if user_input is None:
            return self.async_show_form(step_id="overseerr", data_schema=self._get_overseerr_schema())

        # Validate user input
        errors = {}
        if not user_input.get("overseerr_url") or not user_input.get("overseerr_api_key"):
            errors["base"] = "missing_overseerr_info"

        if errors:
            return self.async_show_form(step_id="overseerr", data_schema=self._get_overseerr_schema(), errors=errors)

        # Create the entry
        return self.async_create_entry(title="Hassarr", data=user_input)

    @staticmethod
    def _get_radarr_sonarr_schema():
        return vol.Schema({
            vol.Required("radarr_url"): str,
            vol.Required("radarr_api_key"): str,
            vol.Required("radarr_quality_profile_name"): str,
            vol.Required("sonarr_url"): str,
            vol.Required("sonarr_api_key"): str,
            vol.Required("sonarr_quality_profile_name"): str
        })

    @staticmethod
    def _get_overseerr_schema():
        return vol.Schema({
            vol.Required("overseerr_url"): str,
            vol.Required("overseerr_api_key"): str
        })

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return HassarrOptionsFlowHandler(config_entry)

OPTIONS_SCHEMA_RADARR_SONARR = vol.Schema({
    vol.Required("radarr_url"): str,
    vol.Required("radarr_api_key"): str,
    vol.Required("radarr_quality_profile_name"): str,
    vol.Required("sonarr_url"): str,
    vol.Required("sonarr_api_key"): str,
    vol.Required("sonarr_quality_profile_name"): str
})

OPTIONS_SCHEMA_OVERSEERR = vol.Schema({
    vol.Required("overseerr_url"): str,
    vol.Required("overseerr_api_key"): str
})

class HassarrOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        if "radarr_url" in self.config_entry.options or "radarr_url" in self.config_entry.data:
            schema = OPTIONS_SCHEMA_RADARR_SONARR
        else:
            schema = OPTIONS_SCHEMA_OVERSEERR

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("radarr_url", default=self.config_entry.options.get("radarr_url", self.config_entry.data.get("radarr_url"))): str,
                vol.Required("radarr_api_key", default=self.config_entry.options.get("radarr_api_key", self.config_entry.data.get("radarr_api_key"))): str,
                vol.Required("radarr_quality_profile_name", default=self.config_entry.options.get("radarr_quality_profile_name", self.config_entry.data.get("radarr_quality_profile_name"))): str,
                vol.Required("sonarr_url", default=self.config_entry.options.get("sonarr_url", self.config_entry.data.get("sonarr_url"))): str,
                vol.Required("sonarr_api_key", default=self.config_entry.options.get("sonarr_api_key", self.config_entry.data.get("sonarr_api_key"))): str,
                vol.Required("sonarr_quality_profile_name", default=self.config_entry.options.get("sonarr_quality_profile_name", self.config_entry.data.get("sonarr_quality_profile_name"))): str
            }) if schema == OPTIONS_SCHEMA_RADARR_SONARR else vol.Schema({
                vol.Required("overseerr_url", default=self.config_entry.options.get("overseerr_url", self.config_entry.data.get("overseerr_url"))): str,
                vol.Required("overseerr_api_key", default=self.config_entry.options.get("overseerr_api_key", self.config_entry.data.get("overseerr_api_key"))): str
            })
        )
