import pygame as pg

from src.modules.mainmenu import startscrean
from src.utils.funcs import load_sound, load_image

from src.modules.Banners.end_screen import end_screen
from src.modules.Banners.pause import pause
from src.modules.Banners.win import win
from src.modules.BaseClasses.Based.BaseGame import BaseGame
from src.modules.handlers.MainHeroActionsHandler import MainHeroActionsHandler
from src.modules.levels.Level import Level
from src.modules.levels.Room import Room
from src.modules.menus.StatsLine import Stats
from src.modules.characters.parents import Player
from src.consts import (FloorsTypes, GAME_HEIGHT, GAME_WIDTH, STATS_HEIGHT, ROOM_WIDTH, ROOM_HEIGHT,
                        MOVE_TO_NEXT_ROOM, MOVE_TO_NEXT_LEVEL, PICKUP_LOOT, PICKUP_ART, BUY_ITEM, USE_BOMB, GG_HURT,
                        USE_KEY, DEATH_ENEMY, GAME_OVER)


def start_game(main_screen):
    """
     Menu de inicio.

     :param main_screen: lienzo sobre el que dibujar.
    """
    pg.display.set_caption("The Binding of Isaac: Python")
    pg.display.set_icon(load_image("images/icon/64x64.ico"))
    pg.mixer.music.load(load_sound('sounds/main_theme.mp3', return_path=True))
    pg.mixer.music.play()
    return startscrean.start_screen(main_screen)


class Game(BaseGame):
    """
    Clase del juego.

    :param name: nombre del personaje
    :param main_screen: lienzo principal en el que se dibujará.
    """
    def __init__(self, name: str, main_screen: pg.Surface, fps: int = 60):
        self.name_hero = name
        self.main_hero = Player(name)

        BaseGame.__init__(self, main_screen, fps)
        self.level_screen = pg.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.is_paused = False
        self.levels = [Level(floor_type, self.main_hero) for floor_type in FloorsTypes]
        self.current_level = self.levels[0]
        self.current_level.update_main_hero_collide_groups()
        self.stats = Stats(self.main_hero, self.current_level)

        self.main_hero_handler = MainHeroActionsHandler(self.main_hero)

    def setup(self):
        """
        Registro de eventos.
        """
        self.register_event(pg.KEYDOWN, self.main_hero_handler.keyboard_handler)
        self.register_event(pg.KEYDOWN, self.switch_pause)
        self.register_event(pg.KEYUP, self.main_hero_handler.keyboard_handler)
        self.register_event(PICKUP_LOOT, self.main_hero_handler.loot_pickup_handler)
        self.register_event(PICKUP_ART, self.main_hero_handler.artifact_pickup_handler)
        self.register_event(BUY_ITEM, self.main_hero_handler.buy_handler)
        self.register_event(USE_BOMB, self.set_bomb)
        self.register_event(MOVE_TO_NEXT_LEVEL, self.move_to_next_level)
        self.register_event(MOVE_TO_NEXT_ROOM, self.move_to_next_room)
        self.register_event(DEATH_ENEMY, self.main_hero_handler.scoring_points)
        self.register_event(GAME_OVER, self.end_screen)
        self.register_event(pg.KEYDOWN, self.kill_all)

        for event in (PICKUP_LOOT, PICKUP_ART, BUY_ITEM, USE_BOMB, GG_HURT, USE_KEY, MOVE_TO_NEXT_ROOM):
            self.register_event(event, self.update_stats)

    def end_screen(self, event: pg.event.Event):
        """
        Ventana de fin.

        :param event: tecla presionada
        """
        self.running = False
        end_screen(self.main_screen, self.name_hero, self.main_hero.score)

    def switch_pause(self, event: pg.event.Event):
        """
        Pausa.

        :param event: tecla presionada
        """
        if event.key == pg.K_ESCAPE:
            self.main_hero.reset_speed()
            self.is_paused = True
            pause(self.main_screen, self.name_hero)

    def get_current_level_rooms(self) -> list[list[Room | None]]:
        """
        Obtener todas las habitaciones del nivel actual.

        :return: Una lista bidimensional de habitaciones.
        """
        return self.current_level.get_rooms()

    def move_to_next_level(self, *args):
        """
        Transición al siguiente nivel.
        """
        if self.current_level.floor_type == FloorsTypes.WOMB:
            if win(self.main_screen, score=self.main_hero.score):
                self.running = False
        self.main_hero.kill_tears()
        self.current_level = self.levels[(self.levels.index(self.current_level) + 1) % len(self.levels)]
        self.current_level.update_main_hero_collide_groups()
        self.move_main_hero((ROOM_WIDTH // 2, ROOM_HEIGHT // 2))
        self.stats = Stats(self.main_hero, self.current_level)

    def move_to_next_room(self, event: pg.event.Event):
        """
        Permite al personaje moverse a otra habitación.

        :param event: Evento que contiene la dirección (activado/causado por una puerta).
        """
        self.main_hero.kill_tears()
        self.current_level.move_to_next_room(event.direction)
        self.current_level.update_main_hero_collide_groups()
        self.stats.update_minimap()
        next_coords = event.next_coords
        self.move_main_hero(next_coords)

    def move_main_hero(self, xy_pos: tuple[int, int]):
        """
        Mueve al héroe principal a las coordenadas especificadas.

        :param xy_pos: Coordenadas del centro (coordenadas centrales).
        """
        self.main_hero.move_to_cell(xy_pos)

    def update_stats(self, event: pg.event.Event = None):
        """
        Actualiza el minimapa y las estadísticas del héroe.

        :param event: evento de tecla presionada
        """
        self.stats.update_minimap()
        self.stats.update_hero_stats()

    def kill_all(self, event: pg.event.Event):
        """
        Eliminar a todos. Básicamente, trucos incorporados.

        :param event: tecla presionada
        """
        if event.key == pg.K_r:
            for enemy in self.current_level.current_room.enemies.sprites():
                enemy.death()
            for boss in self.current_level.current_room.bosses.sprites():
                boss.death()
            # self.current_level.current_room.enemies.empty()
            # self.current_level.current_room.bosses.empty()

    def set_bomb(self, event: pg.event.Event):
        """
        Activación de la bomba.

        :param event: tecla presionada
        """
        if event.type == USE_BOMB:
            self.current_level.current_room.set_bomb(event)

    def update(self, delta_t: float):
        """
        Actualización.

        :param delta_t: tiempo desde la última actualización.
        """
        if self.is_paused:
            self.is_paused = False
            return
        self.current_level.update(delta_t)
        self.main_hero.update(delta_t)

    def draw(self, screen: pg.Surface):
        """
        Renderizar todo.

        :param screen: superficie en la que se va a renderizar.
        """
        self.stats.render(self.main_screen)
        self.current_level.render(self.level_screen)
        screen.blit(self.level_screen, (0, STATS_HEIGHT))
