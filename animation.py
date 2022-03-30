import pygame


class AnimateSprite(pygame.sprite.Sprite):
    size = 54

    def __init__(self, sprite_name, sprite_type):
        super().__init__()
        self.image = pygame.image.load(f"graphics/{sprite_type}/{sprite_name}.png")

        # Load sprite
        self.image = get_image(0, 128, self.image)
        self.image.set_colorkey([0, 0, 0])
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.current_image = 0
        self.images = load_animation_images(sprite_name, sprite_type)

    def animate(self, animation_type):
        # Animation Speed
        self.current_image += 0.08

        if animation_type == "walking_left":
            self.images_list = self.images["walking_left"]
        elif animation_type == "walking_right":
            self.images_list = self.images["walking_right"]
        elif animation_type == "walking_up":
            self.images_list = self.images["walking_up"]
        elif animation_type == "walking_down":
            self.images_list = self.images["walking_down"]
        elif animation_type == "death":
            self.images_list = self.images["death"]
        elif animation_type == "fall":
            self.images_list = self.images["fall"]

        # Reset animations
        if animation_type != "death":
            if self.current_image >= len(self.images_list):
                self.current_image = 0

        # Modify current animation
        if animation_type != "death":
            self.image = self.images_list[int(self.current_image)]
        else:
            if self.current_image <= len(self.images_list):
                self.image = self.images_list[int(self.current_image)]

        # Decrease sprite size gradually in the fall case
        if animation_type == "fall":
            if self.size > 0:
                self.size -= 1

        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image.set_colorkey([0, 0, 0])

    def stop_animation(self, last_animation):
        self.current_image = 0
        if last_animation == "walking_left":
            self.images_list = self.images["walking_left"]
        elif last_animation == "walking_right":
            self.images_list = self.images["walking_right"]
        elif last_animation == "walking_up":
            self.images_list = self.images["walking_up"]
        elif last_animation == "walking_down":
            self.images_list = self.images["walking_down"]

        # Modify current animation
        self.image = self.images_list[int(self.current_image)]
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image.set_colorkey([0, 0, 0])


def load_animation_images(sprite_name, sprite_type):
    images = {
        "walking_left": [],
        "walking_right": [],
        "walking_up": [],
        "walking_down": [],
        "death": [],
        "fall": [],
    }
    sprite = pygame.image.load(f"graphics/{sprite_type}/{sprite_name}.png")

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

    return images


def get_image(x, y, sprite):
    image = pygame.Surface([64, 64])
    image.blit(sprite, (0, 0), (x, y, 64, 64))
    return image
