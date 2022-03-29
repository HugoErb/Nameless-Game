import pygame


class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, sprite_name, sprite_type):
        super().__init__()
        self.image = pygame.image.load(f"graphics/{sprite_type}/{sprite_name}.png")
        # Load sprite
        self.image = self.get_image(0, 128)
        self.image.set_colorkey([0, 0, 0])
        self.current_image = 0
        self.images = load_player_walking_animation_images(sprite_name, sprite_type)

    def get_image(self, x, y):
        image = pygame.Surface([64, 64])
        image.blit(self.image, (0, 0), (x, y, 64, 64))
        return image

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

        # Reset animations
        if self.current_image >= len(self.images_list):
            self.current_image = 0

        # Modify current animation
        self.image = self.images_list[int(self.current_image)]
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
        self.image.set_colorkey([0, 0, 0])


def load_player_walking_animation_images(sprite_name, sprite_type):
    images = {
        "walking_left": [],
        "walking_right": [],
        "walking_up": [],
        "walking_down": [],
    }
    sprite = pygame.image.load(f"graphics/{sprite_type}/{sprite_name}.png")
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

    return images


def get_image(x, y, sprite):
    image = pygame.Surface([64, 64])
    image.blit(sprite, (0, 0), (x, y, 64, 64))
    return image
