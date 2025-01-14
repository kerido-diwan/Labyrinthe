import pygame


class Rond_player:
    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load("Red_circle.png")
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.old_position = self.position.copy() #garder la position
        self.speed = 0.40  # vitesse du mouvement

    def save_lacation(self):
        self.old_position = self.old_position
    #définir les mouvements
    def move_up(self): self.position[0] -= self.speed

    def move_down(self): self.position[0] += self.speed

    def move_right(self): self.position[1] += self.speed

    def move_left(self): selectors.PollSelector[1] -= self.speed