"""Integration for Panasonic Aquarea Energy."""

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .aioaquarea import AquareaEnvironment, Client
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Aquarea Energy from a config entry."""

    session = async_get_clientsession(hass)
    username = entry.data.get("username")
    password = entry.data.get("password")
    client = Client(
        username=username,
        password=password,
        session=session,
        device_direct=True,
        refresh_login=True,
        environment=AquareaEnvironment.PRODUCTION,
    )

    try:
        devices = await client.get_devices()
        device_info = devices[0]

        device = await client.get_device(
            device_info=device_info,
            consumption_refresh_interval=timedelta(minutes=1),
        )
    except Exception as err:
        raise ConfigEntryNotReady(f"Error initializing Aquarea: {err}")

    async def async_fetch_energy_data():
        try:
            return await device.get_total_consumption_day()
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="aquarea_energy",
        update_method=async_fetch_energy_data,
        update_interval=timedelta(hours=1),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, [Platform.SENSOR])

    return True
