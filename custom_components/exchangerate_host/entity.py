"""BlueprintEntity class"""
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTRIBUTION,
    CONF_CONVERT,
    CONF_CURRENCY,
    CONF_NAME,
    DOMAIN,
    NAME,
    VERSION,
)


class ExchangeRateHostEntity(CoordinatorEntity):
    """ExchangeRateHost entity class."""

    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.currency = config_entry.data.get(CONF_CURRENCY)
        self._name = config_entry.data.get(CONF_NAME)
        self.convert = config_entry.data.get(CONF_CONVERT)

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": NAME,
            "model": VERSION,
            "manufacturer": NAME,
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "integration": DOMAIN,
            "conversion": f"{self.currency} -> {self.convert}",
        }
