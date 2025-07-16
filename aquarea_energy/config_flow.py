"""Config flow for the Aquarea Energy integration."""

from homeassistant import config_entries

from .const import DOMAIN  # Asegúrate de tener DOMAIN = "tu_dominio"


class TuDominioConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow sin formulario para tu integración."""

    VERSION = 1  # Versión del esquema de entrada (útil para migraciones futuras)

    async def async_step_user(self, user_input=None):
        """Paso inicial, sin pedir datos."""
        # Evita duplicados: si ya existe una entrada, no creamos otra
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        return self.async_create_entry(title="Aquarea Energy", data={})
