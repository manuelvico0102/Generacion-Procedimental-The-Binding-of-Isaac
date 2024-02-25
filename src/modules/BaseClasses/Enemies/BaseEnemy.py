import pygame as pg

from src.modules.BaseClasses.Based.BaseTear import BaseTear
from src.modules.BaseClasses.Based.MoveSprite import MoveSprite
from src.utils.funcs import load_sound
from src.modules.BaseClasses.Based.BaseSprite import BaseSprite
from src.modules.characters.parents import Player
from src.consts import DEATH_ENEMY


class BaseEnemy(BaseSprite):
    """
    Clase base de enemigos.

    :param xy_pos: Posición de aparición en celdas.
    :param hp: Salud.
    :param damage_from_blow: Daño recibido por explosiones.
    :param room_graph: Diccionario de celdas en la habitación.
    :param main_hero: Personaje principal (debe tener .rect).
    :param enemy_collide_groups: Grupos de sprites para manejar las colisiones de esta entidad.
    :param groups: Grupos de sprites.
    """

    explosion_kill = load_sound("sounds/explosion_kill.mp3")

    def __init__(self,
                 xy_pos: tuple[int, int],
                 hp: int,
                 damage_from_blow: int,
                 room_graph: dict[tuple[int, int]],
                 main_hero: Player,
                 enemy_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup):
        BaseSprite.__init__(self, xy_pos, *groups)
        self.groups = groups

        self.hp = hp
        self.damage_from_blow = damage_from_blow
        self.room_graph = room_graph
        self.main_hero = main_hero
        self.enemy_collide_groups = enemy_collide_groups
        self.image: pg.Surface
        self.rect: pg.Rect

    def blow(self):
        """
        Explosión de la entidad.
        """
        self.hurt(self.damage_from_blow)
        if self.hp <= 0:
            BaseEnemy.explosion_kill.play()

    def hurt(self, damage: int):
        self.hp -= damage
        if self.hp <= 0:
            self.death()

    def update_room_graph(self, room_graph: dict[tuple[int, int]]):
        """
        Actualiza el grafo de la habitación (por ejemplo, después de romper el Poop).

        :param room_graph: Diccionario de celdas similar a un grafo de la habitación.
        """
        self.room_graph = room_graph

    def death(self, is_boss: bool = False):
        """
        Muerte del enemigo.
        """
        count_score = 100
        if is_boss:
            count_score *= 10
        self.kill()
        pg.event.post(pg.event.Event(DEATH_ENEMY, {'count': count_score}))

    def collide(self, other: MoveSprite):
        """
            Comprueba la colisión con otro sprite y realiza las acciones apropiadas.

            Parámetros:
            - other (MoveSprite): El sprite con el que se comprueba la colisión.

            Retorna:
            - bool: True si ocurrió una colisión, False en caso contrario.
        """
        if isinstance(other, BaseTear):
            self.hurt(other.damage)
            other.destroy()
            return True
        if isinstance(other, Player):
            other.hurt(1)
            return True
        return False
