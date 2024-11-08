import random

import pygame

import animation
from audio import Audio


class Player(animation.AnimateSprite):

    def __init__(self, x, y):
        super().__init__("player", "characters")

        # Set player position
        self.rect = self.image.get_rect()
        self.position = [x, y]

        # Last animation of player
        self.last_animation = "walking_down"

        # Last animation of player before falling
        self.last_animation_before_falling = ""

        # Initialize feet of the player, for better collisions and effects
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 10)
        self.old_position = self.position.copy()

        # Player stats
        self.health = 100
        self.stamina = 100
        self.attack = 20
        self.state = "alive"
        self.attacking_animation_is_finished = True

    # Moving method #####################################################

    def move(self, direction):
        if self.attacking_animation_is_finished == True:
            # Définition des vecteurs de mouvement pour chaque direction
            directions = {
                "right": (1, 0),
                "left": (-1, 0),
                "up": (0, -1),
                "down": (0, 1),
                "up_right": (0.8, -0.8),
                "up_left": (-0.8, -0.8),
                "down_right": (0.8, 0.8),
                "down_left": (-0.8, 0.8)
            }

            # Récupération du vecteur correspondant à la direction
            dx, dy = directions.get(direction, (0, 0))

            # Définir l'animation en fonction de la direction
            if "right" in direction:
                self.animate("walking_right")
                self.last_animation = "walking_right"
            elif "left" in direction:
                self.animate("walking_left")
                self.last_animation = "walking_left"
            elif "up" in direction:
                self.animate("walking_up")
                self.last_animation = "walking_up"
            elif "down" in direction:
                self.animate("walking_down")
                self.last_animation = "walking_down"

            # Mise à jour de la position
            self.position[0] += dx * self.speed
            self.position[1] += dy * self.speed

    def move_back(self):
        # print("Collision")
        Audio("collision", "sounds", 0.4)
        self.position = self.old_position
        self.rect.center = self.position
        self.feet.midbottom = self.rect.midbottom

    def not_moving(self):
        # print("Not Moving")
        self.stop_animation(self.last_animation)

    def attacking(self):
        slash_sounds = ["slash", "slash2"]
        Audio(random.choice(slash_sounds), "sounds", 0.4)

        # L'attaque commence
        self.attacking_animation_is_finished = False

        # On utilise la dernière animation pour déterminer la direction d'attaque
        attack_directions = {
            "walking_up": "attacking_up",
            "attacking_up": "attacking_up",
            "walking_down": "attacking_down",
            "attacking_down": "attacking_down",
            "walking_left": "attacking_left",
            "attacking_left": "attacking_left",
            "walking_right": "attacking_right",
            "attacking_right": "attacking_right"
        }
        attacking_direction = attack_directions.get(self.last_animation, "attacking_down")

        # Lance l'animation d'attaque dans la direction déterminée
        self.animate(attacking_direction)

        self.attacking_animation_is_finished = True

        ######################################################################

    def die(self, make_animation):
        if self.health > 0:
            # Set life to 0 gradually
            while self.health > 0:
                self.health -= 1
            print("Player is dead")
            self.state = "dead"
        if make_animation == "true":
            self.animate("death")

    def fall(self):
        """
        Gère l'animation de chute et fait en sorte que le joueur continue légèrement son mouvement
        dans la dernière direction de marche avant de basculer dans l'état 'dead'.

        Lorsque la taille du sprite diminue, le joueur est progressivement déplacé pour compenser cette réduction.
        Si la chute est terminée, l'état passe à 'dead'.
        """
        if self.last_animation_before_falling == "":
            self.last_animation_before_falling = self.last_animation

        if self.state != "dead":
            # Animation de la chute
            result = self.animate("fall")
            if result:
                self.state = "dead"

            # Compense la réduction de taille en ajustant la position
            self.position[0] += 0.25
            self.position[1] += 0.25

            # Application d'une continuation de mouvement plus marquée dans la dernière direction
            move_offsets = {
                "walking_right": (0.25, 0),
                "walking_left": (-0.25, 0),
                "walking_up": (0, -0.1),
                "walking_down": (0, 0.3),
                "walking_up_right": (0.5, -0.5),
                "walking_up_left": (-0.5, -0.5),
                "walking_down_right": (0.5, 0.5),
                "walking_down_left": (-0.5, 0.5)
            }
            dx, dy = move_offsets.get(self.last_animation_before_falling, (0, 0))
            self.position[0] += dx
            self.position[1] += dy

        else:
            # Vérifie si le joueur a encore de la vie pour déclencher la mort
            if self.health > 0:
                print("Player has fallen")
                self.die("false")

    def update(self):
        self.rect.center = self.position
        self.feet.midbottom = self.rect.midbottom

    def save_location(self):
        self.old_position = self.position.copy()
