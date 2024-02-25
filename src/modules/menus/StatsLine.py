import pygame as pg

from src.consts import STATS_HEIGHT
from src.modules.characters.parents import Player
from src.modules.menus.Minimap import Minimap
from src.modules.menus.HeroStats import HeroStats
from src.modules.levels.Level import Level
from src.utils.funcs import load_image


class Stats:
    """
    Clase de la línea de estadísticas en la parte superior.

    :param main_hero: El héroe principal.
    :param level: El nivel actual.
    """
    black_line = load_image("textures/room/black_line.png")

    def __init__(self,
                 main_hero: Player,
                 level: Level):
        self.main_hero = main_hero
        self.minimap = Minimap(level)
        self.hero_stats = HeroStats(main_hero)

    def update_minimap(self):
        """
        Update del minimapa.
        """
        self.minimap.update_minimap()

    def update_hero_stats(self):
        """
        Actualización de las estadísticas del personaje.
        """
        self.hero_stats.update()

    def render(self, screen: pg.Surface):
        self.minimap.render(screen)
        self.hero_stats.render(screen)
        screen.blit(Stats.black_line, (0, STATS_HEIGHT - Stats.black_line.get_height() // 2))
