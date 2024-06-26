import pygame as pg

from src.utils.funcs import load_image
from src.modules.BaseClasses import BaseArtifact


class GreenSyringe(BaseArtifact):
    """
    Green Syringe.

    :param xy_pixels: Centro
    """

    image = load_image("textures/artifacts/green_syringe.png")

    mode = BaseArtifact.modes["add"]

    boosts = {
        "speed": 0.2,
        "shot_distance": 1
    }

    def __init__(self,
                 xy_pixels: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup):
        BaseArtifact.__init__(self, xy_pixels, *groups)
