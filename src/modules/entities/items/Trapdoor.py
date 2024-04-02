import pygame as pg

from src.modules.BaseClasses import BaseItem, MoveSprite
from src.consts import CELL_SIZE, ROOM_WIDTH, ROOM_HEIGHT, MOVE_TO_NEXT_LEVEL
from src.utils.funcs import load_image, crop, load_sound
from src.modules.characters.parents import Player

DOOR_CELL_SIZE = int(CELL_SIZE * 1.75)  # Tamaño de la celda de la puerta (ancho).


class Trapdoor(BaseItem):
    """
    Clase de la trampilla en el suelo. Su padre es la habitación del jefe.

    :param xy_pos: Posición en la habitación.
    :param groups: Todos los grupos a los que pertenece el objeto-sprite.
    :param collidable: Indica si la trampilla está abierta.
    """

    trapdoor_close = crop(load_image("textures/room/doors.png").subsurface(9 * DOOR_CELL_SIZE, 0,
                                                                           DOOR_CELL_SIZE, DOOR_CELL_SIZE))
    trapdoor_open = crop(load_image("textures/room/doors.png").subsurface(9 * DOOR_CELL_SIZE, DOOR_CELL_SIZE,
                                                                          DOOR_CELL_SIZE, DOOR_CELL_SIZE))
    open_sound = load_sound("sounds/boss_defeated.mp3")

    def __init__(self,
                 *groups: pg.sprite.AbstractGroup,
                 collidable: bool = False):
        BaseItem.__init__(self, (ROOM_WIDTH // 2, ROOM_HEIGHT // 2), *groups, collidable=collidable)

        self.set_image()
        self.set_rect()

        if self.collidable:
            self.open()

    def set_image(self):
        self.image = Trapdoor.trapdoor_close

    def open(self, with_sound: bool = False):
        self.image = Trapdoor.trapdoor_open
        self.collidable = True
        if with_sound:
            Trapdoor.open_sound.play()

    def collide(self, other: MoveSprite):
        if not isinstance(other, Player):
            return

        if self.collidable:
            pg.event.post(pg.event.Event(MOVE_TO_NEXT_LEVEL))
