"""
Wake up sounds
"""
sound = hass.states.get("input_select.alarm_clock_light").lower()

if sound == "tv":
    hass.services.call("switch", "turn_on", service_data={"entity_id": "switch.television"})
    for i in range(0, 50):
        hass.services.call("script", "turn_on", service_data={"entity_id": "script.sony_volume_lower"})
    for i in range(0, 50):
        time.sleep(5)
        hass.services.call("script", "turn_on", service_data={"entity_id": "script.sony_volume_higher"})
