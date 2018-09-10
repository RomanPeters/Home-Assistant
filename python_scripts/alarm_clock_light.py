"""
Slowly turn on the lights
"""
light_type = hass.states.get("input_select.alarm_clock_light").lower()
lights = []

if "bed led" in lights:
    lights.append("light.blinkt")
if "standing lamp" in lights:
    lights.append("light.standing_lamp")
if "ceiling lamp" in lights:
    lights.append("light.ceiling_lamp")



if lights:
    for light in lights:
        hass.services.call("light", "turn_on", service_data={"entity_id": light, "brightness_pct": 5, "color": "white"})


    time.sleep(300)  # 5 min
    for light in lights:
        hass.services.call("light", "turn_on", service_data={"entity_id": light, "brightness_pct": 10})


    time.sleep(300)  # 10 min
    for light in lights:
        hass.services.call("light", "turn_on", service_data={"entity_id": light, "brightness_pct": 20})


    time.sleep(300)  # 15 min
    for light in lights:
        hass.services.call("light", "turn_on", service_data={"entity_id": light, "brightness_pct": 40})


    time.sleep(300)  # 20 min
    for light in lights:
        hass.services.call("light", "turn_on", service_data={"entity_id": light, "brightness_pct": 60})


    time.sleep(300)  # 25 min
    for light in lights:
        hass.services.call("light", "turn_on", service_data={"entity_id": light, "brightness_pct": 80})


    time.sleep(300)  # 30 min
    for light in lights:
        hass.services.call("light", "turn_on", service_data={"entity_id": light, "brightness_pct": 100})

