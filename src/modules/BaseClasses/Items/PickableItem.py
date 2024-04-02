import pygame as pg

from src.consts import PICKUP_LOOT
from src.modules.BaseClasses.Items.BaseItem import BaseItem
from src.modules.BaseClasses.Based.MoveSprite import MoveSprite
from src.modules.characters.parents import Player


class PickableItem(BaseItem):
    """
    Clase para representar un objeto que puede ser recogido.

    :param xy_pos: Posición en la habitación.
    :param groups: Grupos de sprites.
    :param collidable: Indica si el objeto es colisionable.
    """

    def __init__(self,
                 xy_pos: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup,
                 collidable: bool = False):
        BaseItem.__init__(self, xy_pos, *groups, collidable=collidable)

        self.pick_sound: pg.mixer.Sound | None = None
        self.count: int = 1

    def collide(self, other: MoveSprite) -> bool:
        """
        Procesamiento de colisiones.

        :param other: El objeto con el que hubo colisión.
        :return: Si hubo colisión o no.
        """
        if not BaseItem.collide(self, other):
            return False

        # Reemplazar MovingEnemy por MainCharacter
        if isinstance(other, Player):
            self.pickup()

        return True

    def kill(self):
        if isinstance(self.pick_sound, pg.mixer.Sound):
            self.pick_sound.play()
        MoveSprite.kill(self)

    def pickup(self):
        """
        Recoger el objeto.
        En la clase heredada, se debe realizar pg.event.post(PICKUP_LOOT).
        """
        pg.event.post(pg.event.Event(PICKUP_LOOT, {
                                                  'item': self,
                                                  'count': self.count,
                                                  'self': self
                                                  }
                                     )
                      )
