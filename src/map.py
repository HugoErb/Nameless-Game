from dataclasses import dataclass

import pyscroll
import pytmx

from settings import *


@dataclass
class Portal:
    from_world: str
    origin_point: str
    destination_world: str
    spawn_point: str


@dataclass
class Map:
    name: str
    walls: []
    death_areas: []
    falling_areas: []
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: []


class MapManager:

    def __init__(self, screen, player):
        self.maps = {}
        self.current_map = "world"
        self.screen = screen
        self.player = player

        self.register_map("world", portals=[
            Portal(from_world="world", origin_point="enter_house", destination_world="house",
                   spawn_point="house_spawn_point")
        ])
        self.register_map("house", portals=[
            Portal(from_world="house", origin_point="exit_house", destination_world="world",
                   spawn_point="spawn_point_from_house")
        ])
        self.teleport(PLAYER_SPAWN_POINT)

    def teleport(self, object_name):
        position = self.get_object(object_name)
        self.player.position[0] = position.x
        self.player.position[1] = position.y
        self.player.save_location()

    def check_collisions(self):
        # Check for teleportation to another map
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                origin_point = self.get_object(portal.origin_point)
                rect = pygame.Rect(origin_point.x, origin_point.y, origin_point.width, origin_point.height)

            if self.player.feet.colliderect(rect):
                self.current_map = portal.destination_world
                self.teleport(portal.spawn_point)

        # Check if walking in a certain area in the current map
        for sprite in self.get_group().sprites():
            # Check for collision
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

            # Check if walking in death areas
            if sprite.feet.collidelist(self.get_death_areas()) > -1:
                sprite.die("true")
                sprite.state = "dead"

            # Check if walking in fall areas
            if sprite.feet.collidelist(self.get_falling_areas()) > -1 or sprite.state == "falling":
                sprite.state = "falling"
                sprite.fall()

    def register_map(self, map_name, portals=[]):

        # Load TMX map
        tmx_data = pytmx.util_pygame.load_pygame(f"./graphics/map/{map_name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        map_layer.zoom = MAP_ZOOM
        nb_layer = len(tmx_data.layers)
        print(nb_layer)

        # Create specials areas on the map
        walls = []
        death_areas = []
        falling_areas = []

        for obj in tmx_data.objects:
            # Create collision_areas
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            # Create death areas
            elif obj.type == "death":
                death_areas.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            # Create fall areas
            elif obj.type == "fall":
                falling_areas.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Draw layer group
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=nb_layer - 3)
        group.add(self.player)

        # Create map instance
        self.maps[map_name] = Map(map_name, walls, death_areas, falling_areas, group, tmx_data, portals)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_falling_areas(self):
        return self.get_map().falling_areas

    def get_death_areas(self):
        return self.get_map().death_areas

    def get_object(self, object_name):
        return self.get_map().tmx_data.get_object_by_name(object_name)

    def draw(self):
        self.get_group().draw(self.screen)

    def center_camera(self):
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()
