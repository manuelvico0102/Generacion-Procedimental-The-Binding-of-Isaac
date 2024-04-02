import math
import random
from typing import Type

import pygame as pg

from src.consts import CELL_SIZE
from src.modules.BaseClasses.Enemies.BaseEnemy import BaseEnemy
from src.modules.BaseClasses.Based.BaseTear import BaseTear
from src.modules.characters.parents import Player


class ShootingEnemy(BaseEnemy):
    """
    Enemigo que dispara.

    :param xy_pos: Posición de spawn en celdas.
    :param hp: Salud.
    :param damage_from_blow: Daño recibido por explosiones.
    :param room_graph: Grafo de celdas en la habitación.
    :param main_hero: Personaje principal (debe tener .rect).
    :param enemy_collide_groups: Grupos de sprites con los que esta entidad puede colisionar.

    :param shot_damage: Daño del disparo.
    :param shot_max_distance: Máxima distancia de vuelo del disparo en celdas.
    :param shot_max_speed: Máxima velocidad de vuelo del disparo en celdas.
    :param shot_delay: Retraso entre disparos.
    :param tear_class: Clase de la lágrima.
    :param tear_collide_groups: Grupos de sprites con los que las lágrimas pueden colisionar.

    :param groups: Grupos de sprites.
    """

    def __init__(self,
                 xy_pos: tuple[int, int],
                 hp: int,
                 damage_from_blow: int,
                 room_graph: dict[tuple[int, int]],
                 main_hero: Player,
                 enemy_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 shot_damage: int | float,
                 shot_max_distance: int | float,
                 shot_max_speed: int | float,
                 shot_delay: int | float,
                 tear_class: Type[BaseTear],
                 tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup):
        BaseEnemy.__init__(self, xy_pos, hp, damage_from_blow, room_graph, main_hero, enemy_collide_groups, *groups)

        self.shot_damage = shot_damage
        self.shot_max_distance = shot_max_distance
        self.shot_max_speed = shot_max_speed
        self.shot_delay = shot_delay
        self.tear_class = tear_class
        self.tear_collide_groups = tear_collide_groups

        self.shot_ticks = random.uniform(0, self.shot_delay / 2)
        self.tears = pg.sprite.Group()

    def update(self, delta_t: float):
        """
        Actualiza al enemigo, contando el tiempo para disparar o moverse.

        :param delta_t: Tiempo desde el último fotograma.
        """
        self.shot_ticks += delta_t

        if self.shot_ticks >= self.shot_delay:
            self.shot()

        self.tears.update(delta_t)

    def draw_tears(self, screen: pg.Surface):
        """
        Dibuja las lágrimas.
        """
        self.tears.draw(screen)

    def shot(self) -> bool:
        """
        Disparo hacia el personaje principal.

        :return: Devuelve True si disparó.
        """
        # body
        x, y = self.main_hero.rect.center
        dx = x - self.rect.centerx
        dy = y - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > self.shot_max_distance * CELL_SIZE or distance == 0:  # Dispara cuando ya esta cerca
            return False

        self.shot_ticks = 0
        vx = self.shot_max_speed * dx / distance + getattr(self, 'vx', 0)  # Teniendo en cuenta su propia velocidad
        vy = self.shot_max_speed * dy / distance + getattr(self, 'vy', 0)  # Teniendo en cuenta su propia velocidad
        self.tear_class((self.x, self.y), self.rect.center, self.shot_damage, self.shot_max_distance, vx, vy,
                        self.tear_collide_groups, self.tears)
        return True
