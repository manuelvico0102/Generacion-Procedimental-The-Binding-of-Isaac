import pygame as pg

from src.modules.BaseClasses import BaseSprite, BaseTear, MoveSprite


class Border(BaseSprite):
    """
    Barrera invisible para paredes.

    :param x: Píxel en la pantalla.
    :param y: Píxel en la pantalla.
    :param width: ancho de la pared.
    :param height: altura de la pared.
    :param groups: grupos de sprites
    :param is_killing: si el sprite muere en caso de colisión.
    """

    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 *groups: pg.sprite.AbstractGroup,
                 is_killing: bool = False):
        BaseSprite.__init__(self, (0, 0), *groups)

        self.is_killing = is_killing
        self.image = pg.Surface((width, height), pg.SRCALPHA, 32)
        self.rect = pg.Rect(x, y, width, height)

    def collide(self, other: MoveSprite):
        if isinstance(other, BaseTear):
            other.destroy()
        if self.is_killing:
            other.kill()
        else:
            other.move_back(self.rect)

    def get_rect(self):
        return self.rect

