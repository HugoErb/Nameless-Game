import sys

import pyscroll
import pytmx

from player import Player
from settings import *


class Game:
    game_is_running = True

    # General setup
    def __init__(self):
        pygame.init()

        # Window setup
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Nameless Game')

        # Load TMX map
        tmx_data = pytmx.util_pygame.load_pygame("graphics/map/map.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.9

        # Create player
        player_position = tmx_data.get_object_by_name("player_spawn_point")
        self.player = Player(player_position.x, player_position.y)

        # Draw layer group
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        self.clock = pygame.time.Clock()

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[KEY_UP]:
            self.player.move_up()
        elif pressed[KEY_DOWN]:
            self.player.move_down()
        elif pressed[KEY_LEFT]:
            self.player.move_left()
        elif pressed[KEY_RIGHT]:
            self.player.move_right()
        elif pressed[pygame.K_RIGHT] and pressed[pygame.K_UP]:
            self.player.move_right()

    # Checking if player is closing the game
    # Game is closed if the player close the game window
    def run(self):
        while self.game_is_running:

            # Catch key pressed
            self.handle_input()

            # Draw layer on screen
            self.group.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_is_running = False
                    print('Game closed')
                    pygame.quit()
                    sys.exit()

            # Add map to the screen
            self.screen.fill('black')
            # pygame.display.update()

            self.clock.tick(FPS)
