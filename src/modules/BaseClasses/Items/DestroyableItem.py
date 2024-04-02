import pygame as pg

from src.modules.BaseClasses.Items.BaseItem import BaseItem
from src.modules.BaseClasses.Based.BaseTear import BaseTear
from src.modules.BaseClasses.Based.MoveSprite import MoveSprite


class DestroyableItem(BaseItem):
    """
    Objeto destruible por lágrimas y bombas.

    :param xy_pos: Posición en la habitación.
    :param groups: Grupos de sprites.
    :param collidable: ¿Obstaculiza el paso a través de sí mismo (impenetrable)?
    :param hurtable: ¿Inflige daño al tocarlo?
    """

    def __init__(self,
                 xy_pos: tuple[int, int],
                 *groups: pg.sprite.Group,
                 collidable: bool = False,
                 hurtable: bool = False):
        BaseItem.__init__(self, xy_pos, *groups, collidable=collidable, hurtable=hurtable)

        self.is_alive = True

    def collide(self, other: MoveSprite) -> bool:
        """
        Manejo de colisiones de colisiones.
        :param other: El objeto con el que colisionó.
        :return: Si hubo colisión o no.
        """
        if not self.is_alive or not BaseItem.collide(self, other):
            return False

        if isinstance(other, BaseTear):
            self.hurt(other.damage)
            if not self.collidable:
                other.destroy()

        return True

    def destroy(self):
        """
        Destruye el objeto, dejando caer el botín si es necesario y desactivando la colisión y el daño.
        """
        self.collidable = False
        self.hurtable = False
        self.is_alive = False
        self.drop_loot()

    def drop_loot(self):
        """
        Lanzar botín después de romperse.
        """
        pass

    def blow(self):
        """
        Explosión del objeto.
        """
        self.hurt(self.hp)

    def hurt(self, damage: int) -> bool:
        """
        Recibir daño.
        :param damage: Cantidad de daño.
        :return: Si se ha recibido daño o no.
        """
        if not self.is_alive:
            return False

        self.hp = max(0, self.hp - damage)

        return True
