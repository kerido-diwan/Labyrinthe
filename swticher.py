def switch_lab(self, filename):
    # importer et charger la carte (carte_pygame)
    tmx_data = pytmx.util_pygame.load_pygame(filename)
    map_data = pyscroll.TiledMapData(tmx_data)  # Permet de deplacer la carte dans la fenetre
    map_layer = pyscroll.orthographic.BufferedRenderer(
        map_data, self.screen.get_size() # Renu graphique en fonction de la taille de la fenetre avec get_size()
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