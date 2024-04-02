import pygame as pg

from src import consts
from src.utils.graph import valid_coords, get_neighbors_coords
from src.modules.levels.Room import Room
from src.modules.levels.LevelGenerator import generate_level
from src.modules.animations.MovingRoomAnimation import MovingRoomAnimation
from src.modules.characters.parents import Player


class Level:
    """
     Nivel/clase de suelo.

     :param Floor_type: Tipo de piso.
     :param main_hero: Personaje principal.
     :param width: ancho máximo de la disposición de la habitación.
     :param height: altura máxima de la disposición de la habitación.
     """
    def __init__(self,
                 floor_type: consts.FloorsTypes | str,
                 main_hero: Player,
                 width: int = 10,
                 height: int = 6):
        self.floor_type = floor_type
        self.main_hero = main_hero
        self.width = width
        self.height = height
        self.level_map: list[list[consts.RoomsTypes | str]] = []
        self.rooms: list[list[Room | None]] = [[None] * width for _ in range(height)]
        self.current_room: Room | None = None
        self.is_moving: bool | MovingRoomAnimation = False

        self.setup_level()

    def setup_level(self):
        """
        Generación de cuartos de nivel y colocación de puertas.
        """
        self.level_map = generate_level(self.width, self.height, 15)
        for y, row in enumerate(self.level_map):
            for x, room_type in enumerate(row):
                if room_type == consts.RoomsTypes.EMPTY:
                    continue
                room = Room(self.floor_type, room_type, (x, y), self.main_hero, None)
                room.setup_doors(self.get_doors(x, y))
                if room_type == consts.RoomsTypes.SPAWN:
                    self.current_room = room

                    # self.main_hero.update_room_groups(self.current_room.get_room_groups())

                # room.update_doors('blow')
                # room.update_doors('open')
                # room.update_doors('close')
                self.rooms[y][x] = room
        assert self.current_room is not None and self.current_room.room_type == consts.RoomsTypes.SPAWN
        self.change_rooms_state(self.current_room.x, self.current_room.y)

    def get_doors(self, cur_x: int, cur_y: int) -> list[tuple[consts.DoorsCoords, consts.RoomsTypes]]:
        """
         Obtención de las coordenadas de las puertas y la información necesaria para la instalación de la textura.

         :param cur_x: Coordenada de la habitación actual.
         :param cur_y: Coordenada de la habitación actual.
         :return: Hoja con pares (coordenadas, tipo de habitación).
         """
        coords = get_neighbors_coords(cur_x, cur_y, self.level_map)
        doors = []
        for room_x, room_y in coords:
            direction = None
            if room_x > cur_x:
                direction = consts.DoorsCoords.RIGHT
            elif room_x < cur_x:
                direction = consts.DoorsCoords.LEFT
            elif room_y > cur_y:
                direction = consts.DoorsCoords.DOWN
            elif room_y < cur_y:
                direction = consts.DoorsCoords.UP
            assert direction is not None, f'No se pudo obtener la ubicación de la puerta'

            if (self.level_map[cur_y][cur_x] in (consts.RoomsTypes.TREASURE, consts.RoomsTypes.BOSS,
                                                 consts.RoomsTypes.SECRET, consts.RoomsTypes.SHOP)
                    and self.level_map[room_y][room_x] != consts.RoomsTypes.SECRET):
                doors.append((direction, self.level_map[cur_y][cur_x]))
            else:
                doors.append((direction, self.level_map[room_y][room_x]))

        return doors

    def get_rooms(self) -> list[list[Room | None]]:
        """
         Recuperar todas las habitaciones de un piso como una matriz bidimensional.
        """
        return self.rooms

    def change_rooms_state(self, cur_x: int, cur_y: int):
        """
         Cambia el estado de visibilidad de las habitaciones actuales y vecinas.

         :param cur_x: Coordenada de la habitación actual.
         :param cur_y: Coordenada de la habitación actual.
        """
        self.rooms[cur_y][cur_x].update_detection_state(is_active=True)
        coords = get_neighbors_coords(cur_x, cur_y, self.level_map)
        for x, y in coords:
            self.rooms[y][x].update_detection_state(is_spotted=True)

        if self.current_room.room_type == consts.RoomsTypes.SECRET:
            self.current_room.update_doors("blow", with_sound=False)

    def move_to_next_room(self, direction: consts.Moves):
        """
         Entrada a otra habitación.

         :param direction: Dirección del movimiento.
        """
        x, y = direction.value
        x, y = self.current_room.x + x, self.current_room.y + y

        if valid_coords(x, y, self.width, self.height) and self.rooms[y][x]:

            self.is_moving = True
            from_room = self.current_room
            to_room = self.rooms[y][x]
            self.moving_room_animation(from_room, to_room, direction)
########################
            # self.main_hero.update_room_groups(self.current_room.get_room_groups())
########################
            self.current_room = self.rooms[y][x]
            self.current_room.update_detection_state(is_active=True)

            self.change_rooms_state(x, y)

    def moving_room_animation(self, from_room: Room, to_room: Room, direction: consts.Moves):
        """
         Iniciar animación de transición entre habitaciones.

         :param from_room: Desde qué habitación.
         :param to_room: Qué habitación.
         :param direction: Dirección.
         """
        self.is_moving = MovingRoomAnimation(from_room, to_room, direction)

    def update_main_hero_collide_groups(self):
        self.main_hero.update_room_groups(*self.current_room.get_room_groups())

    def update(self, delta_t: float):
        if self.is_moving:
            self.is_moving.update(delta_t)
            if self.is_moving.is_over:
                self.is_moving = False
        else:
            self.current_room.update(delta_t)

    def render(self, screen: pg.Surface):
        if self.is_moving:
            self.is_moving.render(screen)
        else:
            self.current_room.render(screen)
