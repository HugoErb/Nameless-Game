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

            # Animation d'attaque
            if not self.is_attacking:
                if pressed[KEY_ATTACKING]:
                    self.player.attacking()

                # Gérer le mouvement du joueur
                else:
                    self.handle_movement(pressed)

                    # Si aucune touche de direction n'est pressée, réinitialiser l'animation
                    if not any([pressed[KEY_UP], pressed[KEY_DOWN], pressed[KEY_LEFT], pressed[KEY_RIGHT]]):
                        self.player.not_moving()

    def handle_movement(self, pressed):
        # Dictionnaire pour gérer la correspondance des touches et des directions
        directions = {
            (True, False, False, False): "up",
            (False, True, False, False): "down",
            (False, False, True, False): "left",
            (False, False, False, True): "right",
            (True, False, False, True): "up_right",
            (True, False, True, False): "up_left",
            (False, True, False, True): "down_right",
            (False, True, True, False): "down_left"
        }

        # Déterminer la direction en fonction des touches pressées
        key_state = (
            pressed[KEY_UP],
            pressed[KEY_DOWN],
            pressed[KEY_LEFT],
            pressed[KEY_RIGHT]
        )

        # Obtenir la direction à partir du dictionnaire et appeler move si une direction est trouvée
        direction = directions.get(key_state)
        if direction:
            self.player.move(direction)

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
