import pygame as pg


from src.modules.BaseClasses.Based.BaseSprite import BaseSprite
from src.modules.BaseClasses.Based.BaseTear import BaseTear
from src.modules.BaseClasses.Based.MoveSprite import MoveSprite


class BaseItem(BaseSprite):
    """
    Clase base para los objetos (piedra, caca, llave, moneda, artefacto, etc.).

    :param xy_pos: Posición en la habitación.
    :param groups: Todos los grupos a los que pertenece el objeto-sprite.
    :param collidable: Indica si se puede colisionar con el objeto (si es impenetrable).
    :param hurtable: Indica si causa daño al personaje al tocarlo.
    """

    def __init__(self,
                 xy_pos: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup,
                 collidable: bool = False,
                 hurtable: bool = False):
        BaseSprite.__init__(self, xy_pos, *groups)

        self.groups = groups
        self.x, self.y = xy_pos
        self.collidable = collidable
        self.hurtable = hurtable

        self.image: pg.Surface
        self.rect: pg.Rect
        self.hp = 0
        self.vx = 0
        self.vy = 0

    def collide(self, other: MoveSprite) -> bool:
        """
        Procesamiento de la colisión con una entidad.

        :param other: Objeto con el que se produjo la colisión (personaje, lágrima, explosión de bomba).
        :return: Si se produjo o no la colisión.
        """
        if not BaseSprite.collide(self, other):
            return False

        if self.collidable:
            other.move_back(self.rect)
            if isinstance(other, BaseTear):
                other.destroy()
        if self.hurtable:
            other.hurt(1)

        return True

    def destroy(self, *args, **kwargs):
        """
        Destrucción/Eliminación de la entidad.
        """
        pass
        # self.kill()
