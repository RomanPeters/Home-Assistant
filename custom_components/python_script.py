"""
Customized component to allow running unrestricted Python scripts.

"""
import datetime
import glob
import logging
import os
import time

import voluptuous as vol

from homeassistant.const import SERVICE_RELOAD
from homeassistant.exceptions import HomeAssistantError
from homeassistant.loader import bind_hass
from homeassistant.util import sanitize_filename
import homeassistant.util.dt as dt_util

REQUIREMENTS = []

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'python_script'

FOLDER = 'python_scripts'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema(dict)
}, extra=vol.ALLOW_EXTRA)


class ScriptError(HomeAssistantError):
    """When a script error occurs."""

    pass


def setup(hass, config):
    """Initialize the Python script component."""
    path = hass.config.path(FOLDER)

    if not os.path.isdir(path):
        _LOGGER.warning("Folder %s not found in configuration folder", FOLDER)
        return False

    discover_scripts(hass)

    def reload_scripts_handler(call):
        """Handle reload service calls."""
        discover_scripts(hass)
    hass.services.register(DOMAIN, SERVICE_RELOAD, reload_scripts_handler)

    return True


def discover_scripts(hass):
    """Discover python scripts in folder."""
    path = hass.config.path(FOLDER)

    if not os.path.isdir(path):
        _LOGGER.warning("Folder %s not found in configuration folder", FOLDER)
        return False

    def python_script_service_handler(call):
        """Handle python script service calls."""
        execute_script(hass, call.service, call.data)

    existing = hass.services.services.get(DOMAIN, {}).keys()
    for existing_service in existing:
        if existing_service == SERVICE_RELOAD:
            continue
        hass.services.remove(DOMAIN, existing_service)

    for fil in glob.iglob(os.path.join(path, '*.py')):
        name = os.path.splitext(os.path.basename(fil))[0]
        hass.services.register(DOMAIN, name, python_script_service_handler)


@bind_hass
def execute_script(hass, name, data=None):
    """Execute a script."""
    filename = '{}.py'.format(name)
    with open(hass.config.path(FOLDER, sanitize_filename(filename))) as fil:
        source = fil.read()
    execute(hass, filename, source, data)


@bind_hass
def execute(hass, filename, source, data=None):
    """Execute Python source."""
    logger = logging.getLogger('{}.{}'.format(__name__, filename))
    try:
        _LOGGER.info("Executing %s: %s", filename, data)
        # pylint: disable=exec-used
        exec(source)
    except Exception as err:  # pylint: disable=broad-except
        logger.exception("Error executing script: %s", err)


