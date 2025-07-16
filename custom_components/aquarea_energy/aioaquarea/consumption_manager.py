from __future__ import annotations
import logging
from typing import TYPE_CHECKING

from .const import AQUAREA_SERVICE_A2W_STATUS_DISPLAY, AQUAREA_SERVICE_CONSUMPTION
from .statistics import Consumption, DateType  # Import from statistics
from .auth import PanasonicRequestHeader

if TYPE_CHECKING:
    from .api_client import AquareaAPIClient

_LOGGER = logging.getLogger(__name__)


class AquareaConsumptionManager:
    """Handles consumption data retrieval."""

    def __init__(self, api_client: AquareaAPIClient, base_url: str):
        self._api_client = api_client
        self._base_url = base_url

    async def get_device_consumption(
        self, device_id: str, aggregation: DateType, date_input: str
    ) -> Consumption:
        """Get device consumption."""
        payload = {
            "apiName": f"/remote/v1/api/consumption",
            "requestMethod": "POST",
            "bodyParam": {
                "gwid": device_id,
                "dataMode": int(aggregation.value),
                "date": date_input,
                "osTimezone": "+02:00",
            },
        }
        response = await self._api_client.request(  # Changed to _api_client.request
            "POST",  # Method is POST for the transfer API
            url="remote/v1/app/common/transfer",  # Specific URL for transfer API
            json=payload,  # Pass payload as json
            throw_on_error=True,
        )
        date_data = await response.json()

        return Consumption(date_data.get("historyDataList"))

    async def get_device_total_consumption(
        self, device_id: str, aggregation: DateType, date_input: str
    ) -> dict:
        """Get device consumption."""
        total_consumption = {}

        payload = {
            "apiName": "/remote/v1/api/consumption",
            "requestMethod": "POST",
            "bodyParam": {
                "gwid": device_id,
                "dataMode": int(aggregation.value),
                "date": date_input,
                "osTimezone": "+02:00",
            },
        }

        # Log para comprobar el estado de la sesión HTTP
        if hasattr(self._api_client, "session"):
            session = self._api_client.session
            _LOGGER.debug(
                "[AquareaConsumptionManager] session is %s (closed=%s)",
                session,
                getattr(session, "closed", "unknown"),
            )
        else:
            _LOGGER.debug(
                "[AquareaConsumptionManager] api_client has no 'session' attribute"
            )

        try:
            response = await self._api_client.request(
                "POST",
                url="remote/v1/app/common/transfer",
                json=payload,
                throw_on_error=True,
            )
        except Exception as exc:
            _LOGGER.error(
                "[AquareaConsumptionManager] Exception during request: %s", exc
            )
            raise

        # Log después de la petición
        if hasattr(self._api_client, "session"):
            session = self._api_client.session
            _LOGGER.debug(
                "[AquareaConsumptionManager] session after request is %s (closed=%s)",
                session,
                getattr(session, "closed", "unknown"),
            )

        date_data = await response.json()
        history_list = date_data.get("historyDataList")

        cool_consumption = 0.0
        heat_consumption = 0.0
        tank_consumption = 0.0
        temperature_list = []

        for item in history_list:
            cool_consumption += item.get("coolConsumption", 0.0)
            heat_consumption += item.get("heatConsumption", 0.0)
            tank_consumption += item.get("tankConsumption", 0.0)
            temperature_list.append(item.get("outdoorTemp", 0))

        total_consumption["daily_cooling"] = cool_consumption
        total_consumption["daily_heating"] = heat_consumption
        total_consumption["daily_tanking"] = tank_consumption
        # total_consumption["daily_temperature"] = temperature_list

        return total_consumption
