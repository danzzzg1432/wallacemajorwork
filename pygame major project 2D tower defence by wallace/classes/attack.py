"""Attack implementations used by the towers.

Each attack is a ``pygame.sprite.Sprite`` that deals damage to enemies
and optionally applies knockback.  The classes here are spawned by the
towers defined in :mod:`tower` and tick every frame until they expire.
"""

import pygame
from pygame import Vector2
import ingame_level_data
import config
import math

# get data from config file
screen = config.Initialise["screen"]
attack_linearIMG = config.Initialise["attack_linearIMG"]
attack_parabolaIMG = config.Initialise["attack_parabolaIMG"]
fps = config.Initialise["fps"]
linear_dps = config.Tower_preset["Linear tower"]["dps"]
parabola_dps = config.Tower_preset["Parabola tower"]["dps"]

"""
# previously used function, might be useful
def sgn(angle):
  if angle == 0:
    return 0
  return int(math.copysign(1, angle)) # returns either -1, 0, 1
"""

class Attacks(pygame.sprite.Sprite):
    """Base class for all projectile attacks."""

    def __init__(self, resize_factor: float, location: Vector2):
        """Create a generic attack sprite at ``location``."""
        super().__init__()
        self.image = None
        self.rect = None
        self.hit_list = None
        self.hit_box = None
        self.resize_factor = resize_factor
        self.location = location

    def tick(self):
        """Update the attack for the current frame."""
        pass

    def resize(self, resize_factor: float):
        """Scale the sprite when the screen is resized."""
        self.image = pygame.transform.scale_by(self.image, resize_factor)
        self.rect = self.image.get_rect()
        self.rect.center = self.location
        self.resize_factor = resize_factor


class Linear_attack(Attacks):
    """Straight line attack used by the :class:`Linear` tower."""

    def __init__(self, resize_factor: float, direction: Vector2, location: Vector2):
        """Create the linear projectile heading in ``direction``."""
        super().__init__(resize_factor, location)

        self.direction = direction

        # the direction this attack will go
        self.hit_list = None
        self.East = pygame.math.Vector2(1, 0)
        # clockwise angle from East axis
        self.angle = self.direction.angle_to(self.East)

        self.image = pygame.transform.scale_by(pygame.transform.rotate(attack_linearIMG, self.angle), self.resize_factor)
        self.rect = self.image.get_rect()
        self.rect.center = self.location

        #  line collision
        self.line_start = self.location + self.direction.normalize() * 1090
        self.line_end = self.location - self.direction.normalize() * 1090

        self.attack_damage_per_second = linear_dps
        # to make the damage output non-affected by framerate adjustments
        self.attack_damage_per_frame = self.attack_damage_per_second / fps

    def tick(self):
        """Apply damage to any enemies intersecting the line."""
        # get list from the file once and for all for this aim
        Enemy_list = ingame_level_data.Ingame_data["Enemy_list"]
        Enemy_dead_list = ingame_level_data.Ingame_data["Enemy_dead_list"]

        for enemy in Enemy_list:
            # line collision check
            if enemy.rect.clipline((self.line_start, self.line_end)):
                enemy.health -= self.attack_damage_per_frame
                if enemy.health <= 0:
                    ingame_level_data.Ingame_data["current_player_currency"] += enemy.bounty
                    Enemy_list.remove(enemy)
                    Enemy_dead_list.add(enemy)

            #  pixel collision check
        #      if self.linear_mask.overlap(enemy.enemy_mask, (enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y)):
        #         enemy.health -= self.attack_damage_per_frame
        #        # if Enemy is dead
        #       if enemy.health <= 0:
        #          Enemy_list.remove(enemy)
        #         Enemy_dead_list.add(enemy)
        self.kill()


class Parabola_attack(Attacks):
    """Curved attack with optional knockback."""

    def __init__(self, resize_factor: float, angle: float, location: Vector2, extension: float):
        """Create a parabola shaped attack rotated by ``angle``."""
        super().__init__(resize_factor, location)
        self.angle = angle
        self.knockback_value = 15
        self.attack_damage_per_second = parabola_dps
        # to make the damage output non-affected by framerate adjustments
        self.attack_damage_per_frame = self.attack_damage_per_second / fps

        # non-rotated image
        self.image = pygame.transform.scale_by(attack_parabolaIMG, ((self.resize_factor * extension, self.resize_factor)))
        self.original_rect = self.image.get_rect()

        # rotated image
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.location

        # to fix base of the parabola on the tower
        # location is location of tower
        self.x_shift = self.original_rect[2] * math.cos ((180 - self.angle) / 180 * math.pi) / 2
        self.y_shift = self.original_rect[2] * math.sin ((180 - self.angle) / 180 * math.pi) / 2
        self.rect.center = (self.location[0] - self.x_shift, self.location[1] - self.y_shift )

    def tick(self):
        """Deal damage and knock back enemies in its path."""
        # get list from the file once and for all for this aim
        Enemy_list = ingame_level_data.Ingame_data["Enemy_list"]
        Enemy_dead_list = ingame_level_data.Ingame_data["Enemy_dead_list"]

        for enemy in Enemy_list:
            # line collision check
           if enemy.rect.clipline((self.location[0] - self.x_shift * 2, self.location[1] - self.y_shift *2), (self.location[0] - self.x_shift / 2, self.location[1] - self.y_shift / 2)):
                enemy.health -= self.attack_damage_per_frame
                enemy.knockback(self.knockback_value, self.location)
                if enemy.health <= 0:
                    ingame_level_data.Ingame_data["current_player_currency"] += enemy.bounty
                    Enemy_list.remove(enemy)
                    Enemy_dead_list.add(enemy)
        self.kill()

