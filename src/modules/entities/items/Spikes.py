import pygame as pg

from src.consts import CELL_SIZE
from src.utils.funcs import load_image
from src.modules.BaseClasses import BaseItem, MoveSprite


class Spikes(BaseItem):
    """
    Spikes en el suelo. Pueden causar daño.

    :param xy_pos: Posición en la habitación.
    :param groups: Grupos de sprites.
    :param hiding_delay: Retraso antes de ocultarse en el suelo. 0 - no se oculta.
    :param hiding_time: Cuánto tiempo se oculta en el suelo. 0 - para siempre.
    :param hurtable: Causa daño o no.
    """

    images: list[pg.Surface] = [
        load_image("textures/room/spikes.png").subsurface(
            x * CELL_SIZE, 0, CELL_SIZE, CELL_SIZE
        )
        for x in range(5)
    ]

    def __init__(self,
                 xy_pos: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup,
                 hiding_delay: int | float = 0,
                 hiding_time: int | float = 0):
        hurtable = True
        BaseItem.__init__(self, xy_pos, *groups, hurtable=hurtable)

        self.hiding_delay = hiding_delay
        self.hiding_time = hiding_time
        self.ticks = 0

        self.set_image()
        self.set_rect()

    def set_image(self):
        self.image = Spikes.images[0]

    def set_rect(self, width: int = None, height: int = None, up: int = 0, left: int = 0):
        BaseItem.set_rect(self, width, height)
        # Intentar reducir el Rect de los pinchos para evitar daños en los bordes (¿reducir la textura?)

    def hide(self, forever: bool = False):
        """
        Oculta los pinchos.

        :param forever: Indica si es de forma permanente.
        """
        # ¡Realizar animación y sonido?
        self.hurtable = False
        self.image = Spikes.images[-1]
        if forever:
            self.hiding_time = 0

    def unhide(self):
        """
        Mostrar los pinchos.
        """
        # ¡Realizar animación y sonido?
        self.hurtable = True
        self.image = Spikes.images[1]

    def update(self, delta_t: float):
        if not self.hiding_delay:
            return
        self.ticks += delta_t
        if self.ticks >= self.hiding_delay and self.hurtable:
            self.ticks = 0
            self.hide()
        if self.ticks >= self.hiding_time and not self.hurtable and self.hiding_time:
            self.ticks = 0
            self.unhide()

    def collide(self, other: MoveSprite):
        # ¡Realizar animación y sonido?
        if isinstance(other, (MoveSprite,)):
            BaseItem.collide(self, other)

