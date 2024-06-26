import pygame as pg

from src.modules.BaseClasses.Items.BaseItem import BaseItem
from src.modules.BaseClasses.Based.BaseSprite import BaseSprite
from src.modules.BaseClasses.Based.MoveSprite import MoveSprite


class MovableItem(BaseItem, MoveSprite):
    """
    Clase de objeto móvil.

    :param xy_pos: Posición en la habitación.
    :param collide_groups: Grupos de sprites con los que no se puede colisionar.
    :param groups: Grupos de sprites.
    :param acceleration: Aceleración de frenado en celdas/segundo.
    :param xy_pixels: Posición en píxeles.
    """

    clear_collide_delay = 1

    def __init__(self,
                 xy_pos: tuple[int, int],
                 collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup,
                 acceleration: int | float = 1,
                 xy_pixels: tuple[int, int] = None):
        BaseItem.__init__(self, xy_pos, *groups, collidable=False)
        MoveSprite.__init__(self, xy_pos, collide_groups, *groups, acceleration=acceleration, xy_pixels=xy_pixels)

        self.collide_sprites: list[BaseSprite] = []
        self.clear_collide_ticks = 0

    def update(self, delta_t: float):
        self.move(delta_t)
        self.clear_collide_ticks += delta_t
        if self.clear_collide_ticks >= MovableItem.clear_collide_delay:
            self.clear_collide_ticks = 0
            self.collide_sprites.clear()

    def move(self, delta_t: float, use_a: bool = True):
        """
        Mover el objeto y cambiar su velocidad.

        :param delta_t: Tiempo desde el último fotograma.
        :param use_a: Utilizar aceleración para desacelerar.
        """
        MoveSprite.move(self, delta_t, use_a=use_a)
        MoveSprite.check_collides(self)

    def move_back(self, rect: pg.Rect):
        """
        Procesamiento de colisiones y cambio de velocidades en caso de colisión.

        :param rect: Rectángulo con el que hubo colisión.
        """
        MoveSprite.move_back(self, rect)

        centerx, centery = rect.center
        if self.rect.centerx < centerx and self.vx > 0:
            self.vx = 0
        if self.rect.centerx > centerx and self.vx < 0:
            self.vx = 0
        if self.rect.centery > centery and self.vy < 0:
            self.vy = 0
        if self.rect.centery < centery and self.vy > 0:
            self.vy = 0

    def collide(self, other: MoveSprite) -> bool:
        """
        No está garantizado que funcione correctamente :)
        Por ahora es muy primitivo, sí

        :return: Si hubo cambios en las velocidades.
        """
        if not BaseItem.collide(self, other):
            return False

        if other not in self.collide_sprites:
            self.collide_sprites.append(other)
            vx = 1 if self.rect.centerx - other.rect.centerx > 0 else -1
            vy = 1 if self.rect.centery - other.rect.centery > 0 else -1
            self.set_speed(self.vx + vx, self.vy + vy)

        return True
