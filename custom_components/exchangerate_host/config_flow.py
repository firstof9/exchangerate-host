"""Adds config flow for Blueprint."""
import logging

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_create_clientsession
import voluptuous as vol

from .api import ExchangeRateHostApiClient
from .const import (
    CONF_CONVERT,
    CONF_CURRENCY,
    CONF_INTERVAL,
    CONF_NAME,
    DEFAULT_INTERVAL,
    DEFAULT_NAME,
    DOMAIN,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def _validate_user_input(user_input: dict) -> tuple:
    """Valididate user input from config flow.

    Returns tuple with error messages and modified user_input
    """
    errors = {}

    # validate scan interval
    if user_input[CONF_INTERVAL] < 30:
        errors[CONF_INTERVAL] = "interval_too_low"

    return errors, user_input


async def _get_symbols(hass: HomeAssistant) -> list | None:
    """Returns list of supported currency."""
    session = async_create_clientsession(hass)
    client = ExchangeRateHostApiClient(session=session)
    data = await client.async_get_symbols()
    symbols = {symbol_id: symbol["description"] for symbol_id, symbol in data.items()}

    return symbols


class ExchangeRateHostFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for ExchangeRateHost."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            self._errors, user_input = await _validate_user_input(user_input)
            if len(self._errors) == 0:
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )
            return await self._show_config_form(user_input)

        user_input = {}
        # Provide defaults for form
        user_input[CONF_NAME] = DEFAULT_NAME
        user_input[CONF_CURRENCY] = None
        user_input[CONF_CONVERT] = None
        user_input[CONF_INTERVAL] = DEFAULT_INTERVAL

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Open the options flow dialog."""
        return ExchangeRateHostOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        symbol_list = await _get_symbols(self.hass)
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME, default=user_input[CONF_NAME]): str,
                    vol.Optional(
                        CONF_CURRENCY, default=user_input[CONF_CURRENCY]
                    ): vol.In(symbol_list),
                    vol.Optional(
                        CONF_CONVERT, default=user_input[CONF_CONVERT]
                    ): vol.In(symbol_list),
                    vol.Optional(
                        CONF_INTERVAL, default=user_input[CONF_INTERVAL]
                    ): vol.Coerce(int),
                }
            ),
            errors=self._errors,
        )


class ExchangeRateHostOptionsFlowHandler(config_entries.OptionsFlow):
    """ExchangeRateHost config flow options handler."""

    def __init__(self, config_entry):
        """Initialize ExchangeRateHost options flow."""
        self._errors = {}
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}
        symbol_list = await _get_symbols(self.hass)
        if user_input is not None:
            self._errors, user_input = await _validate_user_input(user_input)
            if len(self._errors) == 0:
                return await self._update_options(user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_NAME, default=self.config_entry.data.get(CONF_NAME)
                    ): str,
                    vol.Optional(
                        CONF_CURRENCY, default=self.config_entry.data.get(CONF_CURRENCY)
                    ): vol.In(symbol_list),
                    vol.Optional(
                        CONF_CONVERT, default=self.config_entry.data.get(CONF_CONVERT)
                    ): vol.In(symbol_list),
                    vol.Optional(
                        CONF_INTERVAL, default=self.config_entry.data.get(CONF_INTERVAL)
                    ): vol.Coerce(int),
                }
            ),
        )

    async def _update_options(self, user_input):
        """Update config entry options."""
        return self.async_create_entry(title="", data=user_input)
