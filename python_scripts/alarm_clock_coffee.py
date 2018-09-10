"""
Make sure the coffee is ready when the alarm goes off
"""
enabled = True if hass.states.get("input_boolean.alarm_coffee") == "on" else False

if enabled:
    coffee_time = 8*60
    transition_time = 30*60
    time.sleep(transition_time - coffee_time)
    hass.services.call("switch", "turn_on", service_data={"entity_id": "switch.coffee_maker"})
    hass.services.call("input_boolean", "turn_off", service_data={"entity_id": "input_boolean.alarm_coffee"})
