from dateutil.parser import parse

automations = hass.states.get('group.all_automations').attributes['entity_id']


last_dt = None
last_entity_id = None

for entity_id in automations[1:]:
    entity = hass.states.get(entity_id)
    triggered_dt = entity.attributes['last_triggered']
    if triggered_dt:

        if not last_dt:
            last_dt = triggered_dt
            last_entity_id = entity_id
        elif triggered_dt > last_dt:
            last_dt = triggered_dt
            last_entity_id = entity_id

hass.states.set(entity_id='sensor.last_triggered_automation', new_state=last_entity_id)
