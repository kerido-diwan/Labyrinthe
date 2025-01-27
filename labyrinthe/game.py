import itertools

import pygame
import pytmx
import pyscroll

from labyrinthe.rond_player import RondPlayer
from labyrinthe.constants import DIMENSIONS, TITRE, MAP_DIR, MAP_FILE_SUFFIX


class Game:
    def __init__(self):
        #créer la fenetre de jeu.
        self.screen = pygame.display.set_mode(DIMENSIONS)
        pygame.display.set_caption(TITRE)

        map_file_list = [file for file in MAP_DIR.iterdir() if file.suffix == MAP_FILE_SUFFIX]
        self.map_filenames_iter = itertools.cycle(map_file_list)

        # Créer le joueur et initialiser les autres attributs, puis importer la map
        self.player = RondPlayer(0, 0)
        self.walls = None
        self.group = None
        self.enter_lab_rect = None
        self.switch_lab(next(self.map_filenames_iter))


        # faire boujer jouer(l1) et animation(l2)
    def handel_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()


        if pressed[pygame.K_DOWN]:
            self.player.move_down()


        if pressed[pygame.K_LEFT]:
            self.player.move_left()


        if pressed[pygame.K_RIGHT]:
            self.player.move_right()

    def switch_lab(self, filename):
        # importer et charger la carte (carte_pygame)
        tmx_data = pytmx.util_pygame.load_pygame(filename)
        map_data = pyscroll.TiledMapData(tmx_data)  # Permet de deplacer la carte dans la fenetre
        map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, self.screen.get_size()  # Renu graphique en fonction de la taille de la fenetre avec get_size()
        )
        map_layer.zoom = 1.5

        # définir liste de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner groupe de calces
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.player)

        enter_lab = tmx_data.get_object_by_name("next_lab")
        self.enter_lab_rect = pygame.Rect(enter_lab.x, enter_lab.y, enter_lab.width, enter_lab.height)

        # spawn point
        spawn_lab_point = tmx_data.get_object_by_name("spawn_lab")
        self.player.position[0] = spawn_lab_point.x
        self.player.position[1] = spawn_lab_point.y

    def update(self):
        self.group.update()
        self.group.center(self.player.position)
        #verifier entre
        if self.player.feet.colliderect(self.enter_lab_rect):
            self.switch_lab(next(self.map_filenames_iter))

        #continuer pour les autres lab

        #verifier collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()


    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.player.save_location()
            self.handel_input()
            self.update()
            self.group.update()
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        clock.tick(30)
        pygame.quit()