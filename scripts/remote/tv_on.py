import time

if hass.states.get("switch.b") != "on":
    hass.services.call("switch.turn_on", service_data={"entity_id": "switch.b"})
    time.sleep(30)  # wait for tv to turn on
