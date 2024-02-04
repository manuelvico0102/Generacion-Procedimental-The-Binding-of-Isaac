import pygame as pg

from src.utils.funcs import load_image
from src.modules.BaseClasses import BaseArtifact


class RedSyringe(BaseArtifact):
    """
    Красный шприц.

    :param xy_pixels: Центр
    """

    image = load_image("textures/artifacts/red_syringe.png")

    mode = BaseArtifact.modes["add"]

    boosts = {
        "speed": 0.2
    }

    def __init__(self,
                 xy_pixels: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup):
        BaseArtifact.__init__(self, xy_pixels, *groups)
