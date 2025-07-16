"""Config flow for the Aquarea Energy integration."""

from homeassistant import config_entries

from .const import DOMAIN  # Asegúrate de tener DOMAIN = "tu_dominio"



import voluptuous as vol

class AquareaEnergyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow para la integración Aquarea Energy."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            # Aquí podrías validar el usuario/contraseña si lo deseas
            return self.async_create_entry(title="Aquarea Energy", data=user_input)

        data_schema = vol.Schema({
            vol.Required("username"): str,
            vol.Required("password"): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
