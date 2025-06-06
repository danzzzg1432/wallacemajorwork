"""Entry point and main game loop for the tower defence game.

This module wires together the classes defined throughout the project and
contains the runtime logic for each level.  It is intentionally a little
long as it drives the UI and game state.
"""

# initialising
import pygame
import classes.enemy
import classes.tower
import classes.button
import config
import ingame_level_data
from pygame.math import Vector2
import time


# start pygame
pygame.init()

# initialise icon and title
pygame.display.set_icon(pygame.image.load(config.Initialise["icon"]))
pygame.display.set_caption(config.Initialise["title"])

# get data from config file
screen = config.Initialise["screen"]
fps = config.Initialise["fps"]

# consider importing settings to a list that fit into pygame.font.SysFont() -> usually [text family: str, size: int, blod: bool, i]
player_font = pygame.font.SysFont(config.Initialise["player_font"][0], config.Initialise["player_font"][1], config.Initialise["player_font"][2], config.Initialise["player_font"][3])
player_font = player_font = pygame.font.SysFont(config.Initialise["player_font"][0], config.Initialise["player_font"][1], config.Initialise["player_font"][2], config.Initialise["player_font"][3])
enemy_health_font = pygame.font.SysFont(config.Initialise["enemy_health_font"][0], config.Initialise["enemy_health_font"][1], config.Initialise["enemy_health_font"][2], config.Initialise["enemy_health_font"][3])



# getting data from classes
Enemy = classes.enemy.Enemy
Snake = classes.enemy.Snake
Linear = classes.tower.Linear
Parabola = classes.tower.Parabola
Ant_g = classes.enemy.Ant_g
Ant_s = classes.enemy.Ant_s
Shop_item = classes.button.Shop_item
Button = classes.button.Button
Rect = classes.button.Rect
Dialogue = classes.button.Dialogue


def generate_enemies(level : str):
    """
    prepare Enemy objects to be spawned

    Args:
        level: A string (levelx) representing the level to get the data from, where x is an integer

    Result:
        Enemy objects to be spawned in the level is all in Enemy_prep_list which is stored in ingame_level_data.py,
        sorted according to their spawn time.
    """
    ingame_level_data.Ingame_data["Enemy_prep_list"] = []
    for enemy_type in config.Level_preset[level]["enemy_data"]:
        if enemy_type == "snake":
            for spawn_time in config.Level_preset[level]["enemy_data"]["snake"]["spawn_time"]:
                a = Snake(level, spawn_time)
                ingame_level_data.Ingame_data["Enemy_prep_list"].append(a)
        if enemy_type == "ant_g":
            for spawn_time in config.Level_preset[level]["enemy_data"]["ant_g"]["spawn_time"]:
                a = Ant_g(level, spawn_time)
                ingame_level_data.Ingame_data["Enemy_prep_list"].append(a)
        if enemy_type == "ant_s":
            for spawn_time in config.Level_preset[level]["enemy_data"]["ant_s"]["spawn_time"]:
                a = Ant_s(level, spawn_time)
                ingame_level_data.Ingame_data["Enemy_prep_list"].append(a)
    ingame_level_data.Ingame_data["Enemy_prep_list"].sort(key=find_spawn_time)

def generate_music(level : str):
    """
    start music at beginning of level

    Args:
        level: A string (levelx) representing the level to get the data from, where x is an integer

    Result:
        music being played at 50% max volume
    """
    pygame.mixer.music.unload()
    pygame.mixer.music.load(config.Level_preset[level]["music"])
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0, 2000)

def play_sound(sound: str):
    """
    playe sound effect

    Args:
        sound: A string corresponding to the key in the dictionary config.Initialise

    Result:
        sound effect being played, not pausing previous music
    """
    pygame.mixer.Sound.play(config.Initialise[sound])

def play_sound_pause_music(sound: str):
    """
    playe sound effect and pause music

    Args:
        sound: A string corresponding to the key in the dictionary config.Initialise

    Result:
        sound effect being played, pause previous music
    """
    pygame.mixer.music.pause()
    play_sound(sound)

def pass_level(level: str):
    """
    end the level if player passed the level
    Args:
        level: A string (levelx) representing the level to get the data from, where x is an integer

    """
    # no more enemies to be spawned, all spawned enemies killed --> passed!
    if not ingame_level_data.Ingame_data["Enemy_prep_list"] and not ingame_level_data.Ingame_data["Enemy_list"]:
        ingame_level_data.Ingame_data["Dialogue_list"][1].draw()
        
        show_level = player_font.render(level, True, (255, 255, 255))
        screen.blit(show_level, [i * ingame_level_data.Ingame_data["resize_factor"] for i in [440, 150]])

        show_tower_placed = player_font.render(f"tower placed: {ingame_level_data.Ingame_data["tower_placed"]}", True, (38, 255, 74))
        screen.blit(show_tower_placed, [i * ingame_level_data.Ingame_data["resize_factor"] for i in [180, 240]])

        show_health_remaining = player_font.render(f"health remaining : {int(ingame_level_data.Ingame_data["current_player_health"])}", True, (38, 255, 74))
        screen.blit(show_health_remaining, [i * ingame_level_data.Ingame_data["resize_factor"] for i in [180, 280]])

        pygame.display.update()

        play_sound_pause_music("happyendSOUND")
        time.sleep(0.5)
        global level_selected 
        level_selected = "home"

        not_clicked = True
        while not_clicked:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # quit the loop of this level and game level
                        global running
                        running = False
                        level_selected = False
                        not_clicked = False

                    # Buttons
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        not_clicked = False
                        ingame_level_data.Ingame_data["Enemy_dead_list"].empty()
                        ingame_level_data.Ingame_data["Enemy_list"].empty()
                        ingame_level_data.Ingame_data["Enemy_prep_list"] = []
                        ingame_level_data.Ingame_data["Tower_list"].empty()
                        break

def fail_level():
    """
    end the level if player has failed
    """
    # check if the player have any health left --> should add a death message / screen / score
    if ingame_level_data.Ingame_data["current_player_health"] <= 0:
        ingame_level_data.Ingame_data["Dialogue_list"][0].draw()
        play_sound_pause_music("badendSOUND")
        time.sleep(0.5)
        global level_selected 
        level_selected = "home"
        pygame.display.update()

        not_clicked = True
        while not_clicked:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # quit the loop of this level and game level
                        global running
                        running = False
                        level_selected = False
                        not_clicked = False

                    # Buttons
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        not_clicked = False
                        ingame_level_data.Ingame_data["Enemy_dead_list"].empty()
                        ingame_level_data.Ingame_data["Enemy_list"].empty()
                        ingame_level_data.Ingame_data["Enemy_prep_list"] = []
                        ingame_level_data.Ingame_data["Tower_list"].empty()
                        break

def generate_button(level : str):
    """
    prepares Button class and its objects

    Args:
        level: A string (levelx) representing the level to get the data from, where x is an integer

    Results:
        Button, Rect and Shop_item objects to be stored and resized in lists stored in ingame_level_data.py
    """
    ingame_level_data.Ingame_data["Button_list"] = []
    ingame_level_data.Ingame_data["Shop_item_list"] = []
    ingame_level_data.Ingame_data["Rect_list"] = []
    ingame_level_data.Ingame_data["Dialogue_list"] = []
    
    try:  
        for i in range(0, len(config.Level_preset[level]["button_data"])):
            a = Button(i, level)
            ingame_level_data.Ingame_data["Button_list"].append(a)

    except KeyError:
        # in case there is no button for this level
        pass

    try:  
        for i in range(0, len(config.Level_preset[level]["dialogue_data"])):
            a = Dialogue(i, level)
            ingame_level_data.Ingame_data["Dialogue_list"].append(a)
            
    except KeyError:
        pass

    try: 
        for i in range(0, len(config.Level_preset[level]["rect_data"])):
            a = Rect(i, level)
            ingame_level_data.Ingame_data["Rect_list"].append(a)

    except KeyError:
        pass

    try:
        for i in range(0, len(config.Level_preset[level]["shop_data"])):
            a = Shop_item(i, level)
            ingame_level_data.Ingame_data["Shop_item_list"].append(a)

    except KeyError:
        pass

def find_spawn_time(enemy):
    """
    find how many seconds after the level starts should the enemy spawn.
    Used in generate_enemies function.

    Args:
        enemy: A Enemy class object

    Returns:
        enemy.spawn_time: Spawn time of enemies
    """
# to be used in the function generate_enemies
    return(enemy.spawn_time)

def display_player_data():
    """
    draws player health and currency on the screen 
    
    Args:
        None
    
    Result:
        The data is being drawn on screen with suitable fonts
    """
    # health
    show_health = player_font.render(f"Hp: {round(ingame_level_data.Ingame_data["current_player_health"])}", True, (237, 107, 139))
    # draw it at left bottom corner with a 10px padding
    original_show_health_cords = (740, 3)
    screen.blit(show_health, [i * ingame_level_data.Ingame_data["resize_factor"] for i in original_show_health_cords])

    # currency
    show_currency = player_font.render(f"$    : {(ingame_level_data.Ingame_data["current_player_currency"])}", True, (255, 255, 0))

    original_show_currency_cords = (740, 25)
    screen.blit(show_currency, [i * ingame_level_data.Ingame_data["resize_factor"] for i in original_show_currency_cords])

    # enemy spawned / enemy count
    if ingame_level_data.Ingame_data["enemy_count"] != 0:
        show_remaining_enemy = player_font.render(f"{ingame_level_data.Ingame_data["enemy_count"] - len(ingame_level_data.Ingame_data["Enemy_prep_list"])} / {ingame_level_data.Ingame_data["enemy_count"]}", True, (200, 16, 224))
        original_show_remaining_enemy_cords = (740, 47)
        screen.blit(show_remaining_enemy, [i * ingame_level_data.Ingame_data["resize_factor"] for i in original_show_remaining_enemy_cords])

def path_point_distance_check(location: Vector2, min_distance: float):
    """
    Check distance between the enemy path and a point, so that the towers will not be placed on the path

    Args:
        location: where to place
        min_distance: how far should the tower should be from any path
    
    Returns:
        distance: float
    """
    old_point = None
    #print(ingame_level_data.Ingame_data["checkpoints"]) # error testing
    min_distance *= ingame_level_data.Ingame_data["resize_factor"]
    for i in ingame_level_data.Ingame_data["checkpoints"]:
        i = Vector2(i)

        if old_point:
            # some vector manipulations to find out distance of the 
            path_normalized = pygame.Vector2.normalize(i - old_point)
            # pygame.draw.line(screen, (0,0,233), old_point, i, 3) # error testing
            projection_from_i = pygame.Vector2.dot(path_normalized, i - location) * path_normalized
            projection_from_old_point = pygame.Vector2.dot(path_normalized, old_point - location) * path_normalized
            
            """
             The dot product of two vectors that are parallel but in opposite directions is negative
             prevents checking for locations beyond the path segment           
            """

            if pygame.Vector2.dot(projection_from_i, projection_from_old_point) < 0:
                location_to_vector = projection_from_i - i + location
                magnitude = pygame.Vector2.magnitude(location_to_vector)
                
                if magnitude < min_distance:
                    return False
                
        # a circle near each check point to make up for a gap
        if pygame.Vector2.magnitude(i - location) < min_distance:
            return False

        # set up i as old_point to be used by next i
        old_point = i
        #print(old_point)
        #print("")
    
    # if did not return False
    return True

def revert_resizing_cords(cords):
    """
    revert the resizing process
    by getting a resized coordinate and divide components by resize_factor

    Args:
        cords: Vector2
    
    Return:
        original_cords: the original coordinate ( original when resize factor = 1 ) 
    """
    original_cords = Vector2(cords[0] / ingame_level_data.Ingame_data["resize_factor"], cords[1] / ingame_level_data.Ingame_data["resize_factor"])
    return original_cords

def place_tower(tower_type, level, location: Vector2):
    """
    Place a tower

    Args:
        tower_type: "Linear" or "Parabola"
        level: A string (levelx) representing the level to get the data from, where x is an integer
        location: where to place
    
    Result:
        A tower object from the Tower class is created and added into the Tower_list
    """
    original_location = revert_resizing_cords(location)
    # place tower base at where clicked
    original_location = [original_location[0], original_location[1] - 35]

    if path_point_distance_check(location, 60):
        match tower_type:
            case "Linear":
                tower = Linear(tower_type, level, original_location)
                ingame_level_data.Ingame_data["Tower_list"].add(tower)
            case "Parabola":
                tower = Parabola(tower_type, level, original_location)
                ingame_level_data.Ingame_data["Tower_list"].add(tower)

        tower.resize(ingame_level_data.Ingame_data["resize_factor"])
        ingame_level_data.Ingame_data["tower_placed"] += 1
        ingame_level_data.Ingame_data["held_item"] = None

    else:
        error_list.append([2, "Too close to path."])

def spawn_enemies(current_time: float):
    """
    Spawn prepared enemies

    Args:
        current_time: in seconds
    
    Result:
        A enemy object from the Tower class is moved from the Enemy_prep_list to the Enemy_list
    """
    while 0 < len(ingame_level_data.Ingame_data["Enemy_prep_list"]) and ingame_level_data.Ingame_data["Enemy_prep_list"][0].spawn_time <= current_time:
        ingame_level_data.Ingame_data["Enemy_prep_list"][0].resize(ingame_level_data.Ingame_data["resize_factor"])
        ingame_level_data.Ingame_data["Enemy_list"].add(ingame_level_data.Ingame_data["Enemy_prep_list"][0])
        ingame_level_data.Ingame_data["Enemy_prep_list"].pop(0)

def dialogue_show(current_time: float):
    """
    show a dialogue

    Args:
        current_time: in seconds
    
    Result:
        A dialogue object is drawn
    """
        # check if the player have any health left --> should add a death message / screen / score
    if current_time <= ingame_level_data.Ingame_data["Dialogue_list"][2]:
        ingame_level_data.Ingame_data["Dialogue_list"][2].draw()
        play_sound("pauseSOUND")
        time.sleep(0.5)
        pygame.display.update()

        not_clicked = True
        while not_clicked:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # quit the loop of this level and game level
                        global running
                        running = False
                        global level_selected
                        level_selected = False
                        not_clicked = False

                    # Buttons
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        not_clicked = False
                        ingame_level_data.Ingame_data["Enemy_dead_list"].empty()
                        ingame_level_data.Ingame_data["Enemy_list"].empty()
                        ingame_level_data.Ingame_data["Enemy_prep_list"] = []
                        ingame_level_data.Ingame_data["Tower_list"].empty()
                        break

def resize_factor_get():
    """
    find the factor for everything to be resized to

    Args:
        None
    
    Result:
        resize_factor is calculated in order to keep everything in the screen despite the size change 
    """
    old_width, old_height = config.Initialise["screen_size"]
    new_width, new_height = pygame.display.get_surface().get_size()
    
    # compare whether old or new
    width_factor = new_width / old_width
    height_factor = new_height / old_height

    if width_factor <= height_factor:
        ingame_level_data.Ingame_data["resize_factor"] = width_factor
    else:
        ingame_level_data.Ingame_data["resize_factor"] = height_factor

def error_message():
    """
    draws a alerting message on the screen 
    
    Args:
        None
    
    Result:
        The message is being drawn on screen with suitable fonts
    """
    for i in error_list:
        if i[0] > 0:
            show_error = player_font.render(i[1], True, (255, 0, 0))
            screen.blit(show_error, [i * ingame_level_data.Ingame_data["resize_factor"] for i in [300, 500 - 40 * error_list.index(i)]])
            i[0] -= 1 / fps
        else:
            error_list.remove(i)

def pause_level():
    """
    pause the level indefinately untill the user clicks again 
    
    Args:
        None
    
    Result:
        music paused, pause sound palyed , game paused
        unpause -> unpause sound played, music resumed, game resumed
    """
    pause = True
    message = player_font.render("click again to resume." , True, (255, 255, 255))
    message_rect = message.get_rect()
    message_rect.center = (config.Initialise["screen_size"][0] / 2, config.Initialise["screen_size"][1] / 2)
    pygame.draw.rect(screen, (0,0,0), message_rect)
    screen.blit(message, message_rect)
    play_sound_pause_music("pauseSOUND")
    pygame.display.update()
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pause = False
    play_sound_pause_music("unpauseSOUND")
    pygame.mixer.music.unpause()

def initialise(level):
    """
    initialise level

    Args:
        level: A string (levelx) representing the level to get the data from, where x is an integer

    Results:
        Button, Rect and Shop_item objects to be stored and resized in lists stored in ingame_level_data.py
    """
    ingame_level_data.Ingame_data["current_player_health"] = config.Level_preset[level]["player_health"]
    ingame_level_data.Ingame_data["current_player_currency"] = config.Level_preset[level]["player_currency"]
    generate_enemies(level)
    generate_button(level)
    generate_music(level)

    global background
    background = pygame.transform.scale_by(config.Level_preset[level]["background"], ingame_level_data.Ingame_data["resize_factor"])

    # The enemies spawn relative to when the
    global time_level_init
    time_level_init = pygame.time.get_ticks()/1000

    ingame_level_data.Ingame_data["held_item"] = None

    ingame_level_data.Ingame_data["checkpoints"] = []
    for c in config.Level_preset[level]["checkpoints"]:
        ingame_level_data.Ingame_data["checkpoints"].append((c[0] * ingame_level_data.Ingame_data["resize_factor"], c[1] * ingame_level_data.Ingame_data["resize_factor"]))
    ingame_level_data.Ingame_data["enemy_count"] = config.Level_preset[level]["enemy_count"]

    ingame_level_data.Ingame_data["tower_placed"] = 0


# Game loop
running = True

# where level -1 is the homepage and level 0 will be tutorial, level 1 will be level 1
level_selected = "home"

# stores in format of a list containing duration in seconds and text
# eg. [1, "Don't press that"] 
error_list = []

# initialise time right before the loop begins to avoid the delay from running other codes
clock = pygame.time.Clock()


while running:
    match level_selected:
        case "home":
            # set the buttons
            generate_button(level_selected)
            generate_music(level_selected)
            player_font = pygame.font.SysFont(config.Initialise["player_font"][0], round(config.Initialise["player_font"][1]  * ingame_level_data.Ingame_data["resize_factor"]), config.Initialise["player_font"][2], config.Initialise["player_font"][3])

            while level_selected == "home":
                screen.fill((232, 185, 77))

                # function to exit the game while player pressed X on game window
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # quit the loop of this level and game level
                        running = False
                        level_selected = False

                    # Buttons
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()

                        for i in ingame_level_data.Ingame_data["Button_list"]:
                            if i.check_press(mouse) == True:
                                match ingame_level_data.Ingame_data["Button_list"].index(i):
                                    case 0:
                                        level_selected = "tutorial"
                                    case 1:
                                        level_selected = "level1"
                                    case 2:
                                        level_selected = "level2"
                                    case 3:
                                        level_selected = "level3"
                                    case 4:
                                        level_selected = "level4"
                                    case 5:
                                        level_selected = "endless"
                                break

                    elif event.type == pygame.VIDEORESIZE:
                        resize_factor_get()
                        generate_button(level_selected)
                        player_font = pygame.font.SysFont(config.Initialise["player_font"][0], round(config.Initialise["player_font"][1] * ingame_level_data.Ingame_data["resize_factor"]), config.Initialise["player_font"][2], config.Initialise["player_font"][3])

                if len(ingame_level_data.Ingame_data["Button_list"]) > 0:
                    for button in ingame_level_data.Ingame_data["Button_list"]:
                        button.draw()

                error_message()

                pygame.display.update()
                clock.tick(fps)

        # general case for levels "tutorial", "level1", "level2", "level3", "level4"
        case _:
            initialise(level_selected)
            level_running = level_selected

            # start loop for level
            while level_selected == level_running:
                # insert background image
                screen.fill((30, 10, 0))
                screen.blit(background, (0, 0))

                # display player health
                display_player_data()
                
                error_message()
                ingame_level_data.Ingame_data["Tower_list"].draw(screen)
                for tower in ingame_level_data.Ingame_data["Tower_list"]:
                    tower.aim()

                ingame_level_data.Ingame_data["Attack_list"].draw(screen)
                for attack in ingame_level_data.Ingame_data["Attack_list"]:
                    attack.tick()

                # make every Enemy object do what they are supposed to
                for enemy in ingame_level_data.Ingame_data["Enemy_list"]:
                    enemy.move()
                ingame_level_data.Ingame_data["Enemy_list"].draw(screen)

                for enemy in  ingame_level_data.Ingame_data["Enemy_list"]:
                    enemy.show_health(enemy.health, enemy.location)
                    
                for shop_item in ingame_level_data.Ingame_data["Shop_item_list"]:
                    shop_item.draw()

                for button in ingame_level_data.Ingame_data["Button_list"]:
                    button.draw()

                # check if passed
                pass_level(level_selected)

                # check if have health
                fail_level()
                
                # function to exit the game while player pressed X on game window
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        level_selected = False

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        # print(str(mouse) + ', ') # for testing
                        # pressed on UI
                        if ingame_level_data.Ingame_data["Rect_list"][0].check_press(mouse):

                            if ingame_level_data.Ingame_data["Button_list"][0].check_press(mouse): # pressed on pause button
                                pause_level()
                                break
                                

                            elif ingame_level_data.Ingame_data["Button_list"][1].check_press(mouse): # pressed on home button
                                level_selected = "home"
                                ingame_level_data.Ingame_data["Enemy_dead_list"].empty()
                                ingame_level_data.Ingame_data["Enemy_list"].empty()
                                ingame_level_data.Ingame_data["Enemy_prep_list"] = []
                                ingame_level_data.Ingame_data["Tower_list"].empty()
                                play_sound_pause_music("homeSOUND")
                                break


                            elif ingame_level_data.Ingame_data["held_item"] == None: # pressed shop and has not bought anything yet
                                for i in ingame_level_data.Ingame_data["Shop_item_list"]:
                                    if i.check_press(mouse):
                                        if i.name == "Linear tower":
                                            if ingame_level_data.Ingame_data["current_player_currency"] >= i.price: # enough currency to buy!
                                                ingame_level_data.Ingame_data["current_player_currency"] -= i.price
                                                ingame_level_data.Ingame_data["held_item"] = 1
                                                break
                                            else: error_list.append([2, f"You need {i.price - ingame_level_data.Ingame_data["current_player_currency"]} more to buy the tower."])

                                        elif i.name == "Parabola tower":
                                            if ingame_level_data.Ingame_data["current_player_currency"] >= i.price: # enough currency to buy!
                                                ingame_level_data.Ingame_data["current_player_currency"] -= i.price
                                                ingame_level_data.Ingame_data["held_item"] = 2
                                                break
                                            else: error_list.append([2, f"You need {i.price - ingame_level_data.Ingame_data["current_player_currency"]} more to buy the tower."])
                                            
                                        else:
                                           error_list.append([2, i.name + 'this is not yet implemented'])
                                break

                            else: # clicked on shop UI with a item held -> they should not
                                error_list.append([2, "You are holding a tower! click on the battlefield to place it."]) 
                                break

                        #  pressing on the field
                        elif ingame_level_data.Ingame_data["Rect_list"][1].check_press(mouse): 
                            match ingame_level_data.Ingame_data["held_item"]:
                                case None: # check if pressing on tower
                                    clicked = False
                                    for i in ingame_level_data.Ingame_data["Tower_list"]:
                                        if i.check_press(mouse):
                                            clicked = True
                                            break
                                    if not clicked: # not pressing on any tower
                                        error_list.append([2, "You are not holding or clicking on a tower."])
                                    break

                                case 1:
                                    place_tower("Linear", level_selected, Vector2(pygame.mouse.get_pos()))
                                    break

                                case 2:
                                    place_tower("Parabola", level_selected, Vector2(pygame.mouse.get_pos()))
                                    break
                        
                        else: # clicking out of bounds
                            error_list.append([2, "Here is out of bounds!"])


                    elif event.type == pygame.VIDEORESIZE:
                        resize_factor_get()
                        generate_button(level_selected)
                        player_font = pygame.font.SysFont(config.Initialise["player_font"][0], round(config.Initialise["player_font"][1] * ingame_level_data.Ingame_data["resize_factor"]), config.Initialise["player_font"][2], config.Initialise["player_font"][3])
                        player_font = player_font = pygame.font.SysFont(config.Initialise["player_font"][0], round(config.Initialise["player_font"][1]  * ingame_level_data.Ingame_data["resize_factor"]), config.Initialise["player_font"][2], config.Initialise["player_font"][3])
                        ingame_level_data.Ingame_data["checkpoints"] = []
                        for c in config.Level_preset[level_selected]["checkpoints"]:
                            ingame_level_data.Ingame_data["checkpoints"].append((c[0] * ingame_level_data.Ingame_data["resize_factor"], c[1] * ingame_level_data.Ingame_data["resize_factor"]))
                        for i in ingame_level_data.Ingame_data["Enemy_list"]:
                            i.resize(ingame_level_data.Ingame_data["resize_factor"])
                        for j in ingame_level_data.Ingame_data["Tower_list"]:
                            j.resize(ingame_level_data.Ingame_data["resize_factor"])
                        for k in ingame_level_data.Ingame_data["Attack_list"]:
                            k.resize(ingame_level_data.Ingame_data["resize_factor"])

                        background = pygame.transform.scale_by(config.Level_preset[level_selected]["background"], ingame_level_data.Ingame_data["resize_factor"])

                # get time passed in the level in seconds
                current_time = pygame.time.get_ticks() / 1000 - time_level_init

                # move enemies from prep list to list at certain time
                spawn_enemies(current_time)
                # check if any dialogue other than the pass level and fail level
                if len(ingame_level_data.Ingame_data["Dialogue_list"]) >= 3:
                    dialogue_show(current_time)

                # put the changed things on screen
                pygame.display.update()

                clock.tick(fps)

pygame.quit()
