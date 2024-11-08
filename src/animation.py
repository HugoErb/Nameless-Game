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
                self.clock += self.speed * 50
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
    """
    Charge et organise les images d'animation pour un sprite donné dans des catégories spécifiques.

    Args:
        sprite_name (str): Le nom du sprite (fichier d'image sans extension).
        sprite_type (str): Le type de sprite (chemin du dossier relatif).

    Returns:
        dict: Un dictionnaire contenant des listes d'images organisées par type et direction d'animation.
    """
    # Initialisation des types d'animations et directions
    images = {key: [] for key in ["walking_left", "walking_right", "walking_up", "walking_down",
                                  "death", "fall", "attacking_left", "attacking_right",
                                  "attacking_up", "attacking_down"]}

    # Chargement de la feuille de sprite
    sprite = pygame.image.load(f"../graphics/{sprite_type}/{sprite_name}.png")

    # Mapping des directions pour la marche et l'attaque
    directions = ["up", "left", "down", "right"]

    # Chargement des images de marche
    for i, direction in enumerate(directions):
        for j in range(9):
            images[f"walking_{direction}"].append(get_image(64 * j, 512 + 64 * i, sprite))

    # Chargement des images de mort
    images["death"] = [get_image(64 * i, 1280, sprite) for i in range(6)]

    # Chargement des images de chute
    images["fall"] = [get_image(320 + 64 * i, 128, sprite) for i in range(2)]

    # Chargement des images d'attaque
    for i, direction in enumerate(directions):
        for j in range(6):
            images[f"attacking_{direction}"].append(get_image(64 * j, 768 + 64 * i, sprite))

    return images


def get_image(x, y, sprite):
    """
    Extrait une image de 64x64 pixels à partir de la feuille de sprite.

    Args:
        x (int): La coordonnée x du coin supérieur gauche de l'image dans la feuille de sprite.
        y (int): La coordonnée y du coin supérieur gauche de l'image dans la feuille de sprite.
        sprite (pygame.Surface): La feuille de sprite à partir de laquelle extraire l'image.

    Returns:
        pygame.Surface: Une surface Pygame contenant l'image extraite de 64x64 pixels.
    """
    # Créer une surface optimisée avec le même format que la feuille de sprite pour un meilleur rendu
    image = sprite.subsurface((x, y, 64, 64)).copy()
    return image
