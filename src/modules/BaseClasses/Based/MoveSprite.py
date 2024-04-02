import pygame as pg

from src.consts import CELL_SIZE
from src.modules.BaseClasses.Based.BaseSprite import BaseSprite
from src.utils.funcs import cell_to_pixels


class MoveSprite(BaseSprite):
    """
    Sprite que se moverá al 100%.

    :param xy_pos: Posición en la habitación.
    :param collide_groups: Grupos de sprites con los que no se puede colisionar.
    :param groups: Grupos de sprites.
    :param acceleration: Aceleración de frenado en celdas/segundo.
    :param xy_pixels: Posición en píxeles.
    """

    def __init__(self,
                 xy_pos: tuple[int, int],
                 collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup,
                 acceleration: int | float = 1,
                 xy_pixels: tuple[int, int] = None):
        BaseSprite.__init__(self, xy_pos, *groups)

        self.collide_groups = collide_groups
        self.a = acceleration
        if xy_pixels:
            self.x_center, self.y_center = xy_pixels
        else:
            self.x_center, self.y_center = cell_to_pixels(xy_pos)
        self.x_center_last, self.y_center_last = self.x_center, self.y_center

        self.slowdown_coef: float = 1.0
        self.vx, self.vy = 0, 0

    def set_rect(self, width: int = None, height: int = None, up: int = 0, left: int = 0):
        """
        Establece el objeto en el centro de su celda.
        """
        BaseSprite.set_rect(self, width, height, up, left)
        if (self.x_center, self.y_center) != cell_to_pixels((self.x, self.y)):
            self.rect.center = (self.x_center, self.y_center)

    def move(self, delta_t: float, use_a: bool = True):
        """
        Movimiento de la entidad.

        :param delta_t: Tiempo desde el último fotograma.
        :param use_a: Indica si se debe aplicar aceleración/frenado al personaje.
        """
        if self.a and use_a:
            if self.vx:
                if self.vx < 0:
                    self.vx = min((0, self.vx + self.a * delta_t))
                else:
                    self.vx = max((0, self.vx - self.a * delta_t))
            if self.vy:
                if self.vy < 0:
                    self.vy = min((0, self.vy + self.a * delta_t))
                else:
                    self.vy = max((0, self.vy - self.a * delta_t))

        self.x_center_last, self.y_center_last = self.x_center, self.y_center
        self.x_center += self.vx * CELL_SIZE * self.slowdown_coef * delta_t
        self.y_center += self.vy * CELL_SIZE * self.slowdown_coef * delta_t
        self.rect.center = self.x_center, self.y_center

    def check_collides(self):
        for group in self.collide_groups:
            if sprites := pg.sprite.spritecollide(self, group, False):
                for sprite in sprites:
                    if sprite != self:
                        sprite: BaseSprite
                        sprite.collide(self)

    def move_back(self, rect: pg.Rect):
        """
        Manejo de colisión (retroceso)

        :param rect: Rectángulo de la colisión.
        """
        # ¿Cómo podemos hacer que el objeto rebote en el borde en lugar de volver a la posición anterior?

        self.x_center, self.y_center = self.x_center_last, self.y_center_last
        self.rect.center = self.x_center, self.y_center

    def set_speed(self, vx: int | float, vy: int | float):
        """
        Establece la velocidad de movimiento.

        :param vx: Velocidad horizontal en celdas/segundo.
        :param vy: Velocidad vertical en celdas/segundo.
        """
        self.vx = vx
        self.vy = vy
