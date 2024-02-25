import pygame as pg

from src.modules.BaseClasses import PickMovableItem
from src.utils.funcs import load_image, load_sound, crop


class PickBomb(PickMovableItem):
    """
    Bomba recogible.

    :param xy_pos: Posición en la habitación.
    :param main_hero: Héroe principal.
    :param collide_groups: Grupos de sprites a los que no se puede atravesar.
    :param groups: Grupos de sprites.
    :param xy_pixels: Posición en píxeles.
    """

    bomb = crop(load_image("textures/room/bomb.png").subsurface(48, 0, 48, 48))
    pickup_sound = load_sound("sounds/bomb_pickup.wav")

    def __init__(self,
                 xy_pos: tuple[int, int],
                 collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup,
                 xy_pixels: tuple[int, int] = None):
        PickMovableItem.__init__(self, xy_pos, collide_groups, *groups, xy_pixels=xy_pixels)

        self.count = 1

        self.set_image()
        self.set_rect()

    def set_image(self):
        self.image = PickBomb.bomb
        self.pick_sound = PickBomb.pickup_sound
