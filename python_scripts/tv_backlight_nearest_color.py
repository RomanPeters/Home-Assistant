
possible_colors = {}
possible_colors["script.tv_backlight_w"] =  (255,   255,   255)

possible_colors["script.tv_backlight_r"] =  (255, 0,   0)
possible_colors["script.tv_backlight_g"] =  (0,   255, 0)
possible_colors["script.tv_backlight_b"] =  (0,   0,   255)

possible_colors["script.tv_backlight_r1"] = (255, 127, 0)
possible_colors["script.tv_backlight_g1"] = (0,   255, 127)
possible_colors["script.tv_backlight_b1"] = (0,   127, 255)

possible_colors["script.tv_backlight_r2"] = (255, 191, 0)
possible_colors["script.tv_backlight_g2"] = (0,   255, 191)
possible_colors["script.tv_backlight_b2"] = (63, 0, 255)

possible_colors["script.tv_backlight_r3"] = (255, 191, 0)
possible_colors["script.tv_backlight_g3"] = (0, 255, 191)
possible_colors["script.tv_backlight_b3"] = (191, 0, 255)

possible_colors["script.tv_backlight_r4"] = (255, 255, 0)
possible_colors["script.tv_backlight_g4"] = (0, 255, 255)
possible_colors["script.tv_backlight_b4"] = (255, 0, 255)




RGB = data["rgb_color"]
options = possible_colors

RGB_tuple = tuple(int(i) for i in RGB.strip('()').split(','))
R = RGB_tuple[0]
G = RGB_tuple[1]
B = RGB_tuple[2]
mindiff = None
for d in options.keys():
    r, g, b = options[d]
    diff = abs(R -r)*256 + abs(G-g)* 256 + abs(B- b)* 256
    if mindiff is None or diff < mindiff:
        mindiff = diff
        mincolorname = d

script = mincolorname

hass.services.call('script', 'turn_on', {'entity_id': script}, False)

