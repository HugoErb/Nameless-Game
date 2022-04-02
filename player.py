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
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()

        # Player stats
        self.health = 100
        self.stamina = 100
        self.attack = 20
        self.state = "alive"

    # Moving methods #####################################################

    def move_right(self):
        # print("Moving Right")
        self.animate("walking_right")
        self.last_animation = "walking_right"
        self.position[0] += self.speed

    def move_left(self):
        # print("Moving Left")
        self.animate("walking_left")
        self.last_animation = "walking_left"
        self.position[0] -= self.speed

    def move_up(self):
        # print("Moving Up")
        self.animate("walking_up")
        self.last_animation = "walking_up"
        self.position[1] -= self.speed

    def move_down(self):
        # print("Moving Down")
        self.animate("walking_down")
        self.last_animation = "walking_down"
        self.position[1] += self.speed

    def move_up_and_right(self):
        # print("Moving Up and Right")
        self.animate("walking_up")
        self.last_animation = "walking_up"
        self.position[1] -= self.speed * 0.8
        self.position[0] += self.speed * 0.8

    def move_up_and_left(self):
        # print("Moving Up and Left")
        self.animate("walking_up")
        self.last_animation = "walking_up"
        self.position[1] -= self.speed * 0.8
        self.position[0] -= self.speed * 0.8

    def move_down_and_right(self):
        # print("Moving Down and Right")
        self.animate("walking_down")
        self.last_animation = "walking_down"
        self.position[1] += self.speed * 0.8
        self.position[0] += self.speed * 0.8

    def move_down_and_left(self):
        # print("Moving Down and Left")
        self.animate("walking_down")
        self.last_animation = "walking_down"
        self.position[1] += self.speed * 0.8
        self.position[0] -= self.speed * 0.8

    def move_back(self):
        # print("Collision")
        Audio("collision", "sounds", 0.5)
        self.position = self.old_position
        self.rect.center = self.position
        self.feet.midbottom = self.rect.midbottom

    def not_moving(self):
        # print("Not Moving")
        self.stop_animation(self.last_animation)

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
            result = self.animate("fall")
            if result:
                self.state = "dead"
            print("Player has fallen")
        else:
            self.die("false")

    def update(self):
        self.rect.center = self.position
        self.feet.midbottom = self.rect.midbottom

    def save_location(self):
        self.old_position = self.position.copy()
