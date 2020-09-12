import movements

states={
    "pokestop":{
        "area": 0.027,
        "area_err": 0.01,
        "bounds": [(104, 207, 227), (107, 233, 255)] 
    },
    "pokestop_success":{
        "area":  0.10810366666666667,
        "area_err": 0.005,
        "bounds": [(111, 104, 125), (152, 255, 255)] 
    },
    "catch":{
        "area": 0.005432432432432433,
        "area_err": 0.001,
        "bounds": [(33, 40, 51), (53, 71, 219)] 
    },
    "pokemon_caught":{
        "area": 0.013936936936936936,
        "area_err": 0.001,
        "bounds": [(52, 80, 204), (83, 217, 255)]
    },
    "map":{
        "area": 0.000023273273,
        "area_err": 0.00001,
        "bounds": [(94, 240, 219), (179, 255, 255)]
    }
}

state_functions = {
    "pokestop": {
        "function": movements.spinStop,
        "next_states": ["pokestop", "map"],
        "wait": 2
    },
    "map": {
        "function": movements.mapAction,
        "next_states": ["pokestop", "map", "catch"],
        "wait": 3
    },
    "catch": {
        "function": movements.throwPokeball,
        "next_states": ["catch", "pokemon_caught", "map"],
        "wait": 2
    },
    "pokemon_caught":{
        "function": movements.exitCaughtPokemon,
        "next_states": ["map"],
        "wait": 2
    }
}


filters = {
    "day":{
        "roads": [(0, 81, 115), (89, 227, 182)],
        "road_lines": [(21, 97, 0), (51, 145, 255)],
        "light_ground": [(49, 42, 0), (69, 255, 255)],
        "forest": [(0, 255, 0), (87, 255, 255)],
        # "white_lines_and_ui": [(0, 0, 255), (179, 41, 255)],
        "lakes": [(92, 234, 199), (96, 255, 212)],
        # "radar": [(46, 16, 208), (68, 103, 249)]
    },
    "night":{
        "roads": [(41, 151, 108), (110, 188, 180)],
        "road_lines": [(30, 36, 139), (93, 101, 255)],
        "light_ground": [(66, 60, 0), (111, 156, 255)],
        "forest": [(96, 214, 88), (99, 255, 154)],
        "white_lines_and_ui": [(109, 0, 0), (137, 94, 205)],
    },
    "pokestop": [(85, 181, 207), (179, 255, 255)]
}

play_area = (480, 300, 700, 450)

screen_size = (3000, 2000)
img_size = (1500, 1000)
img_crop = (510, 0, 1060, 1000) #x1, y1, x2, y2

limits = {
    "boxes":{
        "pokemon": {
            "min_area": 0,
            "max_area": 0,
            "min_widht": 0,
            "max_width": 0,
            "min_height": 0,
            "max_height": 0,
        },
        "pokestop": {
            "min_area": 0,
            "max_area": 0,
            "min_widht": 0,
            "max_width": 0,
            "min_height": 0,
            "max_height": 0,
        },
    }
}