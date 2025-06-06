"""Enemy implementations for the tower defence game."""

import pygame
import config
from pygame.math import Vector2
import ingame_level_data
import random
import copy

# get global data from config
screen = config.Initialise["screen"]
fps = config.Initialise["fps"]
player_health = config.Level_preset["level1"]["player_health"]
enemy_health_font = pygame.font.SysFont(config.Initialise["enemy_health_font"][0], config.Initialise["enemy_health_font"][1], config.Initialise["enemy_health_font"][2], config.Initialise["enemy_health_font"][3])



# use the defined sprite class for its functions
class Enemy(pygame.sprite.Sprite):
    """Base enemy class."""
    def __init__(self, enemy_type, level, spawn_time):
        """Create an enemy instance for a level."""
        pygame.sprite.Sprite.__init__(self)

        # get defined data from input
        ##################################################################################
        self.enemy_type = enemy_type
        # in format of "levelx"
        self.level = level
        self.spawn_time = spawn_time

        # get the data according to the enemy type
        ##################################################################################
        # distance/frame = (distance/second) / (frame/second)
        # so the speed of enemies will not change when changing the fps
        self.distance_per_frame = config.Level_preset[self.level]["enemy_data"][self.enemy_type]["distance_per_second"] / fps
        self.health = config.Level_preset[self.level]["enemy_data"][self.enemy_type]["health"]
        self.checkpoints = list(config.Level_preset[self.level]["checkpoints"])
        self.image = copy.deepcopy(config.Level_preset[self.level]["enemy_data"][self.enemy_type]["image"])
        self.original_image = config.Level_preset[self.level]["enemy_data"][self.enemy_type]["image"]
        self.bounty = config.Level_preset[self.level]["enemy_data"][self.enemy_type]["bounty"]

        # set common data for all enemies
        ##################################################################################
        # initially starts as first checkpoint, i.e. first checkpoint is spawn point
        self.location = Vector2(self.checkpoints[0])
        # initially goes towards the 2nd checkpoint in the list of checkpoints
        self.target_checkpoint = 1

#        self.image = config.Level_data[self.level]["enemy_data"][self.enemy_type]["image"]
        self.movement = None
        self.target_location = None

        self.rect = self.image.get_rect()
        self.rect.center = self.location

        self.old_resize_factor = 1

        self.knockback_resistance = 1
        self.knockback_resistance_growth_value = 1.1   # this value >= 1
        self.knockback_minimum = 1.5

    # show health of enemy, logically belongs to the enemy class
    def show_health(self, health: int, location: Vector2):
        """Display inverted health comparison."""
        """Show the health with a random comparison number."""
        """Render the enemy's health value."""
        global enemy_health_font
        show_health = enemy_health_font.render(f"{round(health)}", True, (255, 255, 0))
        screen.blit(show_health, location)


    def death(self):
        """Handle enemy death and award bounty."""
        ingame_level_data.Ingame_data["current_player_currency"] += self.bounty
        self.kill()


    def move(self):
        """Advance the enemy along its path."""
        # modification of global variable needed
        global player_health
        # check if there is still checkpoints to go
        if self.target_checkpoint < len(self.checkpoints):
            # O is origin, T is the target checkpoint. This is the vector OT
            self.target_location = Vector2(self.checkpoints[self.target_checkpoint])

            # self.location is OL the vector from origin to the current checkpoint.
            # Therefore, self.movement is OT - OL = LO + OT = LT,
            # which is the vector for moving from current checkpoint to the targeted checkpoint.
            self.movement = self.target_location - self.location

            distance_from_target = self.movement.length()
            # if the enemy is very close to the previous one
            if distance_from_target < self.distance_per_frame:
                # move for the remaining distance_from_target between it and the target
                self.location += self.movement.normalize()*distance_from_target
                # change target
                self.target_checkpoint += 1
            else:  # haven't reached
                # normalise converts the vector to a vector with total length of 1
                # therefore the enemy will move in the movement's direction for a number(as defined in speed) of pixels
                self.location += self.movement.normalize()*self.distance_per_frame

            self.rect.center = self.location
        # enemy has finished path
        else:
            ingame_level_data.Ingame_data["current_player_health"] -= self.health
            self.death()
#            print('-' , self.health)  #  show health when finish path

    def resize(self, resize_factor: float):
        """Resize ant_s specific data."""
        """Resize ant_g specific data."""
        """Resize snake specific data."""
        """Resize enemy sprite and update movement values."""
        self.image = pygame.transform.scale_by(self.original_image, resize_factor)

        self.chekcpoints = ingame_level_data.Ingame_data["checkpoints"]
      #  self.checkpoints = []
       # for i in config.Level_preset[self.level]["checkpoints"]:
        #    self.checkpoints.append((i[0] * resize_factor, i[1] * resize_factor))

        self.distance_per_frame = config.Level_preset[self.level]["enemy_data"][self.enemy_type]["distance_per_second"] / fps * resize_factor

        self.location = Vector2(self.location[0] / self.old_resize_factor * resize_factor , self.location[1] / self.old_resize_factor * resize_factor)
        self.rect = self.image.get_rect()
        self.rect.center = self.location

        self.old_resize_factor = resize_factor

        global enemy_health_font
        enemy_health_font = pygame.font.SysFont(config.Initialise["enemy_health_font"][0], round(config.Initialise["enemy_health_font"][1] * resize_factor), config.Initialise["enemy_health_font"][2], config.Initialise["enemy_health_font"][3])

    def knockback(self, knockback_value: int, knock_back_origin: Vector2):
        """Apply knockback effect."""
        knockback_range = (knockback_value - min(self.knockback_resistance, knockback_value)) * pygame.math.Vector2.normalize(self.location - knock_back_origin)
        self.location += knockback_range
        self.knockback_resistance = min(knockback_value - self.knockback_minimum, self.knockback_resistance * self.knockback_resistance_growth_value)


class Snake(Enemy):
    """Enemy that displays its health above."""
    # equal sign
    def __init__(self, level, spawn_time):
        """Create an Ant_s enemy."""
        """Create an Ant_g enemy."""
        """Create a Snake enemy."""
        Enemy.__init__(self, "snake", level, spawn_time)
        self.original_message_align = 5

    # show health of enemy, logically belongs to the enemy class
    def show_health(self, health: int, location: Vector2):
        global enemy_health_font
        show_health = enemy_health_font.render(f"{round(health)}", True, (255, 255, 0))
        screen.blit(show_health, (location[0], location[1] - self.message_align))

    def resize(self, resize_factor: float):
        self.message_align = self.original_message_align * resize_factor

        self.image = pygame.transform.scale_by(self.original_image, resize_factor)

        self.checkpoints = []
        for i in config.Level_preset[self.level]["checkpoints"]:
            self.checkpoints.append((i[0] * resize_factor, i[1] * resize_factor))

        self.distance_per_frame = config.Level_preset[self.level]["enemy_data"][self.enemy_type]["distance_per_second"] / fps * resize_factor

        self.location = Vector2(self.location[0] / self.old_resize_factor * resize_factor , self.location[1] / self.old_resize_factor * resize_factor)
        self.rect = self.image.get_rect()
        self.rect.center = self.location

        self.old_resize_factor = resize_factor

        global enemy_health_font
        enemy_health_font = pygame.font.SysFont(config.Initialise["enemy_health_font"][0], round(config.Initialise["enemy_health_font"][1] * resize_factor), config.Initialise["enemy_health_font"][2], config.Initialise["enemy_health_font"][3])


class Ant_g(Enemy):
    """Enemy that requires health to be greater than a number."""
    # greater than
    def __init__(self, level, spawn_time):
        Enemy.__init__(self, "ant_g", level, spawn_time)
        self.randint: int = random.randint(-100,100)

        ## means dont in resize function
        # get the width needed to center this message, allow functions in this class to accesss the width 
        ##health_message_align = enemy_health_font.render(str(self.randint), True, (255, 255, 0))
        # +13 in consideration of the length of the "<" symbol
        ##self.message_width_half: float = health_message_align.get_rect()[2] + 13

    # show a health and the number that it needs to be greater than
    def show_health(self, health: int, location: Vector2):
        global enemy_health_font
        # get the strings
        health_message: str = f"{self.randint} < {round(health + self.randint)}"
        # turn the strings into pygame rectangles
        health_message = enemy_health_font.render(health_message, True, (255, 255, 0))

        # center the "<" in health_message 
        message_height_half = health_message.get_rect()[3] / 2
        screen.blit(health_message, (location[0] - self.message_width_half, location[1] - message_height_half))

    # aditionally update the health_message_align
    def resize(self, resize_factor: float):
        self.image = pygame.transform.scale_by(self.original_image, resize_factor)

        self.checkpoints = []
        for i in config.Level_preset[self.level]["checkpoints"]:
            self.checkpoints.append((i[0] * resize_factor, i[1] * resize_factor))

        self.distance_per_frame = config.Level_preset[self.level]["enemy_data"][self.enemy_type]["distance_per_second"] / fps * resize_factor

        self.location = Vector2(self.location[0] / self.old_resize_factor * resize_factor , self.location[1] / self.old_resize_factor * resize_factor)
        self.rect = self.image.get_rect()
        self.rect.center = self.location

        self.old_resize_factor = resize_factor

        global enemy_health_font
        enemy_health_font = pygame.font.SysFont(config.Initialise["enemy_health_font"][0], round(config.Initialise["enemy_health_font"][1] * ingame_level_data.Ingame_data["resize_factor"]), config.Initialise["enemy_health_font"][2], config.Initialise["enemy_health_font"][3])

        # get the width needed to center this message, allow functions in this class to accesss the width 
        health_message_align = enemy_health_font.render(str(self.randint), True, (255, 255, 0))
        # +13 in consideration of the length of the "<" symbol
        self.message_width_half: float = health_message_align.get_rect()[2] + 13 * resize_factor


class Ant_s(Enemy):
    """Enemy whose apparent health is reduced."""
    # smaller than
    def __init__(self, level, spawn_time):
        Enemy.__init__(self, "ant_s", level, spawn_time)
        self.randint: int = random.randint(100,200)
        self.appearent_health: int = self.randint - self.health 

        ## means that they are defined in the resize function
        # get the width needed to center this message, allow functions in this class to accesss the width 
        health_message_align: str = f"{self.randint} "
        ##health_message_align = enemy_health_font.render(health_message_align, True, (255, 255, 0))
        # +13 in consideration of the length of the ">" symbol
        ##self.message_width_half: float = health_message_align.get_rect()[2] + 13

    # show a health and the number that it needs to be greater than
    def show_health(self, health: int, location: Vector2):
        global enemy_health_font
        # get the strings
        health_message: str = f"{self.randint} > {round(-health + self.randint)}"
        # turn the strings into pygame rectangles
        health_message = enemy_health_font.render(health_message, True, (255, 255, 0))

        # center the ">" in health_message 
        message_height_half = health_message.get_rect()[3] / 2
        screen.blit(health_message, (location[0] - self.message_width_half, location[1] - message_height_half))

    # aditionally update the health_message_align
    def resize(self, resize_factor: float):
        self.image = pygame.transform.scale_by(self.original_image, resize_factor)

        self.checkpoints = []
        for i in config.Level_preset[self.level]["checkpoints"]:
            self.checkpoints.append((i[0] * resize_factor, i[1] * resize_factor))

        self.distance_per_frame = config.Level_preset[self.level]["enemy_data"][self.enemy_type]["distance_per_second"] / fps * resize_factor

        self.location = Vector2(self.location[0] / self.old_resize_factor * resize_factor , self.location[1] / self.old_resize_factor * resize_factor)
        self.rect = self.image.get_rect()
        self.rect.center = self.location

        self.old_resize_factor = resize_factor

        global enemy_health_font
        enemy_health_font = pygame.font.SysFont(config.Initialise["enemy_health_font"][0], round(config.Initialise["enemy_health_font"][1] * ingame_level_data.Ingame_data["resize_factor"]), config.Initialise["enemy_health_font"][2], config.Initialise["enemy_health_font"][3])
        
        # get the width needed to center this message, allow functions in this class to accesss the width 
        health_message_align = enemy_health_font.render(str(self.randint), True, (255, 255, 0))
        # +13 in consideration of the length of the ">" symbol
        self.message_width_half: float = health_message_align.get_rect()[2] + 13 * resize_factor

