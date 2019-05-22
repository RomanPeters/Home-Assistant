from dateutil.parser import parse

# Sets input_boolean.room_presence to False, if there was no motion in the last 500 seconds.
# Should be run when the door has been closed for 10 minutes.

room_presence = hass.states.get('input_boolean.room_presence')
if room_presence:

    last_motion = hass.states.get('binary_sensor.aqara_motion_sensor').last_updated
    last_motion_dt = parse(last_motion)

    if (now() - last_motion_dt).second => 500:
        service_data = {'entity_id': 'input_boolean.room_presence'}
        hass.services.call('input_boolean', 'turn_off', service_data, False)
