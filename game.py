import sys

import pyscroll
import pytmx

from player import Player
from settings import *


class Game:

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
        map_layer.zoom = 2.5

        # Create player
        player_position = tmx_data.get_object_by_name("player_spawn_point")
        self.player = Player(player_position.x, player_position.y)

        # Create collisions
        self.collisions = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.collisions.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Draw layer group
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        self.clock = pygame.time.Clock()

    # Manage player movements
    def handle_input(self):
        pressed = pygame.key.get_pressed()

        # Animate the sprite when the player move in a certain direction
        if pressed[KEY_UP] and not pressed[KEY_RIGHT] and not pressed[KEY_LEFT] and not pressed[KEY_DOWN]:
            self.player.move_up()
        elif pressed[KEY_DOWN] and not pressed[KEY_RIGHT] and not pressed[KEY_LEFT] and not pressed[KEY_UP]:
            self.player.move_down()
        elif pressed[KEY_LEFT] and not pressed[KEY_UP] and not pressed[KEY_DOWN] and not pressed[KEY_RIGHT]:
            self.player.move_left()
        elif pressed[KEY_RIGHT] and not pressed[KEY_UP] and not pressed[KEY_DOWN] and not pressed[KEY_LEFT]:
            self.player.move_right()
        elif pressed[KEY_RIGHT] and pressed[KEY_UP]:
            self.player.move_up_and_right()
        elif pressed[KEY_LEFT] and pressed[KEY_UP]:
            self.player.move_up_and_left()
        elif pressed[KEY_RIGHT] and pressed[KEY_DOWN]:
            self.player.move_down_and_right()
        elif pressed[KEY_LEFT] and pressed[KEY_DOWN]:
            self.player.move_down_and_left()

        # If the player do not move, reset animation
        elif not pressed[KEY_UP] and not pressed[KEY_RIGHT] and not pressed[KEY_LEFT] and not pressed[KEY_DOWN]:
            self.player.not_moving()

    def update(self):
        self.group.update()

        # Check for collisions
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.collisions) > -1:
                sprite.move_back()

    def run(self):
        # While the game is running
        game_is_running = True
        while game_is_running:

            # Save player location
            self.player.save_location()

            # Catch key pressed
            self.handle_input()

            # Draw layer on screen
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

            # Game is closed if the player close the game window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_is_running = False
                    print('Game closed')
                    pygame.quit()
                    sys.exit()

            # Fill the empty part of the screen with black
            self.screen.fill('black')

            # Manage FPS
            self.clock.tick(FPS)
