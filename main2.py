import pygame as pg
from src import consts
import argparse

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

def main(algorithm):
    name_hero = "isaac"
    main_hero = Player(name_hero)
    
    if algorithm == 0:
        print("Algoritmo genético de estado estacionario")
    else:
        print("Algoritmo genético generacional")

    levels = [Level(floor_type, main_hero, algorithm=algorithm) for floor_type in consts.FloorsTypes]
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
                    levels = [Level(floor_type, main_hero, algorithm=algorithm) for floor_type in consts.FloorsTypes]
                    for level in levels:
                        level.change_all_rooms_state()
                    minimaps = [Minimap(level) for level in levels]
                if event.key == pg.K_d:
                    for level in levels:
                        level.download_level_map_to_file("mapa" + str(levels.index(level)) + ".txt")
                if event.key == pg.K_c:
                    for level in levels:
                        level.load_level_map_from_file("mapa" + str(levels.index(level)) + ".txt")
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ejecución del juego con algoritmo genético.')
    parser.add_argument('--algorithm', type=int, default=0, choices=[0, 1],
                        help='Especifica el algoritmo a utilizar: 0 para estado estacionario, 1 para generacional')

    args = parser.parse_args()
    main(args.algorithm)
    