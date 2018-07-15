"""
  input_boolean:
    night_mode:
      name: Sleeping
      initial: off
"""

import appdaemon.plugins.hass.hassapi as hass

class Sleeping(hass.Hass):
    def initialize(self):
        self.listen_state(self.lights_turned_off, "group.all_lights", new = "off")

    def lights_turned_off(self, *args, **kwargs):
        self.turn_on("input_boolean.night_mode")


class Waking(hass.Hass):
    def initialize(self):
        self.listen_state(self.motion_detected, "binary_sensor.motion_sensor", new = "on")

    def motion_detected(self):
        if self.get_state("binary_sensor.dark") == "off":
            self.turn_off("input_boolean.night_mode")
