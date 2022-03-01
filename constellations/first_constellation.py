# Note, all measures are in SI units (kg, m, s, etc.)

AU = 149_597_871 * 10 ** 3

constellation = {
    "Sun": {
        "x": 0,
        "y": 0,
        "radius": 696_342_000,
        "init_velocity_x": 0,
        "init_velocity_y": 0,
        "mass": 1.98847 * 10 ** 30,
        "colour": [250, 0, 0],
        "image": "resources/star1.png",
    },
    "Earth": {
        "x": -AU,
        "y": 0,
        "radius": 6_371_000,
        "init_velocity_x": 0,
        "init_velocity_y": 29_800,
        "mass": 5.772 * 10 ** 24,
        "colour": [0, 0, 250],
        "image": "resources/planet1.png",
    },
    "Mars": {
        "x": -249_000_000_000,
        "y": 0,
        "radius": 3_389_500,
        "init_velocity_x": 0,
        "init_velocity_y": 21970,
        "mass": 6.39 * 10 ** 23,
        "colour": [0, 250, 0],
        "image": "resources/planet2.png",
    },
    "Pluto": {
        "x": -7304.326 * 10 ** 9,
        "y": 0,
        "radius": 1_188_300,
        "init_velocity_x": 0,
        "init_velocity_y": 3710,
        "mass": 0.01303 * 10 ** 24,
        "colour": [255, 165, 0],
        "image": "resources/planet3.png",
    },
}


general_parameters = {
    "time_step": 3600 * 5,
    "scale_factor": 10 / AU,
}
