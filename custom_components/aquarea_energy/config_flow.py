import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN  # Asegúrate de tener 'DOMAIN = "aquarea_energy"' en const.py

DATA_SCHEMA = vol.Schema(
    {
        vol.Required("username"): str,
        vol.Required("password"): str,
    }
)


class AquareaEnergyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Aquarea Energy."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}

        if user_input is not None:
            # Aquí podrías validar credenciales si quieres
            return self.async_create_entry(
                title=user_input["username"], data=user_input
            )

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return AquareaEnergyOptionsFlowHandler(config_entry)


class AquareaEnergyOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Aquarea Energy."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return self.async_show_form(step_id="init", data_schema=vol.Schema({}))
