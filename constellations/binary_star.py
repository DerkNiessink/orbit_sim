AU = 149_597_871 * 10 ** 3
mass_sun = 1.98847 * 10 ** 30
radius_sun = 696_342_000

constellation = {
    "Star 1": {
        "init_position": (0, 0, 0),
        "init_velocity": (0, - 50000, 25000),
        "radius": 1.711 * radius_sun,
        "mass": 4 * mass_sun,
        "tail_length": 3000,
        "image": "resources/star1.png",
    },
    "Star 2": {
        "init_position": (2 * AU, 0 , 0),
        "init_velocity": (0, 0, 0),
        "radius": 1.711 * radius_sun,
        "mass": 3 * mass_sun,
        "tail_length": 3000,
        "image": "resources/star1.png",
    },
       "Planet 1": {
        "init_position": (-3 * AU, 0 , 0),
        "init_velocity": (0, 0, -10000),
        "radius": 1.711 * radius_sun,
        "mass": 0.000001 * mass_sun,
        "tail_length": 1000,
        "image": "resources/planet1.png",
    },
        "Planet 2": {
        "init_position": (2.5 * AU, 0 , 0),
        "init_velocity": (0, 0, -70000),
        "radius": 1.711 * radius_sun,
        "mass": 0.000001 * mass_sun,
        "tail_length": 100,
        "image": "resources/planet1.png",
    },
}


general_parameters = {
    "time_step": 3600 * 0.5,
    "scale_factor": 10 / AU,
}
