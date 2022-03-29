# Note, all measures are in SI units (kg, m, s, etc.)


AU = 149_597_871 * 10 ** 3

constellation = {
    "Sun": {
        "init_position": (0, 0, 0),
        "init_velocity": (0, 0, 0),
        "radius": 696_342_000,
        "mass": 1.98847 * 10 ** 30,
        "image": "resources/star1.png",
    },
    "Mercury": {
        "init_position": (-69_818_000_000, 0, 0),
        "init_velocity": (0, 38_860, 0),
        "radius": 2_479_000,
        "mass": 0.33010 * 10 ** 24,
        "image": "resources/mercury.jpg",
    },
    "Earth": {
        "init_position": (-AU, 0, 0),
        "init_velocity": (0, 29_800, 0),
        "radius": 6_371_000,
        "mass": 5.772 * 10 ** 24,
        "image": "resources/planet1.png",
    },
    "Mars": {
        "init_position": (-249_000_000_000, 0, 0),
        "init_velocity": (0, 21970, 0),
        "radius": 3_389_500,
        "mass": 6.39 * 10 ** 23,
        "image": "resources/planet2.png",
    },
    "Jupiter": {
        "init_position": (-5.367 * AU, 0, 0),
        "init_velocity": (0, 12440, 0),
        "radius": 71_492_000,
        "mass": 1.898 * 10 ** 24,
        "image": "resources/planet4.png",
    },
    "Pluto": {
        "init_position": (-7304.326 * 10 ** 9, 0, 0),
        "init_velocity": (0, 3710, 0),
        "radius": 1_188_300,
        "mass": 0.01303 * 10 ** 24,
        "image": "resources/planet3.png",
    },
    "Venus": {
        "init_position": (-0.716 * AU, 0, 0),
        "init_velocity": (0, 34790, 0),
        "radius": 6051.8 * 10 ** 3,
        "mass": 4.8673 * 10 ** 24,
        "image": "resources/planet3.png",
    },
    "Saturn": {
        "init_position": (-9.905 * AU, 0, 0),
        "init_velocity": (0, 9090, 0),
        "radius": 60_268_000,
        "mass": 568.32 * 10 ** 24,
        "image": "resources/planet3.png",
    },
    "Uranus": {
        "init_position": (-19.733 * AU, 0, 0),
        "init_velocity": (0, 6490, 0),
        "radius": 25_559_000,
        "mass": 86.811 * 10 ** 24,
        "image": "resources/planet3.png",
    },
    "Neptune": {
        "init_position": (-29.973 * AU, 0, 0),
        "init_velocity": (0, 5370, 0),
        "radius": 24_764_000,
        "mass": 102.409 * 10 ** 24,
        "image": "resources/planet3.png",
    },
    "Moon": {
        "init_position": (-AU - 0.4055 * 10 ** 9, 0, 0),
        "init_velocity": (0, 970 + 29_800, 0),
        "radius": 1_736_000,
        "mass": 0.07346 * 10 ** 24,
        "image": "resources/moon1.png",
        "tail_length": 45,
    },
}


general_parameters = {
    "time_step": 1800,
    "scale_factor": 10 / AU,
}
