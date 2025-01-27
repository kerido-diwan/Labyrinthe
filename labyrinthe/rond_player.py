import pygame

from labyrinthe.constants import PLAYER_SKIN_DIMENSIONS

class RondPlayer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load("assets/red_circle.png")
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 5)
        self.old_position = self.position.copy() #garder la position
        self.speed = 0.20  # vitesse du mouvement

    def save_location(self):
        self.old_position = self.position.copy()

    #définir les mouvements
    def move_up(self):
        self.position[1] -= self.speed

    def move_down(self):
        self.position[1] += self.speed

    def move_right(self):
        self.position[0] += self.speed

    def move_left(self):
        self.position[0] -= self.speed

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        image = pygame.Surface(PLAYER_SKIN_DIMENSIONS)
        image.blit(self.sprite_sheet, (0, 0), (x, y, PLAYER_SKIN_DIMENSIONS[0], PLAYER_SKIN_DIMENSIONS[1]))
        return image

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom