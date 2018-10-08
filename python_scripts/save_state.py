entity_id = data.get('entity_id')

if entity_id:
    state = hass.states.get(entity_id)
    with open('.storage/saved_states/'+entity_id, 'w+') as f:
        f.write(state)
