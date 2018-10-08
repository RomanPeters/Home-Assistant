"""
Slowly turn on the lights
"""
light = "light.standing_lamp"

brightness = 0
while hass.states.get("sensor.button") == "long":
    time.sleep(1)
    brightness += 1
    hass.services.call("light", "turn_on", service_data={"entity_id": light, "brightness_pct": brightness})
    if brightness == 100:
        break
