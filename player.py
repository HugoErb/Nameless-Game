import animation


class Player(animation.AnimateSprite):

    def __init__(self, x, y):
        super().__init__("player", "characters")

        # Set player position
        self.rect = self.image.get_rect()
        self.position = [x, y]

        # Player move speed
        self.speed = 1.5

    # Moving methods #####################################################

    def move_right(self):
        print("Moving Right")
        self.position[0] += self.speed

    def move_left(self):
        print("Moving Left")
        self.position[0] -= self.speed

    def move_up(self):
        print("Moving Up")
        self.position[1] -= self.speed

    def move_down(self):
        print("Moving Down")
        self.position[1] += self.speed

    def move_up_and_right(self):
        print("Moving Up and Right")
        self.position[1] -= self.speed * 0.8
        self.position[0] += self.speed * 0.8

    def move_up_and_left(self):
        print("Moving Up and Left")
        self.position[1] -= self.speed * 0.8
        self.position[0] -= self.speed * 0.8

    def move_down_and_right(self):
        print("Moving Down and Right")
        self.position[1] += self.speed * 0.8
        self.position[0] += self.speed * 0.8

    def move_down_and_left(self):
        print("Moving Down and Left")
        self.position[1] += self.speed * 0.8
        self.position[0] -= self.speed * 0.8

    ######################################################################

    def update(self):
        self.rect.center = self.position
