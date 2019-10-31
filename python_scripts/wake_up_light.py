from dateutil.parser import parse

LAMP = data.get('entity_id') if data.get('entity_id') else 		"light.aqara_white_bulb"
TEMPERATURE = data.get('temperature') if data.get('temperature') else 	154
MAX_BRIGHTNESS = data.get('brightness') if data.get('brightness') else 	255

alarm_clock_ts = parse(hass.states.get('input_datetime.alarm_clock').state).timestamp()
duration = alarm_clock_ts - time.time()
if duration < 1:
    duration += 86400

elif duration > 3600:
    logger.warning(f"Alarm clock light adjusted to 1 hour (was {duration//60} minutes)")
    duration = 3600

increment = duration / MAX_BRIGHTNESS

if hass.states.get('input_boolean.alarm_clock').state == 'on':
    # Initial call
    brightness = 1
    hass.services.call('light', 'turn_on', {'entity_id': LAMP,
                                            'color_temp': TEMPERATURE,
                                            'brightness': brightness}, False)

    time.sleep(increment)

    # Further increasing
    while brightness <= MAX_BRIGHTNESS and hass.states.get('input_boolean.alarm_clock').state == 'on' and hass.states.get(LAMP).state == "on":
        brightness += 1
        hass.services.call('light', 'turn_on', {'entity_id': LAMP,
                                                'brightness': brightness}, False)
        time.sleep(increment)
