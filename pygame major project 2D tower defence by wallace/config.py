"""Static configuration values for the tower defence game.

This module initialises Pygame and exposes dictionaries that describe
initial game constants, level presets and tower presets.  All other
modules import from here so that these values remain centralised.
"""

import pygame

pygame.init()
pygame.mixer.init()
pygame.mixer.fadeout(1)


# store data used in all files
Initialise = {
    # screen, icon and title
    "screen_size" : (940, 540),
    "screen" : pygame.display.set_mode((940,540), pygame.RESIZABLE),
    "icon" : 'pygame major project 2D tower defence by wallace/assets/game-icon.png',
    "title" : "Maths defence",

    # convert to make it load more quickly, alpha allows image transparency
    "enemy_snakeIMG" : pygame.transform.scale_by(pygame.image.load('pygame major project 2D tower defence by wallace/assets/enemy_snakeIMG.png').convert_alpha(), 1.3),
    "enemy_ant_gIMG" : pygame.transform.scale_by(pygame.image.load('pygame major project 2D tower defence by wallace/assets/enemy_ant_gIMG.png').convert_alpha(), 1.3),
    "enemy_ant_sIMG" : pygame.transform.scale_by(pygame.image.load('pygame major project 2D tower defence by wallace/assets/enemy_ant_sIMG.png').convert_alpha(), 1.3),

    "attack_linearIMG" : pygame.transform.scale_by(pygame.image.load('pygame major project 2D tower defence by wallace/assets/attack_linearIMG.png').convert_alpha(), 0.7),
    "attack_parabolaIMG" : pygame.transform.scale_by(pygame.image.load('pygame major project 2D tower defence by wallace/assets/attack_parabolaIMG.png').convert_alpha(), 1),
    "tower_linearIMG" : pygame.transform.scale_by(pygame.image.load('pygame major project 2D tower defence by wallace/assets/tower_linearIMG.png').convert_alpha(), 0.8),
    "tower_parabolaIMG" : pygame.transform.scale_by(pygame.image.load('pygame major project 2D tower defence by wallace/assets/tower_parabolaIMG.png').convert_alpha(), 0.8),
    "queryIMG" : pygame.image.load('pygame major project 2D tower defence by wallace/assets/query.png').convert_alpha(),
    "button_pauseIMG": pygame.image.load('pygame major project 2D tower defence by wallace/assets/button_pauseIMG.png').convert_alpha(),
    "button_homeIMG": pygame.image.load('pygame major project 2D tower defence by wallace/assets/button_homeIMG.png').convert_alpha(),
    "Dialogue_badend": pygame.image.load('pygame major project 2D tower defence by wallace/assets/Dialogue_badend.png').convert_alpha(),
    "Dialogue_happyend": pygame.image.load('pygame major project 2D tower defence by wallace/assets/Dialogue_happyend.png').convert_alpha(),

    # text font initialise
    # consider importing settings to a list that fit into pygame.font.SysFont() -> usually [text family: str, size: int, blod: bool, i]
    "enemy_health_font" : ["cambria", 25, False, False],
    "player_font" : ["cambria", 20, True, False],

    # audio initialise
    "badendSOUND": pygame.mixer.Sound("pygame major project 2D tower defence by wallace/audio/badendSOUND.mp3"),
    "happyendSOUND": pygame.mixer.Sound("pygame major project 2D tower defence by wallace/audio/happyendSOUND.mp3"),
    "pauseSOUND":  pygame.mixer.Sound("pygame major project 2D tower defence by wallace/audio/pauseSOUND.mp3"),
    "unpauseSOUND":  pygame.mixer.Sound("pygame major project 2D tower defence by wallace/audio/unpauseSOUND.mp3"),
    "homeSOUND":  pygame.mixer.Sound("pygame major project 2D tower defence by wallace/audio/homeSOUND.mp3"),


    # frames per second
    "fps" : 30
}

Level_preset = {
    # home screen
    "home": { # button_data with rectangles of [85 + 285k, 70 + 235m, 200, 200 ]  -- > k and m are integers 
              # k represents the column number, m the row number
        # button to: tutorial, level1, level2,/n level3, level4, level5
        "button_data" : [
            [pygame.image.load('pygame major project 2D tower defence by wallace/assets/button_tutorialIMG.png').convert_alpha(), [85, 70]],
            [pygame.image.load('pygame major project 2D tower defence by wallace/assets/button_lv1IMG.png').convert_alpha(), [375, 70]],
            [pygame.image.load('pygame major project 2D tower defence by wallace/assets/button_lv2IMG.png').convert_alpha(), [655, 70]],
            [pygame.image.load('pygame major project 2D tower defence by wallace/assets/button_lv3IMG.png').convert_alpha(), [85, 305]],
            [pygame.image.load('pygame major project 2D tower defence by wallace/assets/button_lv4IMG.png').convert_alpha(), [375, 305]],
            [pygame.image.load('pygame major project 2D tower defence by wallace/assets/button_lv5IMG.png').convert_alpha(), [655, 305]],
        ],
        "music": "pygame major project 2D tower defence by wallace/audio/HomeMUSIC.mp3",
    },

    # tutorial
    "tutorial": {
        "enemy_data": {
            "snake": {
                "health": 100,
                # distance in pixels
                "distance_per_second": 100,
                "image": Initialise["enemy_snakeIMG"],
                "spawn_time": {1,7.4, 8.1, 8.9, 9.5, 10.0, 10.4, 10.9, 11.3, 11.9, 17.6, 18.2, 18.8, 19.3, 19.7, 20.0, 20.4, 20.8, 21.3, 21.8},
                "bounty": 20
            },
        },
        # (0,0) is not a valid checkpoint
        "checkpoints": [(0, 270), (740, 270)],
        "player_health": 100,
        "player_currency": 100,
        # pause, home
        "button_data": [[Initialise["button_pauseIMG"],[840,0]],[Initialise["button_homeIMG"],[890,0]]],
        # badend, happyend, other dialogues with a time 
        "dialogue_data": [[Initialise["Dialogue_badend"],[90,55]],[Initialise["Dialogue_happyend"],[90,55]]],
        # UI, battlefield
        "rect_data":[[735, 0 , 200, 540],[0, 0 , 735, 540]],
        # for every shop item [tower_image, name: str, description: str, price: int, unlocked:bool, price:int]
        "shop_data": [["Linear tower", True]],
        "enemy_count": 20,
        "background": pygame.image.load('pygame major project 2D tower defence by wallace/assets/TutorialIMG.png'),
        "music": "pygame major project 2D tower defence by wallace/audio/TutorialMUSIC.mp3"
        },

    # 1
    "level1": {
        "enemy_data": {
            "snake": {
                "health": 120,
                # distance in pixels
                "distance_per_second": 100,
                "image": Initialise["enemy_snakeIMG"],
                "spawn_time": {
                                # Group 1 (center 5, 3 numbers)
                                1.00, 1.85, 4.45,
                                
                                # Group 2 (center 10, 6 numbers)
                                8.25, 8.55, 9.85, 10.15, 10.45, 12.75,
                                
                                # Group 3 (center 15, 8 numbers)
                                13.95, 14.25, 14.55, 15.85, 16.15, 16.45, 17.75, 18.05,
                                
                                # Group 4 (center 20, 13 numbers)
                                19.65, 19.95, 20.00, 20.55, 20.85, 21.00, 21.15, 22.45, 23.75, 24.05, 25.35, 26.65, 27.95
                                },
                "bounty": 20
            },
        },
        # (0,0) is not a valid checkpoint
        "checkpoints": [(0, 1), (260, 180), (120, 300), (300, 400), (530, 230), (710, 350), (570, 470), (700, 570)],
        "player_health": 100,
        "player_currency": 100,
        # pause, home
        "button_data": [[Initialise["button_pauseIMG"],[840,0]],[Initialise["button_homeIMG"],[890,0]]],
        # badend, happyend
        "dialogue_data": [[Initialise["Dialogue_badend"],[90,55]],[Initialise["Dialogue_happyend"],[90,55]]],
        # UI, battlefield
        "rect_data":[[735, 0 , 200, 540],[0, 0 , 735, 540]],
        # for every shop item [tower_image, name: str, description: str, price: int, unlocked:bool, price:int]
        "shop_data": [["Linear tower", True]],
        "enemy_count": 30,
        "background": pygame.image.load('pygame major project 2D tower defence by wallace/assets/Lv1IMG.png'),
        "music": "pygame major project 2D tower defence by wallace/audio/Lv1MUSIC.mp3"
        },

    # 2
    "level2": {
        "enemy_data": {
            "snake": {
                "health": 150,
                # distance in pixels
                "distance_per_second": 100,
                "image": Initialise["enemy_snakeIMG"],
                "spawn_time": {8, 9, 10 , 11, 11.5, 19.5, 21, 21.5, 22, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40},
                "bounty": 20
            },

            "ant_s": {
                "health": 125,
                # distance in pixels
                "distance_per_second": 125,
                "image": Initialise["enemy_ant_sIMG"],
                "spawn_time": {1, 3, 9, 10, 11, 20, 22, 23, 25, 27, 29, 30, 33, 35, 36, 36, 37, 38, 39, 40}, 
                "bounty": 10
            }
        },
        # (0,0) is not a valid checkpoint
        "checkpoints": [(-10, 412), (75, 458), (432, 273), (761, 458)],
        "player_health": 100,
        "player_currency": 170,
        # pause, home
        "button_data": [[Initialise["button_pauseIMG"],[840,0]],[Initialise["button_homeIMG"],[890,0]]],
        # badend, happyend
        "dialogue_data": [[Initialise["Dialogue_badend"],[90,55]],[Initialise["Dialogue_happyend"],[90,55]]],
        # UI, battlefield
        "rect_data":[[735, 0 , 200, 540],[0, 0 , 735, 540]],
        # for every shop item [tower_image, name: str, description: str, price: int, unlocked:bool, price:int]
        "shop_data": [["Linear tower", True]],
        "enemy_count": 40,
        "background": pygame.image.load('pygame major project 2D tower defence by wallace/assets/Lv2IMG.png'),
        "music": "pygame major project 2D tower defence by wallace/audio/Lv2MUSIC.mp3",
        },

    # 3
    "level3": {
        "enemy_data": {
            "ant_g": {
                "health": 60,
                # distance in pixels
                "distance_per_second": 200,
                "image": Initialise["enemy_ant_gIMG"],
                "spawn_time": {1, 5, 6, 19, 13, 16, 33, 34, 36, 37, 38, 39, 40},
                "bounty": 30
            },
            "ant_s": {
                "health": 150,
                # distance in pixels
                "distance_per_second": 150,
                "image": Initialise["enemy_ant_sIMG"],
                "spawn_time": {23, 26, 27.1, 27.3, 27.5, 27.6, 27.9, 28.0, 28.1, 28.2, 28.4, 28.5, 28.6, 28.9, 29.1, 38.2, 38.3, 38.5, 38.6, 38.8, 38.9, 39.0, 39.1, 39.3, 39.4, 39.6, 39.8},
                "bounty": 15
            }
        },
        # (0,0) is not a valid checkpoint
        "checkpoints": [(19, 32), (440, 412), (645, 201), (498, 79), (153, 398), (302, 536)],
        "player_health": 100,
        "player_currency": 95,
        # pause, home
        "button_data": [[Initialise["button_pauseIMG"],[840,0]],[Initialise["button_homeIMG"],[890,0]]],
        # badend, happyend
        "dialogue_data": [[Initialise["Dialogue_badend"],[90,55]],[Initialise["Dialogue_happyend"],[90,55]]],
        # UI, battlefield
        "rect_data":[[735, 0 , 200, 540],[0, 0 , 735, 540]],
        # for every shop item [tower_image, name: str, description: str, price: int, unlocked:bool, price:int]
        "shop_data": [["Linear tower", True], ["Parabola tower", True]],
        "enemy_count": 40,
        "background": pygame.image.load('pygame major project 2D tower defence by wallace/assets/Lv3IMG.png'),
        "music": "pygame major project 2D tower defence by wallace/audio/Lv3MUSIC.mp3",
        },

    # 4
    "level4": {
        "enemy_data": {
            "snake": {
                "health": 200,
                # distance in pixels
                "distance_per_second": 100,
                "image": Initialise["enemy_snakeIMG"],
                "spawn_time": {17, 19, 20, 21, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58},
                "bounty": 20
            },
            "ant_g": {
                "health": 100,
                # distance in pixels
                "distance_per_second": 200,
                "image": Initialise["enemy_ant_gIMG"],
                "spawn_time": {1, 5, 6, 13, 14, 16, 33, 34, 36, 37, 48, 50, 52},
                "bounty": 15
            },
            "ant_s": {
                "health": 150,
                # distance in pixels
                "distance_per_second": 150,
                "image": Initialise["enemy_ant_sIMG"],
                "spawn_time": {18, 19, 20, 21, 22, 23, 32, 33, 34, 35, 36, 37, 48, 49, 50, 51, 52, 53, 54, 55}, # (tuple([x/100 for x in range(1000)])),
                "bounty": 10
            }
        },
        # (0,0) is not a valid checkpoint
        "checkpoints": [(0, 1), (282, 279), (400, 187), (744, 550)],
        "player_health": 100,
        "player_currency": 150,
        # pause, home
        "button_data": [[Initialise["button_pauseIMG"],[840,0]],[Initialise["button_homeIMG"],[890,0]]],
        # badend, happyend
        "dialogue_data": [[Initialise["Dialogue_badend"],[90,55]],[Initialise["Dialogue_happyend"],[90,55]]],
        # UI, battlefield
        "rect_data":[[735, 0 , 200, 540],[0, 0 , 735, 540]],
        # for every shop item [tower_image, name: str, description: str, price: int, unlocked:bool, price:int]
        "shop_data": [["Linear tower", True], ["Parabola tower", True]],
        "enemy_count": 60,
        "background": pygame.image.load('pygame major project 2D tower defence by wallace/assets/Lv4IMG.png'),
        "music": "pygame major project 2D tower defence by wallace/audio/Lv4MUSIC.mp3",
        },
}

Tower_preset = {
    "Linear tower": {
        "dps": 30,
        "description" : "penetrative!",
        "details" : ["This tower shoots a straight line nothing can stop, dealing damage to enemies on", "its path. This is also how linear graphs looks like - also a straight line, extending to", "infinity. The equation would be y = Ax or Ay = x"],
        "price": 100,
        "image" : Initialise["tower_linearIMG"],
        "range" : 200,
    },
    "Parabola tower": {
        "dps": 30,
        "description" : "Knocks back!",
        "details" : ["This tower shoots a growing curve knocking back enemies. This is also how parabola", " graphs looks like - also a curve curving at a linear rate. The equation would be y = Ax^2", " or Ay^2 = x, where ^2 means to the power of two. Be aware that you will only learn", " about parabolas facing verticly and horizontally in high school."],
        "price" : 50,
        "image" : Initialise["tower_parabolaIMG"],
    "range" : 230,
    }
}
