import random
from typing import Type

import pygame as pg

from src.consts import PICKUP_ART, CELL_SIZE
from src.utils.funcs import load_image, load_sound
from src.modules.BaseClasses import PickableItem, BaseArtifact


class Pedestal(PickableItem):
    """
    Clase de pedestal en la que se encuentra un artefacto.

    :param xy_pos: Posición del pedestal en la habitación.
    :param collide_groups: Grupos de sprites con los que no se puede colisionar.
    :param artifacts_group: Grupo de sprites donde todos los sprites son artefactos.
    :param groups: Grupos de sprites.
    """

    pedestal = load_image("textures/room/altars.png").subsurface(0, 0, CELL_SIZE, CELL_SIZE)
    pick_sound = [load_sound(f"sounds/powerup{i}.mp3") for i in range(1, 5)]

    def __init__(self,
                 xy_pos: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup,
                 artifacts_group: pg.sprite.AbstractGroup = None,
                 artifact: Type[BaseArtifact] = None):
        PickableItem.__init__(self, xy_pos, *groups, collidable=True)

        self.image = Pedestal.pedestal
        self.set_rect()
        self.pick_sound = Pedestal.pick_sound

        self.artifact: BaseArtifact | None = None
        self.set_artifact(artifact, artifacts_group)

    def set_artifact(self, artifact: Type[BaseArtifact] | None, artifacts_group: pg.sprite.AbstractGroup | None):
        """
        Establece el artefacto en el pedestal.

        :param artifact: Artefacto.
        :param artifacts_group: Grupo de sprites donde todos los sprites son artefactos.
        """
        if artifact:
            assert isinstance(artifacts_group, pg.sprite.AbstractGroup)
            self.artifact = artifact(self.rect.midtop, artifacts_group)

    def update(self, delta_t: float):
        """
        La animación del artefacto (movimiento hacia arriba y hacia abajo) ocurre dentro del propio artefacto.

        :param delta_t: Tiempo transcurrido desde el último fotograma.
        """
        if self.artifact:
            self.artifact.update(delta_t)

    def pickup(self):
        """
        Recoger el objeto.
        """
        if not self.artifact:
            return

        if isinstance(self.pick_sound, pg.mixer.Sound):
            self.pick_sound.play()
        elif isinstance(self.pick_sound, list):
            random.choice(self.pick_sound).play()

        pg.event.post(pg.event.Event(PICKUP_ART, {
                                                 'item': self.artifact,
                                                 'self': self
                                                 }
                                     )
                      )

        self.artifact.kill()
        self.artifact = None
