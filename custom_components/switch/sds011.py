"""Sleep/wake support for SDS011."""
import logging

from homeassistant.components.switch import SwitchDevice, PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME

import voluptuous as vol
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['pyserial']

DEFAULT_NAME = 'sds011'
CONF_SERIAL_DEVICE = 'serial_device'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_SERIAL_DEVICE): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the SDS011 platform."""
    # pylint: disable=import-error, no-member
    import serial
    
    name = config.get(CONF_NAME)

    ser = serial.Serial()
    ser.port = config.get(CONF_SERIAL_DEVICE)
    ser.baudrate = 9600
    ser.open()
    ser.flushInput()

    if config.get(CONF_NAME) is not None:
        name = config.get(CONF_NAME)
    else:
        name = 'sds011'

    add_devices([
        SDS011(name, ser)
    ])




class SDS011(SwitchDevice):
    """Representation of a SDS011."""

    def __init__(self, name, ser):
        """Initialize the SDS011."""
        self._name = name
        self.serial = ser
        self._state = True
        SwitchDevice.__init__(self)

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def is_on(self):
        """Return true if it is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Turn the switch on."""    
        if self.serial.write(self.construct_command(6, [0x1, 0]).encode()):
            self.read_response()
            self._state = True
            self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        if self.serial.write(self.construct_command(6, [0x1, 0]).encode()):
            self.read_response()
            self._state = False
            self.schedule_update_ha_state()

  
    def construct_command(self, cmd, data=[]):
        """Taken from https://raw.githubusercontent.com/zefanja/aqi/master/python/aqi.py"""
        assert len(data) <= 12
        data += [0,]*(12-len(data))
        checksum = (sum(data)+cmd-2)%256
        ret = "\xaa\xb4" + chr(cmd)
        ret += ''.join(chr(x) for x in data)
        ret += "\xff\xff" + chr(checksum) + "\xab"
        return ret

    def dump(self, d, prefix=''):
        print(prefix + ' '.join(x.encode('hex') for x in d))

    def read_response(self):
        byte = 0
        while byte != "\xaa":
            byte = self.serial.read(size=1)

        d = self.serial.read(size=9)


        self.dump(d, '< ')
        return byte + d
