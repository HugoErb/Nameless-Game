import animation


class Player(animation.AnimateSprite):

    def __init__(self, x, y):
        super().__init__("player", "characters")

        # Set player position
        self.rect = self.image.get_rect()
        self.position = [x, y]

        # Player move speed
        self.speed = 1.5

        # Last animation of player
        self.last_animation = "walking_down"

    # Moving methods #####################################################

    def move_right(self):
        print("Moving Right")
        self.update_animation("walking_right")
        self.last_animation = "walking_right"
        self.position[0] += self.speed

    def move_left(self):
        print("Moving Left")
        self.update_animation("walking_left")
        self.last_animation = "walking_left"
        self.position[0] -= self.speed

    def move_up(self):
        print("Moving Up")
        self.update_animation("walking_up")
        self.last_animation = "walking_up"
        self.position[1] -= self.speed

    def move_down(self):
        print("Moving Down")
        self.update_animation("walking_down")
        self.last_animation = "walking_down"
        self.position[1] += self.speed

    def move_up_and_right(self):
        print("Moving Up and Right")
        self.update_animation("walking_up")
        self.last_animation = "walking_up"
        self.position[1] -= self.speed * 0.8
        self.position[0] += self.speed * 0.8

    def move_up_and_left(self):
        print("Moving Up and Left")
        self.update_animation("walking_up")
        self.last_animation = "walking_up"
        self.position[1] -= self.speed * 0.8
        self.position[0] -= self.speed * 0.8

    def move_down_and_right(self):
        print("Moving Down and Right")
        self.update_animation("walking_down")
        self.last_animation = "walking_down"
        self.position[1] += self.speed * 0.8
        self.position[0] += self.speed * 0.8

    def move_down_and_left(self):
        print("Moving Down and Left")
        self.update_animation("walking_down")
        self.last_animation = "walking_down"
        self.position[1] += self.speed * 0.8
        self.position[0] -= self.speed * 0.8

    def not_moving(self):
        print("Not Moving")
        self.stop_animation(self.last_animation)

    ######################################################################

    def update_animation(self, animation_type):
        self.animate(animation_type)

    def update(self):
        self.rect.center = self.position
