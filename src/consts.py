from enum import Enum

import pygame as pg


class FloorsTypes(Enum):
    """
    Constantes de tipos de pisos.
    """
    BASEMENT: str = "basement"
    CAVES: str = "caves"
    CATACOMBS: str = "catacombs"
    DEPTHS: str = "depths"
    BLUEWOMB: str = "bluewomb"
    WOMB: str = "womb"


class RoomsTypes(Enum):
    """
    Constantes de tipos de habitaciones (¿cambiar a algún valor aleatorio?).
    """
    EMPTY: str = "empty"
    DEFAULT: str = "default"
    SPAWN: str = "spawn"
    TREASURE: str = "treasure"
    SHOP: str = "shop"
    SECRET: str = "secret"
    BOSS: str = "boss"


class Moves(Enum):
    """
     Posibles direcciones (x, y) (hacer suma).
     La esquina superior izquierda es el origen.
    """
    UP = (0, -1)
    DOWN = (0, 1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    TOPLEFT = (-1, -1)
    TOPRIGHT = (1, -1)
    BOTTOMRIGHT = (1, 1)
    BOTTOMLEFT = (-1, 1)


class DoorsCoords(Enum):
    """
    Posibles coordenadas de las puertas en la habitación (x, y)
    """
    UP = (6, -1)
    DOWN = (6, 7)
    RIGHT = (13, 3)
    LEFT = (-1, 3)


class FirePlacesTypes(Enum):
    """
    Tipos de fogatas.
    """
    DEFAULT = 'default'
    RED = 'red'


class HeartsTypes(Enum):
    """
    Tipos de corazones del personaje.
    """
    RED = 'red'
    BLUE = 'blue'
    BLACK = 'black'


FPS = 60                                          # O tal vez 59.98?
WIDTH, HEIGHT = 1280, 960                         # Pantalla completa
GAME_WIDTH, GAME_HEIGHT = 1280, 812               # Parte de la pantalla del juego
STATS_WIDTH, STATS_HEIGHT = 1280, 148             # Parte de la pantalla con una estadística (hp, mapa, dinero, etc.)
ROOM_WIDTH, ROOM_HEIGHT = 13, 7                   # En celdas
WALL_SIZE = 133                                   # Tamaño de la pared de la textura de la habitación (píxeles)
CELL_SIZE = 78                                    # Tamaño de la celda de la habitación (píxeles)
MINIMAP_CELL_WIDTH, MINIMAP_CELL_HEIGHT = 41, 21  # Tamaño de la celda de la minimapa (píxeles)
MINIMAP_WIDTH, MINIMAP_HEIGHT = 410, 126          # Tamaño de la minimapa (10x6)

MOVE_TO_NEXT_ROOM = pg.USEREVENT + 1              # Transición entre habitaciones
MOVE_TO_NEXT_LEVEL = pg.USEREVENT + 2             # Pasar al siguiente nivel
PICKUP_LOOT = pg.USEREVENT + 3                    # Selección de botín (bombas, monedas, llaves, etc.)
PICKUP_ART = pg.USEREVENT + 4                     # Recogida de artefactos
BUY_ITEM = pg.USEREVENT + 5                       # Compra en tienda
USE_BOMB = pg.USEREVENT + 6                       # Colocar una bomba debajo del personaje
GAME_OVER = pg.USEREVENT + 7                      # Fin del juego
GG_HURT = pg.USEREVENT + 8                        # Personaje principal herido
USE_KEY = pg.USEREVENT + 9                        # Usar una llave para abrir una puerta
DEATH_ENEMY = pg.USEREVENT + 10                   # El enemigo esta muerto
