"""
Used for voice broadcasts over the speakers.
"""

if hass.states.get("input_boolean.home") and not hass.states.get("input_boolean.night_mode"):  # only when home and awake
   
    if hass.states.get("switch.speakers") == "off":
        hass.services.call("switch.turn_on", service_data={"entity_id": "switch.speakers"})
        time.sleep(2) # wait for speakers

    hass.services.call("switch.tts.google_say",
                       service_data={"entity_id": "media_player.apple_tv",
                                     "message": data.get("message")})

    
