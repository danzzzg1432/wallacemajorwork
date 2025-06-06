"""UI button and shop item classes."""

import pygame
import config
import ingame_level_data

# get global data from config
screen = config.Initialise["screen"]
currency = ingame_level_data.Ingame_data["current_player_currency"] 
queryIMG = config.Initialise["queryIMG"]


# use the defined sprite class for its functions
class Button:
    """Generic clickable button."""
    def __init__(self, position_in_list: int, level: int):
        """Initialise the button from level presets."""
        # get defined data from input
        ##################################################################################
        self.position_in_list = position_in_list # position in the preset list, starting from 0
        # in format of "levelx" , x is an integer
        self.level = level
        self.storage = "button_data"

        # get the data according to the position
        ##################################################################################
        self.original_image = config.Level_preset[self.level][self.storage][self.position_in_list][0]
        self.resize(ingame_level_data.Ingame_data["resize_factor"])

    def __repr__(self):
        return f"{self.x, self.y, self.rect[2], self.rect[3]}"

    def draw(self):
        """Draw the item and its UI elements."""
        """Placeholder method for drawing."""
        """Blit the button image onto the screen."""
        screen.blit(self.image, (self.x, self.y))

    def resize(self, resize_factor: float):
        """Scale the button when the window size changes."""
        self.image = pygame.transform.scale_by(self.original_image, resize_factor)
        self.rect = self.image.get_rect()
        self.x = config.Level_preset[self.level][self.storage][self.position_in_list][1][0] * resize_factor
        self.y = config.Level_preset[self.level][self.storage][self.position_in_list][1][1] * resize_factor


    def check_press(self, mouse_pos):
        """Check if the item or its query icon was clicked."""
        """Return True if the mouse is within this rectangle."""
        """Return True if ``mouse_pos`` is inside this button."""
        # check if pressed on this item
        if self.x <= mouse_pos[0] <= (self.x + self.rect[2]) and self.y <= mouse_pos[1] <= (self.y + self.rect[3]):
            return True
        else: return False


# button that is not drawn every tick, stored in another list
class Dialogue(Button):
    """Button that is only shown as part of a dialogue."""
    def __init__(self, position_in_list: int, level: int):
        """Initialise the dialogue image."""
        super().__init__(position_in_list, level)
        # get defined data from input
        ##################################################################################
        self.position_in_list = position_in_list # position in the preset list, starting from 0
        # in format of "levelx" , x is an integer
        self.level = level
        self.storage = "dialogue_data"

        # get the data according to the position
        ##################################################################################
        self.original_image = config.Level_preset[self.level][self.storage][self.position_in_list][0]
        self.resize(ingame_level_data.Ingame_data["resize_factor"])


# button without the image
class Rect:
    """Invisible clickable area."""
    def __init__(self, position_in_list: int, level: int):
        """Create a rectangle from level preset."""
        # get defined data from input
        ##################################################################################
        self.position_in_list = position_in_list # position in the preset list, starting from 0
        # in format of "levelx" , x is an integer
        self.level = level

        self.original_rect = config.Level_preset[self.level]["rect_data"][self.position_in_list]
        self.resize(ingame_level_data.Ingame_data["resize_factor"])

    def resize(self, resize_factor):
        """Resize all UI elements for the item."""
        """Resize the rectangle when the window changes."""
        self.rect = [i * resize_factor for i in self.original_rect]
        self.x = self.rect[0]
        self.y = self.rect[1]

    def draw(self):
        pass
    
    def __repr__(self):
        return f"{self.x, self.y, self.rect[2], self.rect[3]}"

    def check_press(self, mouse_pos):
        # check if pressed on this item
        if self.x <= mouse_pos[0] <= (self.x + self.rect[2]) and self.y <= mouse_pos[1] <= (self.y + self.rect[3]):
            return True
        else: return False


# button but with more capabilities
class Shop_item:
    """Item displayed in the shop UI."""
    def __init__(self, position_in_list: int, level: int):
        """Initialise item data from presets."""
        # get defined data from input
        ##################################################################################
        self.position_in_list = position_in_list # position in the preset list, starting from 0
        # in format of "levelx" , x is an integer
        self.level = level
        
        # get the data according to the position
        ##################################################################################
        self.name: str = config.Level_preset[self.level]["shop_data"][self.position_in_list][0]
        # unlock is not a must have feature, might not be implemented
        self.unlocked = config.Level_preset[self.level]["shop_data"][self.position_in_list][1]

        self.dps = config.Tower_preset[self.name]["dps"]
        self.description = config.Tower_preset[self.name]["description"]
        self.details = config.Tower_preset[self.name]["details"]
        self.price = config.Tower_preset[self.name]["price"]
        self.original_towerIMG = config.Tower_preset[self.name]["image"]
        self.resize(ingame_level_data.Ingame_data["resize_factor"])

    def draw(self):
        pygame.draw.rect(screen, (102, 51, 0), pygame.Rect(self.rect))
        pygame.draw.rect(screen, (153, 102, 0), pygame.Rect(self.inner_rect))
        screen.blit(self.show_name, (self.name_x, self.name_y))
        screen.blit(self.towerIMG, (self.towerIMG_x , self.towerIMG_y))
        screen.blit(self.show_description, (self.description_x, self.description_y))
        screen.blit(self.show_price, (self.price_x, self.price_y))
        screen.blit(self.queryIMG, (self.queryIMG_x , self.queryIMG_y))

    def __repr__(self):
        return f"{self.x, self.y}"

    def resize(self, resize_factor):
        self.towerIMG = pygame.transform.scale_by(self.original_towerIMG, resize_factor * 0.6)
        self.queryIMG = pygame.transform.scale_by(queryIMG, resize_factor)

        self.rect = (740 * resize_factor, float(80 + 80 * self.position_in_list) * resize_factor, 195 * resize_factor, 70 * resize_factor)
        self.x = self.rect[0]
        self.y = self.rect[1]

        # images
        self.towerIMG_x = self.x + (3 * resize_factor)
        self.towerIMG_y = self.y + (-40 * resize_factor)

        self.inner_rect = (self.rect[0] + (5 * resize_factor), self.rect[1] + (5 * resize_factor), self.rect[2] - (10 * resize_factor), self.rect[3] - (10 * resize_factor))

        self.queryIMG_x = self.x + self.rect[2] - 16 * resize_factor
        self.queryIMG_y = self.y
        self.queryIMG_height = 16 * resize_factor

        # texts
        self.extreme_font = pygame.font.SysFont(config.Initialise["player_font"][0], round(config.Initialise["player_font"][1] * resize_factor * 3), config.Initialise["player_font"][2], config.Initialise["player_font"][3])
        self.big_font = pygame.font.SysFont(config.Initialise["player_font"][0], round(config.Initialise["player_font"][1] * resize_factor), config.Initialise["player_font"][2], config.Initialise["player_font"][3])
        self.small_font = pygame.font.SysFont(config.Initialise["player_font"][0], round(config.Initialise["player_font"][1] * resize_factor / 2), config.Initialise["player_font"][2], config.Initialise["player_font"][3])

        self.name_x = self.x + (50 * resize_factor)
        self.name_y = self.y + (10 * resize_factor)
        self.show_name = self.big_font.render(self.name , True, (255, 255, 255))

        self.description_x = self.x + (10 * resize_factor)
        self.description_y = self.y + (50 * resize_factor)
        self.show_description = self.small_font.render(self.description , True, (255, 255, 255))

        self.price_x = self.x + (100 * resize_factor)
        self.price_y = self.y + (40 * resize_factor)
        self.show_price = self.big_font.render(str(self.price) , True, (255, 255, 0))

        self.query_rect =[i * resize_factor for i in [50, 50, 840, 440]]
        self.query_inner_rect = [i * resize_factor for i in [60, 60, 820, 420]]
        self.query_image_cords = [i * resize_factor for i in [70, -30]]
        self.query_line_start = [i * resize_factor for i in [70, 180]]
        self.query_line_end = [i * resize_factor for i in [870, 180]]
        self.query_line_width = int(resize_factor * 5)
        self.query_name_cords = [i * resize_factor for i in [200, 70]]
        self.show_query_name = self.extreme_font.render(self.name , True, (255, 255, 255))
        self.query_price_cords = [i * resize_factor for i in [640,70]]
        self.show_query_price = self.big_font.render('price: ' + str(self.price), True, (255, 255, 0))
        self.query_dps_cords = [i * resize_factor for i in [640, 120]]
        self.show_query_dps = self.big_font.render('damage per second: ' + str(self.dps), True, (255, 117, 117))

        # seperate lines because the details are too long
        self.query_details_cords : list = []
        self.show_query_details : list = []
        for i in range(0, len(self.details)):
            self.query_details_cords.append([70 * resize_factor, (250 + 30 * i) * resize_factor])
            self.show_query_details.append(self.big_font.render(self.details[i], True, (255, 255, 255)))

        self.query_return_cords = [i * resize_factor for i in [300, 420]]
        self.show_query_return = self.big_font.render('click again to resume', True, (255, 255, 255))

    def query(self):
        """Display an information overlay for this item."""
        query = True
        while query == True:
            # boarder
            pygame.draw.rect(screen, (102, 51, 0), pygame.Rect(self.query_rect))
            pygame.draw.rect(screen, (120, 81, 46), pygame.Rect(self.query_inner_rect))

            # above line
            screen.blit(pygame.transform.scale_by(self.towerIMG, 2), self.query_image_cords)
            screen.blit(self.show_query_name, self.query_name_cords)
            screen.blit(self.show_query_price, self.query_price_cords)
            screen.blit(self.show_query_dps, self.query_dps_cords)
        
            pygame.draw.line(screen, (102, 51, 0), self.query_line_start, self.query_line_end, self.query_line_width)
            # below line

            for i in range(0, len(self.query_details_cords)):
                screen.blit(self.show_query_details[i], self.query_details_cords[i])
            screen.blit(self.show_query_return, self.query_return_cords)

            pygame.display.update()

            for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        query = False

    def check_press(self, mouse_pos):
        # check if pressed on this item
        if self.x <= mouse_pos[0] <= (self.x + self.rect[2]) and self.y <= mouse_pos[1] <= (self.y + self.rect[3]):
            if self.queryIMG_x <= mouse_pos[0] and self.queryIMG_y <= mouse_pos[1] <= (self.queryIMG_y + self.queryIMG_height):
                self.query()
                return False
            return True
        else: return False

