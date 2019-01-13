from dateutil.parser import parse

LAMP = data.get('entity_id') if data.get('entity_id') else 		"light.aqara_white_bulb"
TEMPERATURE = data.get('temperature') if data.get('temperature') else 	370
MAX_BRIGHTNESS = data.get('brightness') if data.get('brightness') else 	160
DURATION = data.get('duration') if data.get('duration') else  		900


increment = DURATION / MAX_BRIGHTNESS

sunset = parse(hass.states.get('sun.sun').attributes["next_setting"])
sunset_ts = sunset.timestamp()

seconds_from_start = DURATION - int(sunset_ts - time.time())
if seconds_from_start < 0:
    seconds_from_start = 0
    logger.warning(f"Script called before sunset interval, adjusted to {DURATION} seconds")

brightness = seconds_from_start // increment + 1
if brightness < 1:
    brightness = 1

hass.services.call('light', 'turn_on', {'entity_id': LAMP,
                                        'color_temp': TEMPERATURE,
                                        'brightness': brightness}, False)

time.sleep(increment)

# Further increasing
while brightness <= MAX_BRIGHTNESS and hass.states.get(LAMP).state == "on":
    brightness += 1
    hass.services.call('light', 'turn_on', {'entity_id': LAMP,
                                            'brightness': brightness}, False)
    time.sleep(increment)
