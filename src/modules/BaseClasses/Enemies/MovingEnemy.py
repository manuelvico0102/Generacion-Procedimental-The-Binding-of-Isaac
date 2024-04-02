import math

import pygame as pg

from src.modules.BaseClasses.Enemies.BaseEnemy import BaseEnemy
from src.modules.BaseClasses.Based.MoveSprite import MoveSprite
from src.modules.characters.parents import Player
from src.modules.levels.Border import Border
from src.utils.funcs import pixels_to_cell, cell_to_pixels
from src.utils.graph import make_path_to_cell


class MovingEnemy(BaseEnemy, MoveSprite):
    """
    Enemigo que se mueve.

    :param xy_pos: Posición de aparición en celdas.
    :param hp: Salud.
    :param speed: Velocidad en celdas.
    :param damage_from_blow: Daño recibido de explosiones.
    :param move_update_delay: Retraso entre recálculos de la ruta hacia el personaje principal.
    :param room_graph: Diccionario de celdas en forma de grafo en la habitación.
    :param main_hero: Personaje principal (debe tener .rect).
    :param enemy_collide_groups: Grupos de sprites para manejar las colisiones de esta entidad.
    :param groups: Grupos de sprites.
    """

    def __init__(self,
                 xy_pos: tuple[int, int],
                 hp: int,
                 speed: int | float,
                 damage_from_blow: int,
                 move_update_delay: int | float,
                 room_graph: dict[tuple[int, int]],
                 main_hero: Player | pg.sprite.Sprite,
                 enemy_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup,
                 flyable: bool = False):
        BaseEnemy.__init__(self, xy_pos, hp, damage_from_blow, room_graph, main_hero, enemy_collide_groups, *groups)
        MoveSprite.__init__(self, xy_pos, enemy_collide_groups, *groups, acceleration=0)

        self.speed = speed
        self.move_update_delay = move_update_delay
        self.move_ticks = 0
        self.slowdown_coef: float = 1.0
        self.flyable = flyable
        self.path: list[tuple[int, int]] = []

        self.do_update_speed = True

    def update(self, delta_t: float):
        """
        Actualiza al enemigo, mide el tiempo para disparar o moverse.

        :param delta_t: Tiempo transcurrido desde el último fotograma.
        """
        BaseEnemy.update(self, delta_t)
        MoveSprite.update(self, delta_t)

        self.move_ticks += delta_t

        if self.move_ticks >= self.move_update_delay:
            self.update_move_speed()

        self.move(delta_t)

    def move(self, delta_t: float, change_speeds: bool = True):
        """
        Movimiento de la entidad.

        :param delta_t: Tiempo transcurrido desde el último fotograma.
        :param change_speeds: Indica si se debe llamar a update_move_speed().
        """
        MoveSprite.move(self, delta_t)

        # Verificar colisiones
        if self.flyable:
            self.check_fly_collides()
        else:
            MoveSprite.check_collides(self)

        # Si hay coordenadas y son diferentes a las actuales, actualizamos las velocidades
        xy_cell = pixels_to_cell((self.x_center, self.y_center))
        if xy_cell and (self.x, self.y) != xy_cell:
            self.x, self.y = xy_cell
            if change_speeds:
                self.update_move_speed()

    def move_back(self, rect: pg.Rect):
        """
        Maneja la colisión y cambia las velocidades para evitar obstáculos.

        :param rect: Centro del sprite con el que hubo colisión.
        """
        MoveSprite.move_back(self, rect)

    def update_move_speed(self):
        """
        Actualiza las velocidades vertical y horizontal para moverse hacia el personaje principal.
        """
        if not self.do_update_speed:
            self.move_ticks = 0
            return

        if self.flyable:  # Los voladores vuelan directamente hacia el personaje principal
            dx = self.main_hero.rect.centerx - self.rect.centerx
            dy = self.main_hero.rect.centery - self.rect.centery
            distance = math.hypot(dx, dy)
            if distance:
                self.set_speed(self.speed * dx / distance, self.speed * dy / distance)
            else:
                self.set_speed(0, 0)
            return

        self.move_ticks = 0
        xy_end = self.main_hero.rect.center
        xy_end = pixels_to_cell(xy_end)
        path_list = make_path_to_cell(self.room_graph, (self.x, self.y), xy_end)
        if not path_list or len(path_list) < 2:
            self.vx, self.vy = 0, 0
            return

        self.path = path_list[1:]
        next_cell = self.path[0]
        x, y = cell_to_pixels(next_cell)
        dx = x - self.rect.centerx
        dy = y - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance:
            self.set_speed(self.speed * dx / distance, self.speed * dy / distance)

    def check_fly_collides(self):
        for group in self.collide_groups:
            if sprites := pg.sprite.spritecollide(self, group, False):
                for sprite in sprites:
                    # Agregar aquí los objetos con los que los enemigos voladores deben colisionar
                    if sprite != self and isinstance(sprite, (Border,)):
                        sprite: Border
                        sprite.collide(self)
