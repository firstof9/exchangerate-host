"""Sensor platform for integration_blueprint."""
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity

from .const import CONF_CONVERT, CONF_CURRENCY, CONF_NAME, DOMAIN, ICON
from .entity import ExchangeRateHostEntity

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([ExchangeRateHostSensor(coordinator, entry)])


class ExchangeRateHostSensor(ExchangeRateHostEntity, SensorEntity):
    """ExchangeRateHost Sensor class."""

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"{self._name}_{self.currency}"

    @property
    def native_value(self) -> float:
        """Return the native value of the sensor."""
        return self.coordinator.data.get("rates")[self.convert]

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return self.convert

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return ICON
