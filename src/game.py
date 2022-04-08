import sys

from player import Player
from settings import *
from src.map import MapManager


class Game:

    def __init__(self):
        pygame.init()

        # Variables #######################################################

        # Game setup
        self.game_is_running = True
        self.window_name = WINDOW_NAME
        self.window_icon_path = WINDOW_ICON_PATH

        # Window setup
        icon = pygame.image.load(self.window_icon_path)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGTH))
        pygame.display.set_caption(self.window_name)
        pygame.display.set_icon(icon)

        # Create player
        self.player = Player(0, 0)
        self.map_manager = MapManager(self.screen, self.player)
        self.is_attacking = False

        self.clock = pygame.time.Clock()

    # Manage player movements
    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if self.player.state == "alive":

            # Attacking animation
            if not self.is_attacking:
                if pressed[KEY_ATTACKING]:
                    self.player.attacking()

                # Move and animate the sprite when the player move in a certain direction
                elif pressed[KEY_UP] and not pressed[KEY_RIGHT] and not pressed[KEY_LEFT] and not pressed[KEY_DOWN]:
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
        self.map_manager.update()

    def run(self):
        # While the game is running
        while self.game_is_running:

            # Save player location
            self.player.save_location()

            # Catch key pressed
            self.handle_input()

            # Update several aspects of the game each frame
            self.update()

            # Center camera on player
            if self.player.state == "alive":
                self.map_manager.center_camera()

            # Draw layer on screen
            self.map_manager.draw()
            pygame.display.flip()

            # Game is closed if the player close the game window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('Game closed')
                    self.game_is_running = False
                    pygame.quit()
                    sys.exit()

            # Fill the empty part of the screen with black
            self.screen.fill(WINDOW_BACKGROUND_COLOR)

            # Set Frame Per Second
            self.clock.tick(FPS)
