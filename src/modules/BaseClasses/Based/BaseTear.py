import math
import random

import pygame as pg

from src.modules.BaseClasses.Based.BaseSprite import BaseSprite
from src.modules.BaseClasses.Based.MoveSprite import MoveSprite
from src.consts import CELL_SIZE
from src.modules.animations.Animation import Animation
from src.utils.funcs import load_image, load_sound


class PopsImage:
    all_ends = load_image("textures/tears/tears_pop.png")
    width = all_ends.get_width()
    height = 64


class BaseTear(MoveSprite, PopsImage):
    all_tears: list[list[pg.Surface]] = [
        [
            load_image("textures/tears/tears.png").subsurface(x * 64, y * 64, 64, 64)
            for x in range(13)
        ]
        for y in range(2)
    ]

    impacts: list[pg.mixer.Sound] = [load_sound(f"sounds/tear_impact{i}.mp3") for i in range(1, 4)]

    """
    Clase base de la lágrima (puede requerir modificaciones).

    :param xy_pos: Posición en la habitación.
    :param xy_pixels: Coordenada de aparición en píxeles, centro de la lágrima.
    :param damage: Daño.
    :param distance: Distancia de vuelo en celdas (se convierte a píxeles/segundo).
    :param vx: Velocidad horizontal en celdas (se convierte a píxeles/segundo).
    :param vy: Velocidad vertical en celdas (se convierte a píxeles/segundo).
    :param collide_groups: Grupos con los que se debe comprobar la colisión.
    :param groups: Grupos de sprites.
    :param acceleration: Aceleración de frenado de la lágrima, si se desea que frene.
    :param max_lifetime: Tiempo máximo de vida.
    :param is_friendly: Ignora al personaje principal.
    """

    def __init__(self,
                 xy_pos: tuple[int, int],
                 xy_pixels: tuple[int, int],
                 damage: int,
                 max_distance: int | float,
                 vx: int | float,
                 vy: int | float,
                 collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.Group,
                 acceleration: int | float = 0,
                 max_lifetime: int | float = 0,
                 is_friendly: bool = False):
        MoveSprite.__init__(self, xy_pos, collide_groups, *groups, acceleration=acceleration, xy_pixels=xy_pixels)

        self.start_x, self.start_y = xy_pixels
        self.damage = damage
        self.max_distance = max_distance
        self.vx, self.vy = vx, vy
        self.collide_groups = collide_groups
        self.groups = groups
        self.is_friendly = is_friendly
        self.max_lifetime = max_lifetime
        self.lifetime_ticks = 0
        self.destroyed = False
        self.animation: Animation | None = None

        self.image: pg.Surface
        self.rect: pg.Rect

    def update(self, delta_t: float):
        """
        Actualiza la posición de la lágrima.

        :param delta_t: Tiempo transcurrido desde el último fotograma.
        """
        if self.destroyed:
            self.destroy_animation(delta_t)
            return

        self.lifetime_ticks += delta_t

        MoveSprite.move(self, delta_t)
        self.check_collides()

        if math.hypot(self.start_x - self.rect.x, self.start_y - self.rect.y) > self.max_distance * CELL_SIZE:
            self.destroy()
        elif self.max_lifetime and self.lifetime_ticks >= self.max_lifetime:
            self.destroy()

    def check_collides(self):
        """
        Comprueba las colisiones.
        """
        for collide_group in self.collide_groups:
            if pg.sprite.spritecollideany(self, collide_group):
                for collide in pg.sprite.spritecollide(self, collide_group, False):
                    collide: BaseSprite
                    # collide.hurt(self.damage)
                    collide.collide(self)

    def set_rect(self, width: int = None, height: int = None, up: int = 0, left: int = 0):
        """
        Establecer el rectángulo de la lágrima.
        """
        width, height = self.image.get_width(), self.image.get_height()
        self.rect = pg.Rect(self.start_x - width // 2, self.start_y - height // 2, width, height)

    def destroy(self):
        """
        Destruye la lagrima...
        """
        random.choice(BaseTear.impacts).play()
        self.destroyed = True

    def destroy_animation(self, delta_t: float):
        if not self.animation:
            raise SyntaxError("No hay animación al heredar de BaseTear / "
                              "No se ha sobrescrito el método update o destroy_animation")
        status = self.animation.update(delta_t)
        self.image = self.animation.image
        self.rect = self.animation.rect
        self.rect.center = self.x_center, self.y_center
        if status is None:
            self.kill()
