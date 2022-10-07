"""Constants for ExchangeRate.host."""
# Base component constants
NAME = "ExchangeRate.host"
DOMAIN = "exchangerate_host"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"
ATTRIBUTION = "Data provided by ExchangeRate.host"
ISSUE_URL = "https://github.com/firstof9/exchangerate-host/issues"
BASE_URL = "https://api.exchangerate.host/"
TIMEOUT = 10

# Icons
ICON = "mdi:swap-horizontal"

# Platforms
PLATFORMS = ["sensor"]

# Configuration and options
CONF_NAME = "name"
CONF_CONVERT = "convert"
CONF_CURRENCY = "currency"
CONF_INTERVAL = "interval"

# Defaults
DEFAULT_NAME = DOMAIN
DEFAULT_INTERVAL = 43200


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
