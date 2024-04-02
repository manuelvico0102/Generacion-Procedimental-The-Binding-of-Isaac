import random

import pygame as pg

from src.consts import CELL_SIZE
from src.utils.funcs import load_image
from src.modules.BaseClasses import BaseItem, MovingEnemy, MovableItem, MoveSprite
from src.modules.characters.parents import Player


class Web(BaseItem):
    """
    Clase de la telaraña que ralentiza.

    :param xy_pos: Posición en la habitación.
    :param groups: Grupos de sprites.
    :param colliadble: Indica si es colisionable.
    """

    webs: list[pg.Surface] = [load_image("textures/room/web.png").subsurface(x * CELL_SIZE, 0, CELL_SIZE, CELL_SIZE)
                              for x in range(3)]
    destoryed: pg.Surface = load_image("textures/room/web.png").subsurface(3 * CELL_SIZE, 0, CELL_SIZE, CELL_SIZE)

    slowdown_coef = 3/4
    clear_collides_delay = 1

    def __init__(self,
                 xy_pos: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup,
                 colliadble: bool = True):
        BaseItem.__init__(self, xy_pos, *groups, collidable=colliadble)

        self.collide_sprites: list[MoveSprite] = []
        self.ticks = 0

        self.set_image()
        self.set_rect()

    def set_image(self):
        self.image = random.choice(Web.webs)

    def blow(self):
        """
        Explosión (destrucción) de la telaraña.
        """
        self.collidable = False
        self.image = Web.destoryed
        self.reset_collides_sprites()

    def update(self, delta_t: float):
        self.ticks += delta_t
        if self.ticks >= Web.clear_collides_delay:
            self.ticks = 0
            self.reset_collides_sprites()

    def reset_collides_sprites(self):
        """
        Reinicia la lista de colisiones y restablece el coeficiente de velocidad.
        """
        for sprite in self.collide_sprites:
            sprite: MoveSprite
            sprite.slowdown_coef = 1
        self.collide_sprites.clear()

    def collide(self, other: MoveSprite):
        # Cambiar MovingEnemy por MainCharacter o simplemente agregar MainCharacter?
        # Funciona mejor ahora porque hay un coeficiente, pero se elimina con retraso,
        # se puede reducir Web.clear_collides_delay.
        if self.collidable and isinstance(other, (MovingEnemy, MovableItem, Player)):
            if other not in self.collide_sprites:
                self.collide_sprites.append(other)
                other.slowdown_coef = Web.slowdown_coef
