import pygame as pg
from src import consts

pg.init()
pg.font.init()
pg.mixer.init()
screen = pg.display.set_mode((consts.WIDTH, consts.HEIGHT))

from src.modules.menus.Minimap import Minimap
from src.modules.levels.Level import Level
from src.modules.characters.parents import Player
from src.modules.levels.LevelGenerator import main as generate_level
from src.modules.levels.LevelGenerator import main as generate_initial_population
import src.modules.levels.algoritmoGenetico as ag

def main():
    name_hero = "isaac"
    main_hero = Player(name_hero)

    levels = [Level(floor_type, main_hero) for floor_type in consts.FloorsTypes]
    for level in levels:
        level.change_all_rooms_state()

    minimaps = [Minimap(level) for level in levels]

    num_levels = len(levels)
    num_cols = 3
    num_rows = 2
    minimap_width = consts.WIDTH // num_cols
    minimap_height = consts.HEIGHT // num_rows

    offset_x = 20
    offset_y = 100
    

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_r:  # Verificar si se presiona la tecla "r"
                    # Regenerar los niveles
                    levels = [Level(floor_type, main_hero) for floor_type in consts.FloorsTypes]
                    for level in levels:
                        level.change_all_rooms_state()
                    minimaps = [Minimap(level) for level in levels]

        screen.fill((0,0,0))

        for i, minimap in enumerate(minimaps[:6]):
            row = i // num_cols
            col = i % num_cols
            minimap_x = col * minimap_width + offset_x
            minimap_y = row * minimap_height + offset_y
            minimap.render(screen, minimap_x, minimap_y)
        
        pg.display.flip()

    pg.quit()


def main2(mapas):
    name_hero = "isaac"
    main_hero = Player(name_hero)

    levels = [Level(consts.FloorsTypes.BASEMENT, main_hero, level_map=mapa) for mapa in mapas]

    for level in levels:
        level.change_all_rooms_state()

    minimaps = [Minimap(level) for level in levels]

    num_cols = 3
    num_rows = 2
    minimap_width = consts.WIDTH // num_cols
    minimap_height = consts.HEIGHT // num_rows

    offset_x = 20
    offset_y = 100

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((0, 0, 0))

        for i, minimap in enumerate(minimaps):
            row = i // num_cols
            col = i % num_cols
            minimap_x = col * minimap_width + offset_x
            minimap_y = row * minimap_height + offset_y
            minimap.render(screen, minimap_x, minimap_y)

        pg.display.flip()

    pg.quit()

if __name__ == '__main__':
    main()
    #parent1, parent2, child = ag.main2()
    """parent1, parent2 = ag.generate_initial_population(2, 10, 6, 15)
    child = ag.crossover(parent1, parent2)

    print(parent1)
    print()
    print(parent2)
    print()
    #print(child)
    print()
    mapas = [parent1, parent2, child]
    main2(mapas)"""
    #ag.generate_initial_population(10, 10, 10, 20)
    