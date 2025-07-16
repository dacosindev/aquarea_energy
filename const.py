"""Constants for the Aquarea Energy integration."""

DOMAIN = "aquarea_energy"

SENSOR_TYPES = {
    "daily_heating": {
        "name": "Daily Heating Energy",
        "unit": "kWh",
        "icon": "mdi:fire",
    },
    "daily_cooling": {
        "name": "Daily Cooling Energy",
        "unit": "kWh",
        "icon": "mdi:snowflake",
    },
    "daily_tanking": {
        "name": "Daily Tank Energy",
        "unit": "kWh",
        "icon": "mdi:water",
    },
}
