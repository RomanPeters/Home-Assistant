"""
Support for N26.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.n26/
"""
import logging
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_USERNAME, CONF_PASSWORD, CONF_NAME, CONF_CURRENCY)
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['n26==0.1.3']

_LOGGER = logging.getLogger(__name__)

ATTR_ID = 'ID'
ATTR_AVAILABLE_BALANCE = 'Available Balance'
ATTR_USABLE_BALANCE = 'Usable Balance'
ATTR_BANK_BALANCE = 'Bank Balance'
ATTR_IBAN = 'IBAN'
ATTR_BIC = 'BIC'
ATTR_BANK_NAME = 'Bank Name'
ATTR_SEIZED = 'Seized'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_CURRENCY): cv.string,
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the N26 sensor."""
    from n26 import config as n26config
    from n26 import api as n26api

    name = config.get(CONF_NAME)
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    currency = config.get(CONF_CURRENCY)

    if not name:
        name = "N26"
    if not currency:
        currency = "EUR"  # At the moment N26 only offers EUR currency anyway


    add_devices([
        N26Sensor(name, username, password, currency, n26config, n26api)
    ])


class N26Sensor(Entity):
    """Implementation of a N26 sensor."""

    def __init__(self, name, username, password, currency, n26config, n26api):
        """Initialize the sensor."""
        self._name = name
        self._username = username
        self._password = password
        self._config = n26config
        self._api = n26api
        self._conf = self._config.Config(username=username, password=password, card_id=None)  # card_id not necessary for sensor
        self._conn = self._api.Api(self._conf)
        self._unit_of_measurement = currency  # Couldn't find an API call to retrieve currency type
        self._state = None
        self._id = None
        self._available_balance = None
        self._usable_balance = None
        self._bank_balance = None
        self._iban = None
        self._bic = None
        self._bank_name = None
        self._seized = None


    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement this sensor expresses itself in."""
        return self._unit_of_measurement

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        return {
            ATTR_ID: self._id,
            ATTR_AVAILABLE_BALANCE: self._available_balance,
            ATTR_USABLE_BALANCE: self._usable_balance,
            ATTR_BANK_BALANCE: self._bank_balance,
            ATTR_IBAN: self._iban,
            ATTR_BIC: self._bic,
            ATTR_BANK_NAME: self._bank_name,
            ATTR_SEIZED: self._seized,
        }

    def update(self):
        """Get the latest state of the sensor."""
        self._conn = self._api.Api(self._conf)
        account = self._conn.get_balance()
        self._state = '{:0,.2f}'.format(account['availableBalance'])
        self._id = account['id']
        self._available_balance = str(account['availableBalance'])
        self._usable_balance = str(account['usableBalance'])
        self._bank_balance = str(account['bankBalance'])
        self._iban = account['iban']
        self._bic = account['bic']
        self._bank_name = account['bankName']
        self._seized = str(account['seized'])
