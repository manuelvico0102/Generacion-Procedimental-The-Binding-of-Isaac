import random

import pygame as pg

from src.consts import CELL_SIZE
from src.utils.funcs import load_image, load_sound
from src.modules.BaseClasses import DestroyableItem


class Poop(DestroyableItem):
    """
    Clase Poop.

    :param xy_pos: Posición en la habitación.
    :param *groups: Otros grupos de sprites.
    :param collidable: Indica si se puede colisionar con el objeto (si es atravesable o no).
    """

    poops: pg.Surface = load_image("textures/room/poops.png")
    poop_destoryed = [load_sound("sounds/pop1.wav"), load_sound("sounds/pop2.mp3")]

    max_hp = 10

    def __init__(self,
                 xy_pos: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup,
                 collidable: bool = True):
        DestroyableItem.__init__(self, xy_pos, *groups, collidable=collidable)

        self.stages: list[pg.Surface] = []
        self.hp = Poop.max_hp

        self.set_image()
        self.set_rect(CELL_SIZE, CELL_SIZE)

    def set_image(self):
        poop_type = random.choices(list(range(0, 5)), [0.90, 0.045, 0.045, 0.005, 0.005])[0]
        # Agregar botín a self.treasure si la textura es de los últimos dos
        texture_x = poop_type * CELL_SIZE
        self.stages = [Poop.poops.subsurface(texture_x, y * CELL_SIZE, CELL_SIZE, CELL_SIZE) for y in range(5)]
        self.image = self.stages[0]

    def hurt(self, damage: int):
        """
        Método para aplicar daño a Poop.

        :param damage: Cantidad de daño.
        """
        if not DestroyableItem.hurt(self, damage):
            return

        percent = self.hp / Poop.max_hp
        if percent >= 0.75:
            self.image = self.stages[0]
        elif percent >= 0.5:
            self.image = self.stages[1]
        elif percent >= 0.25:
            self.image = self.stages[2]
        elif percent > 0:
            self.image = self.stages[3]
        else:
            self.destroy()

    def destroy(self):
        """
        Destrucción de Poop después de la explosión/rotura.
        """
        DestroyableItem.destroy(self)
        self.image = self.stages[4]
        random.choice(self.poop_destoryed).play()
