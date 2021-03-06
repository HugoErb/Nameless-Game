import pygame


class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, sprite_name, sprite_type):
        super().__init__()

        # Animations setup
        self.last_animation = "none"
        self.animation_finished = False
        self.size = 54
        self.current_image = 0

        # Load sprite
        self.image = pygame.image.load(f"../graphics/{sprite_type}/{sprite_name}.png")
        self.image = get_image(0, 128, self.image)
        self.image.set_colorkey(0, 0)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.images = load_animation_images(sprite_name, sprite_type)

        # Animation and player speed
        self.clock = 0
        self.speed = 1.1

    def animate(self, animation_type):
        # We only launch the method if the animation is not finished
        if not self.animation_finished:

            # Reset loop index for new animation launched
            if animation_type != self.last_animation:
                self.last_animation = animation_type
                self.current_image = 0
                self.animation_finished = False

            # Animation speed
            if animation_type.startswith("attacking"):
                self.clock += self.speed * 10
            else:
                self.clock += self.speed * 8.5

            # When the clock timer is reached
            if self.clock >= 100:
                # Modify current animation
                if animation_type != "death" and not animation_type.startswith("attacking"):
                    self.current_image += 1
                elif animation_type == "death" or animation_type.startswith("attacking"):
                    if self.current_image + 1 < len(self.images[animation_type]):
                        self.current_image += 1
                    else:
                        self.animation_finished = True
                        print("L'animation " + animation_type + " est terminée.")

                # Reset animation loop
                if self.current_image >= len(
                        self.images[animation_type]) and (
                        animation_type != "death" or not animation_type.startswith("attacking")):
                    self.current_image = 0
                self.clock = 0

            # Transform the sprite
            self.image = self.images[animation_type][self.current_image]
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            self.image.set_colorkey(0, 0)

            # Decrease sprite size gradually in the fall case
            if animation_type == "fall":
                if self.size > 0:
                    self.size -= 0.5
                else:
                    self.animation_finished = True

            if self.animation_finished:
                return True
            else:
                return False

    def stop_animation(self, last_animation):
        self.current_image = 0
        self.image = self.images[last_animation][self.current_image]

        # Modify current animation
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image.set_colorkey(0, 0)


def load_animation_images(sprite_name, sprite_type):
    images = {
        "walking_left": [],
        "walking_right": [],
        "walking_up": [],
        "walking_down": [],
        "death": [],
        "fall": [],
        "attacking_left": [],
        "attacking_right": [],
        "attacking_up": [],
        "attacking_down": []
    }
    sprite = pygame.image.load(f"../graphics/{sprite_type}/{sprite_name}.png")

    # Walking animation
    for i in range(0, 4):
        for j in range(0, 9):
            img_list = get_image((64 * j), (512 + 64 * i), sprite)
            if i == 0:
                images["walking_up"].append(img_list)
            elif i == 1:
                images["walking_left"].append(img_list)
            elif i == 2:
                images["walking_down"].append(img_list)
            elif i == 3:
                images["walking_right"].append(img_list)

    # Death animation
    for i in range(0, 6):
        img_list = get_image((64 * i), 1280, sprite)
        images["death"].append(img_list)

    # Falling animation
    for i in range(0, 2):
        img_list = get_image((320 + 64 * i), 128, sprite)
        images["fall"].append(img_list)

    # Attacking animation
    for i in range(0, 4):
        for j in range(0, 6):
            img_list = get_image((64 * j), (768 + 64 * i), sprite)
            if i == 0:
                images["attacking_up"].append(img_list)
            elif i == 1:
                images["attacking_left"].append(img_list)
            elif i == 2:
                images["attacking_down"].append(img_list)
            elif i == 3:
                images["attacking_right"].append(img_list)

    return images


def get_image(x, y, sprite):
    image = pygame.Surface([64, 64])
    image.blit(sprite, (0, 0), (x, y, 64, 64))
    return image
