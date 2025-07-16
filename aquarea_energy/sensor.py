"""Integration for Panasonic Aquarea Energy."""

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SENSOR_TYPES


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities,
) -> None:
    """Set up the Aquarea sensors from config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    sensors = [AquareaEnergySensor(coordinator, key) for key in SENSOR_TYPES]

    async_add_entities(sensors, update_before_add=True)


class AquareaEnergySensor(CoordinatorEntity, SensorEntity):
    """Representation of an Aquarea energy sensor."""

    def __init__(self, coordinator, sensor_type) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_name = "aquarea_energy_" + SENSOR_TYPES[sensor_type]["name"]
        self._attr_icon = SENSOR_TYPES[sensor_type]["icon"]
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type]["unit"]
        self._attr_unique_id = f"aquarea_energy_{sensor_type}"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    @property
    def native_value(self) -> float:
        """Return the state of the sensor."""
        data = self.coordinator.data or {}
        return data.get(self._sensor_type)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "aquarea_device")},
            "name": "Panasonic Aquarea",
            "manufacturer": "Panasonic",
            "model": "Aquarea",
            "entry_type": "service",
        }
