import pygame as pg
import os

from src import consts
from src.utils.graph import valid_coords, get_neighbors_coords
from src.modules.levels.Room import Room
from src.modules.levels.LevelGenerator import generate_level
from src.modules.animations.MovingRoomAnimation import MovingRoomAnimation
from src.modules.characters.parents import Player
from src.consts import RoomsTypes


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
                 height: int = 6,
                 algorithm: int = 0):
        self.floor_type = floor_type
        self.main_hero = main_hero
        self.width = width
        self.height = height
        self.level_map: list[list[consts.RoomsTypes | str]] = []
        self.rooms: list[list[Room | None]] = [[None] * width for _ in range(height)]
        self.current_room: Room | None = None
        self.is_moving: bool | MovingRoomAnimation = False

        self.setup_level(algorithm=algorithm)

    def setup_level(self, algorithm: int = 0):
        """
        Generación de cuartos de nivel y colocación de puertas.
        """
        rangeRooms = self.get_number_of_rooms(self.floor_type)
        self.level_map = generate_level(self.width, self.height, rangeRooms, algorithm)
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

    def change_all_rooms_state(self):
        for row in self.rooms:
            for room in row:
                if room:
                    room.update_detection_state(is_spotted=True, see_secret=True)

    def get_number_of_rooms(self, nivel: consts.FloorsTypes) -> tuple[int, int]:
        """
         Selección el rango del número de habitaciones que tendrá el piso por nivel.

         :param nivel: Nivel de piso.
         :return: Rango del número de habitaciones.
        """

        minRooms = 10
        maxRooms = 15

        if nivel == consts.FloorsTypes.BASEMENT:
            minRooms += 2
            maxRooms += 2
        elif nivel == consts.FloorsTypes.CAVES:
            minRooms += 4
            maxRooms += 4
        elif nivel == consts.FloorsTypes.CATACOMBS:
            minRooms += 6
            maxRooms += 6
        elif nivel == consts.FloorsTypes.DEPTHS:
            minRooms += 8
            maxRooms += 8
        elif nivel == consts.FloorsTypes.BLUEWOMB:
            minRooms += 10
            maxRooms += 10
        elif nivel == consts.FloorsTypes.WOMB:
            minRooms += 12
            maxRooms += 12
        
        return minRooms, maxRooms
    
    # constructor pasando mapa de nivel
    def constructor(self, floor_type: consts.FloorsTypes | str, main_hero: Player, level_map: list[list[consts.RoomsTypes | str]], width: int = 10, height: int = 6):
        self.floor_type = floor_type
        self.main_hero = main_hero
        self.width = width
        self.height = height
        self.level_map = level_map                     
        self.rooms: list[list[Room | None]] = [[None] * width for _ in range(height)]
        self.current_room: Room | None = None
        self.is_moving: bool | MovingRoomAnimation = False

        self.load_level_map(level_map)

    def load_level_map(self, level_map: list[list[consts.RoomsTypes | str]]):
        self.level_map = level_map
        for y, row in enumerate(self.level_map):
            for x, room_type in enumerate(row):
                if room_type == consts.RoomsTypes.EMPTY:
                    continue
                room = Room(self.floor_type, room_type, (x, y), self.main_hero, None)
                room.setup_doors(self.get_doors(x, y))
                if room_type == consts.RoomsTypes.SPAWN:
                    self.current_room = room
                    
                self.rooms[y][x] = room
        assert self.current_room is not None and self.current_room.room_type == consts.RoomsTypes.SPAWN
        self.change_rooms_state(self.current_room.x, self.current_room.y)


    def download_level_map_to_file(self, filename: str):
        directory = "mapas"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Diccionario de mapeo
        room_type_map = {
            None: "__",
            RoomsTypes.DEFAULT: "DE",
            RoomsTypes.SECRET: "SE",
            RoomsTypes.SHOP: "SH",
            RoomsTypes.BOSS: "BO",
            RoomsTypes.TREASURE: "TR",
            RoomsTypes.SPAWN: "SP"
        }

        file_path = os.path.join(directory, filename)

        with open(file_path, 'w') as file:
            for row in self.rooms:
                row_str = [room_type_map.get(room.room_type if room else None) for room in row]
                file.write(','.join(row_str) + '\n')
                

    def load_level_map_from_file(self, filename: str):

        symbol_to_room_type = {
            "__": RoomsTypes.EMPTY,
            "DE": RoomsTypes.DEFAULT,
            "SE": RoomsTypes.SECRET,
            "SH": RoomsTypes.SHOP,
            "BO": RoomsTypes.BOSS,
            "TR": RoomsTypes.TREASURE,
            "SP": RoomsTypes.SPAWN
        }

        aniadir = "mapas/"
        filename = aniadir + filename
        
        with open(filename, 'r') as file:
            level_map = []
            for line in file:
                row = line.strip().split(',')
                level_map_row = [
                    symbol_to_room_type[symbol] if symbol in symbol_to_room_type else RoomsTypes.EMPTY
                    for symbol in row
                ]
                level_map.append(level_map_row)

        self.constructor(self.floor_type, self.main_hero, level_map, self.width, self.height)
        
        
        