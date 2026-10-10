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
        # Lance uniquement l'animation si elle n'est pas terminée
        print(animation_type)
        if not self.animation_finished:
            # Réinitialise l'index de la boucle pour une nouvelle animation
            if animation_type != self.last_animation:
                self.reset_animation(animation_type)

            # Appelle la méthode spécifique en fonction du type d'animation
            if animation_type.startswith("attacking"):
                return self.animate_attacking(animation_type)
            elif animation_type == "death":
                return self.animate_death()
            elif animation_type == "fall":
                return self.animate_fall()
            else:
                return self.animate_standard(animation_type)

    def reset_animation(self, animation_type):
        """Réinitialise les paramètres d'animation pour une nouvelle animation"""
        self.last_animation = animation_type
        self.current_image = 0
        self.animation_finished = False
        self.clock = 0

    def animate_attacking(self, animation_type):
        """Animation spécifique pour les attaques"""
        self.clock += self.speed * 15
        if self.clock >= 100:
            if self.current_image + 1 < len(self.images[animation_type]):
                self.current_image += 1
            else:
                self.animation_finished = True
                print(f"L'animation {animation_type} est terminée.")
            self.clock = 0
        self.update_image(animation_type)
        return self.animation_finished

    def animate_death(self):
        """Animation spécifique pour la mort"""
        self.clock += self.speed * 8.5
        if self.clock >= 100:
            if self.current_image + 1 < len(self.images["death"]):
                self.current_image += 1
            else:
                self.animation_finished = True
                print("L'animation de mort est terminée.")
            self.clock = 0
        self.update_image("death")
        return self.animation_finished

    def animate_fall(self):
        """Animation spécifique pour la chute"""
        self.clock += self.speed * 8.5
        if self.clock >= 100:
            if self.size > 0:
                self.size -= 0.5
            else:
                self.animation_finished = True
            self.clock = 0
        self.update_image("fall")
        return self.animation_finished

    def animate_standard(self, animation_type):
        """Animation standard pour les autres actions"""
        self.clock += self.speed * 8.5
        if self.clock >= 100:
            self.current_image = (self.current_image + 1) % len(self.images[animation_type])
            self.clock = 0
        self.update_image(animation_type)
        return self.animation_finished

    def update_image(self, animation_type):
        """Met à jour l'image et applique la transformation"""
        self.image = self.images[animation_type][self.current_image]
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image.set_colorkey(0, 0)

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
