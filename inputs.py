VERTICAL = (0.3, 0.3, 0.15, 0.15, 0.1)
HORIZONTAL = (0.15, 0.15, 0.3, 0.3, 0.1)
LAZY = (0.15, 0.15, 0.15, 0.15, 0.4)
UP_LEANING = (0.4, 0.15, 0.15, 0.15, 0.15)
DOWN_LEANING = (0.15, 0.4, 0.15, 0.15, 0.15)
LEFT_LEANING = (0.15, 0.15, 0.4, 0.15, 0.15)
RIGHT_LEANING = (0.15, 0.15, 0.15, 0.4, 0.15)

small_inputs = [

    {
        "map": [['P', 'P', 'P', 'P', 'P'],
                ['P', 'I', 'P', 'P', 'P'],
                ['P', 'P', 'I', 'P', 'P'],
                ['P', 'P', 'P', 'I', 'P'], ],
        "drones": {'drone 1': (3, 0), },
        "packages": {'package 1': (3, 4),
                     'package 2': (3, 4)},
        "clients": {'Alice': {"location": (0, 0),
                              "packages": ('package 1',),
                              "probabilities": VERTICAL},
                    'Bob': {"location": (2, 0),
                            "packages": ('package 2',),
                            "probabilities": HORIZONTAL}
                    },
        "turns to go": 200
    },

    {
        "map": [['P', 'P', 'P', 'P', 'P'],
                ['P', 'I', 'P', 'P', 'P'],
                ['P', 'P', 'I', 'P', 'P'],
                ['P', 'P', 'P', 'I', 'P'],
                ['P', 'P', 'P', 'P', 'P'],
                ['P', 'P', 'P', 'I', 'P'], ],
        "drones": {'drone 1': (3, 0),
                   'drone 2': (2, 4)},
        "packages": {'package 1': (5, 4),
                     'package 2': (5, 4),
                     'package 3': (5, 4),
                     'package 4': (5, 4),
                     'package 5': (5, 4)},
        "clients": {'Alice': {"location": (0, 0),
                              "packages": ('package 1', 'package 2'),
                              "probabilities": RIGHT_LEANING},
                    'Bob': {"location": (2, 3),
                            "packages": ('package 3', 'package 4'),
                            "probabilities": LAZY},
                    'Charlie': {"location": (5, 1),
                                "packages": ('package 5',),
                                "probabilities": VERTICAL},
                    },
        "turns to go": 350
    },
]