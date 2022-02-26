AU = 149_597_871 * 10 ** 3


constellation = {
    "body1": {
        "x": -AU,
        "y": 0,
        "init_velocity_x": 0,
        "init_velocity_y": 29800,
        "mass": 5.772 * 10 ** 24,
        "colour": [0, 0, 250],
        "image": "resources/planet1.png",
    },
    "body2": {
        "x": 0,
        "y": 0,
        "init_velocity_x": 0,
        "init_velocity_y": 0,
        "mass": 1.98847 * 10 ** 30,
        "colour": [250, 0, 0],
        "image": "resources/star1.png",
    },
    "body3": {
        "x": -249_000_000_000,
        "y": 0,
        "init_velocity_x": 0,
        "init_velocity_y": 21970,
        "mass": 6.39 * 10 ** 23,
        "colour": [0, 250, 0],
        "image": "resources/planet2.png",
    },
}


general_parameters = {
    "time_step": 3600 * 24,
    "scale_factor": 250 / AU,
}
