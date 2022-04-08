AU = 149_597_871 * 10 ** 3
mass_earth = 5.772 * 10 ** 24
radius_earth = 6_371_000

constellation = {
    "Sun": {
        "init_position": (0, 0, 0),
        "init_velocity": (0, 0, 0),
        "radius": 696_342_000,
        "mass": 1.98847 * 10 ** 30,
        "type": "star",
    },
    "Mercury": {
        "init_position": (-69_818_000_000, 0, 0),
        "init_velocity": (0, 38_860, 0),
        "radius": 2_479_000,
        "mass": 0.33010 * 10 ** 24,
        "type": "terrestrial hot",
    },
    "Earth": {
        "init_position": (-AU, 0, 0),
        "init_velocity": (0, 29_800, 0),
        "radius": radius_earth,
        "mass": mass_earth,
        "type": "terrestrial oceanic",
    },
    "Mars": {
        "init_position": (-249_000_000_000, 0, 0),
        "init_velocity": (0, 21970, 0),
        "radius": 3_389_500,
        "mass": 6.39 * 10 ** 23,
        "type": "terrestrial dry",
    },
    "Jupiter": {
        "init_position": (-5.367 * AU, 0, 0),
        "init_velocity": (0, 12440, 0),
        "radius": 71_492_000,
        "mass": 1.898 * 10 ** 24,
        "type": "gas giant",
    },
    "Pluto": {
        "aphelion": -48.023 * AU,
        "min_orbital_velocity": 3710,
        "inclination": 17.16, 
        "radius": 0.186 * radius_earth,
        "mass": 0.0022 * mass_earth,
        "type": "terrestrial dry",
    },
    "Venus": {
        "init_position": (-0.716 * AU, 0, 0),
        "init_velocity": (0, 34790, 0),
        "radius": 6051.8 * 10 ** 3,
        "mass": 4.8673 * 10 ** 24,
        "type": "terrestrial hot",
    },
    "Saturn": {
        "init_position": (-9.905 * AU, 0, 0),
        "init_velocity": (0, 9090, 0),
        "radius": 60_268_000,
        "mass": 568.32 * 10 ** 24,
        "type": "gas giant",
    },
    "Uranus": {
        "init_position": (-19.733 * AU, 0, 0),
        "init_velocity": (0, 6490, 0),
        "radius": 25_559_000,
        "mass": 86.811 * 10 ** 24,
        "type": "terrestrial dry",
    },
    "Neptune": {
        "init_position": (-29.973 * AU, 0, 0),
        "init_velocity": (0, 5370, 0),
        "radius": 24_764_000,
        "mass": 102.409 * 10 ** 24,
        "type": "terrestrial dry",
    },
    "Moon": {
        "init_position": (-AU - 0.4055 * 10 ** 9, 0, 0),
        "init_velocity": (0, 970 + 29_800, 0),
        "radius": 1_736_000,
        "mass": 0.07346 * 10 ** 24,
        "type": "moon",
        "tail_length": 45,
    },
}


general_parameters = {
    "time_step": 1800,
    "scale_factor": 10 / AU,
}
