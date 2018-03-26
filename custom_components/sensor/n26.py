"""
Support for N26.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.n26/
"""
from datetime import timedelta
import logging

import voluptuous as vol
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_USERNAME, CONF_PASSWORD, CONF_CARD_ID)
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['n26==0.1.3']

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_FORCED_UPDATES = timedelta(seconds=5)
MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=15)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_CARD_ID): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the N26 sensor."""
    name = config.get(CONF_NAME)
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    card_id = config.get(CONF_CARD_ID)

    if not name:
        name = "N26 Balance"

    add_devices(N26Sensor(name, username, password, card_id))


class N26Sensor(Entity):
    """Implementation of a N26 sensor."""

    def __init__(self, name, username, password, card_id):
        """Initialize the sensor."""
        from n26 import config, api
        self._name = name
        self._username = username
        self._password = password
        self._card_id = card_id
        self._state = None
        self._unit_of_measurement = 'Euro'
        self._conf = config.Config(username, password, card_id)
        self._conn = api.Api(self._conf)

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
            ATTR_ATTRIBUTION: CONF_ATTRIBUTION,
        }

    def update(self):
        """Get the latest state of the sensor."""        
        self._state = self.conn.get_balance()['availableBalance']
