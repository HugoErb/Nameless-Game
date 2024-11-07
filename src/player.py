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

        # Réinitialiser l'animation d'attaque
        self.animation_finished = False

        # Dictionnaire de correspondance pour déterminer la direction d'attaque
        attack_directions = {
            "walking_up": "attacking_up",
            "walking_down": "attacking_down",
            "walking_left": "attacking_left",
            "walking_right": "attacking_right",
        }

        # Utilise la dernière animation pour déterminer la direction d'attaque
        attacking_direction = attack_directions.get(self.last_animation, "attacking_down")

        # Lance l'animation d'attaque dans la direction déterminée
        self.animate(attacking_direction)

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
        if self.state != "dead":
            # Animate the falling
            result = self.animate("fall")
            if result:
                self.state = "dead"
            # Move the player to compensate the size reduction
            self.position[1] += 0.25
            self.position[0] += 0.25
        else:
            if self.health > 0:
                print("Player has fallen")
                self.die("false")

    def update(self):
        self.rect.center = self.position
        self.feet.midbottom = self.rect.midbottom

    def save_location(self):
        self.old_position = self.position.copy()
