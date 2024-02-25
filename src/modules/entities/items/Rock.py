import random

import pygame as pg

from src.utils.funcs import load_image, load_sound
from src.consts import FloorsTypes, RoomsTypes, CELL_SIZE
from src.modules.BaseClasses import BaseItem


class Rock(BaseItem):
    """
    Clase de la roca.

    :param xy_pos: Posición en la habitación.
    :param floor_type: Tipo de piso.
    :param room_type: Tipo de habitación.
    :param collidable_group: Grupo de sprites donde todos los sprites son obstáculos.
    :param *groups: Otros grupos de sprites.
    :param collidable: Si se puede chocar con el objeto (si es impenetrable).
    :param hurtable: Si causa daño al tocarlo.
    """
    rocks: pg.Surface = load_image("textures/room/rocks.png")
    destroy_frames: pg.Surface = None
    rock_crumble: list[pg.mixer.Sound] = [
        load_sound("sounds/rock_crumble1.wav"),
        load_sound("sounds/rock_crumble2.wav"),
        load_sound("sounds/rock_crumble3.wav"),
    ]

    def __init__(self,
                 xy_pos: tuple[int, int],
                 floor_type: FloorsTypes | str,
                 room_type: RoomsTypes | str,
                 collidable_group: pg.sprite.AbstractGroup,
                 *groups: pg.sprite.AbstractGroup,
                 collidable: bool = True,
                 hurtable: bool = False):
        BaseItem.__init__(self, xy_pos, collidable_group, *groups, collidable=collidable, hurtable=hurtable)

        self.collidable_group = collidable_group
        self.floor_type = floor_type
        self.room_type = room_type
        self.with_treasure = False

        self.destroyed_image = pg.Surface((0, 0))
        self.set_image()
        self.set_rect()

    def set_image(self):
        texture_x = 0
        texture_y = random.choices(list(range(1, 5)), [0.333, 0.333, 0.333, 0.001])[0] * CELL_SIZE
        self.with_treasure = texture_y == CELL_SIZE * 4
        for i, floor_type in enumerate(FloorsTypes):
            if floor_type == self.floor_type:
                texture_x = i * CELL_SIZE
                break
        else:
            if self.room_type == RoomsTypes.SECRET:
                texture_x = len(FloorsTypes) * CELL_SIZE

        self.image = Rock.rocks.subsurface((texture_x, texture_y, CELL_SIZE, CELL_SIZE))
        self.destroyed_image = Rock.rocks.subsurface((texture_x, 0, CELL_SIZE, CELL_SIZE))

    def blow(self):
        """
        Explosión/destrucción de la roca.
        """
        self.destroy()

    def destroy(self):
        """
        Destrucción de la roca después de la explosión.
        """
        if not self.collidable:
            return
        self.collidable = False
        self.hurtable = False
        self.image = self.destroyed_image
        self.collidable_group.remove(self)
        random.choice(Rock.rock_crumble).play()
        self.destroy_animation()
        if self.with_treasure:
            self.drop_something()

    def drop_something(self):
        """
        Drop de objetos después de romperse.
        """
        pass

    def destroy_animation(self):
        pass
        # Partículas dispersas que se eliminarán al volver a entrar en la habitación
        # SingleAnimation(Rock.destroy_frames)
