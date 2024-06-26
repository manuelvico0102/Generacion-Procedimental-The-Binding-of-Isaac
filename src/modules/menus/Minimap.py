import pygame as pg


from src.modules.levels import Level
from src.consts import MINIMAP_WIDTH, MINIMAP_HEIGHT, MINIMAP_CELL_WIDTH, MINIMAP_CELL_HEIGHT


class Minimap:
    """
    Clase Minimap.

    :param level: Nivel actual.
    """
    def __init__(self,
                 level: Level):
        self.level = level
        self.minimap = pg.Surface((MINIMAP_WIDTH, MINIMAP_HEIGHT))
        self.update_minimap()

    def update_minimap(self):
        """
        Actualización del minimapa.
        """
        rooms = self.level.get_rooms()
        surface = pg.Surface((MINIMAP_WIDTH, MINIMAP_HEIGHT), pg.SRCALPHA, 32)
        for y, row in enumerate(rooms):
            for x, col in enumerate(row):
                if rooms[y][x]:
                    cell = rooms[y][x].get_minimap_cell()
                    surface.blit(cell, (x * MINIMAP_CELL_WIDTH, y * MINIMAP_CELL_HEIGHT))
        self.minimap = surface

    def render(self, screen: pg.Surface, width: int = MINIMAP_CELL_WIDTH, height: int = MINIMAP_CELL_HEIGHT // 2):
        screen.blit(self.minimap, (width, height))
