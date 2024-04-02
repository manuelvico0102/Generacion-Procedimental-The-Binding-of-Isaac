import inspect
import random
from typing import Type

import pygame as pg

from src.modules.BaseClasses.Based.MoveSprite import MoveSprite
from src.modules.BaseClasses.Items.BaseArtifact import BaseArtifact
from src.modules.BaseClasses.Items.PickableItem import PickableItem
from src.modules.Banners.ShopFont import ShopFont
from src.consts import BUY_ITEM


class ShopItem(PickableItem):
    """
    Clase de un objeto que se puede comprar en la tienda.

    :param xy_pos: Posición en la habitación.
    :param item: Objeto que se vende.
    :param groups: Grupos de sprites.
    :param price: Precio del objeto.
    """

    def __init__(self,
                 xy_pos: tuple[int, int],
                 item: Type[PickableItem] | Type[BaseArtifact],
                 *groups: pg.sprite.AbstractGroup,
                 price: int = None):
        PickableItem.__init__(self, xy_pos, *groups, collidable=True)

        assert inspect.isclass(item)

        self.item = item((0, 0), pg.sprite.Group())
        self.font = ShopFont()
        self.event_rect = self.item.rect.copy()

        if price:
            self.price = price
        else:
            if isinstance(self.item, BaseArtifact):
                self.price = 15
            else:
                self.price = random.choice([3, 5, 7, 10, 15])

        self.set_image()
        self.set_rect()
        self.event_rect.center = self.rect.center

    def set_image(self):
        banner = self.font.write_text(f'{self.price}c')
        width = max(self.item.image.get_width(), banner.get_width())
        height = self.item.image.get_height() + banner.get_height()
        self.image = pg.Surface((width, height), pg.SRCALPHA, 32)
        self.image.blit(self.item.image, (
            (width - self.item.image.get_width()) // 2,
            0
        ))
        self.image.blit(banner, (
            (width - banner.get_width()),
            (height - banner.get_height())
        ))

    def collide(self, other: MoveSprite):
        """
        Procesamiento de colisiones.

        :param other: Con quién hubo colisión.
        :return: Si hubo colisión o no.
        """
        if not pg.Rect.colliderect(self.event_rect, other.rect):
            return
        PickableItem.collide(self, other)

    def kill(self):
        PickableItem.kill(self)
        self.item.kill()

    def pickup(self):
        """
        Recoger (comprar) el objeto.
        """
        pg.event.post(pg.event.Event(BUY_ITEM, {
                                                 'item': self.item,
                                                 'count': self.count,
                                                 'heart_type': getattr(self.item, 'heart_type', None),
                                                 'price': self.price,
                                                 'self': self
                                                 }
                                     )
                      )

