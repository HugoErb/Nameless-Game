import pygame


class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, sprite_name, sprite_type):
        super().__init__()
        self.image = pygame.image.load(f"graphics/{sprite_type}/{sprite_name}.png")
        # Load sprite
        self.image = self.get_image(0, 128)
        self.image.set_colorkey([0, 0, 0])

    def get_image(self, x, y):
        image = pygame.Surface([64, 64])
        image.blit(self.image, (0, 0), (x, y, 64, 64))
        return image


def load_animation_images(sprite_name, sprite_type):
    images = []
    sprite = f"graphics/{sprite_type}/{sprite_name}.png"
    for i in range(0, 3):
        for j in range(0, 8):
            images.append(get_image((64 * j), (512 + 64 * i), sprite))


def get_image(x, y, sprite):
    image = pygame.Surface([64, 64])
    image.blit(self.sprite_sheet, (0, 0), (x, y, 64, 64))
    return image
