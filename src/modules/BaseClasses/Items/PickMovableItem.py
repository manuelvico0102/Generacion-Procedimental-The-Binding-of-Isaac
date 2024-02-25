import pygame as pg

from src.modules.BaseClasses.Items.PickableItem import PickableItem
from src.modules.BaseClasses.Items.MovableItem import MovableItem


class PickMovableItem(PickableItem, MovableItem):
    """
    Objeto recogible y movible.

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
        PickableItem.__init__(self, xy_pos, *groups)
        MovableItem.__init__(self, xy_pos, collide_groups, *groups,
                             acceleration=acceleration, xy_pixels=xy_pixels)

    def update(self, delta_t: float):
        PickableItem.update(self, delta_t)
        MovableItem.update(self, delta_t)

    def collide(self, other: MovableItem) -> bool:
        """
        Procesamiento de colisiones.

        :param other: Con quién hubo colisión.
        :return: Si hubo colisión o no.
        """
        return bool(PickableItem.collide(self, other) + MovableItem.collide(self, other))
