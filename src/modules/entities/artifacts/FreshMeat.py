import pygame as pg

from src.utils.funcs import load_image
from src.modules.BaseClasses import BaseArtifact


class FreshMeat(BaseArtifact):
    """
    FreshMeat.

    :param xy_pixels: Centro
    """

    image = load_image("textures/artifacts/fresh_meat.png")

    mode = BaseArtifact.modes["add"]  # Método de aplicación a un item (suma o multiplicación).

    boosts = {
        "max_hp": 1,
        "heal_hp": 1,
    }

    def __init__(self,
                 xy_pixels: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup):
        BaseArtifact.__init__(self, xy_pixels, *groups)
