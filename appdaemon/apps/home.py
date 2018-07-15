import os
import time
import datetime
import appdaemon.plugins.hass.hassapi as hass

def has_changed(entity, minutes):
    """ Check if entity has changed last x minutes """
    last_changed_str = entity.last_changed
    last_changed = datetime.datetime.strptime(last_changed_str, '%Y-%m-%dT%H:%M:%S.%f+00:00') + datetime.timedelta(hours=2)
    start_moment = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
    if last_changed > start_moment:
        return True


class Home(hass.Hass):
    """
    input_boolean:
      home:
        name: Presence Detected
        initial: off
    """
    def initialize(self):
        laptop_ip = "10.10.10.1"
        if os.system("ping -c 1 " + laptop_ip) == 0:
            self.turn_on("input_boolean.home")

        self.listen_state(self.door_open, "binary_sensor.door", new = "on")
        self.listen_state(self.door_close, "binary_sensor.door", new = "off")

    def door_open(self):
        """ Someone opened the door, so someone is there """
        self.log("door opened!")
        self.turn_on("input_boolean.home")

    def door_close(self):
        """ Someone closed the door, is he leaving or arriving? """
        self.log("door closed!")
        minutes = 15  # minutes to monitor for activity
        time.sleep(60*minutes)

        # motion detected -> home
        if self.has_changed(self.entities.binary_sensor.motion_sensor, minutes-3):
            self.log("There was motion")
            self.turn_on("input_boolean.home")
            return

        # button activity -> home
        if self.has_changed(self.entities.sensor.wall_switch, minutes) or self.has_changed(self.entities.sensor.button, minutes):
            self.log("There was button pressing")
            self.turn_on("input_boolean.home")
            return

        # no activity -> away
        self.log("No activity detected")
        self.turn_off("input_boolean.home")
