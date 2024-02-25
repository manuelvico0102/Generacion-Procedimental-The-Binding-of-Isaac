import pygame as pg

from src.modules.BaseClasses import MoveSprite


class BaseArtifact(MoveSprite):
    """
    Clase de artefacto que vuela sobre un pedestal.

    :param xy_pos: Posición en la habitación (pedestal).
    :param groups: Grupos de sprites.
    :param xy_pixels: Posición en píxeles.
    """

    fly_speed = 0.1  # Velocidad de subida y bajada en celdas/segundo
    change_direction_delay = 2

    modes = {
        "mul": lambda x, y: x * y,
        "add": lambda x, y: x + y
    }
    mode = modes["add"]  # Método de aplicación al artefacto (suma o multiplicación).

    # Aquí se encuentra todo lo que hace mejor.
    boosts = {
        "max_hp": 1,         # Cambio en la salud máxima (en corazones enteros).
        "heal_hp": 1,        # Cambio en la salud actual (en corazones enteros).
        "damage": 1,         # Cambia el daño infligido por el personaje.
        "speed": 1,          # Cambia la velocidad del personaje (celdas/segundo).
        "shot_speed": 1,     # Cambia la velocidad de las lágrimas (celdas/segundo).
        "shot_distance": 1,  # Cambia el rango/distancia de las lágrimas (celdas).
        "shot_delay": -1,    # Cambia el retraso entre disparos (segundos).
    }

    """
    for stats, dif in item.boosts:
        if stats == "...":
            self.smt = item.mode(self.smt, dif)
        elif ...:
            ...
    """

    def __init__(self,
                 xy_pixels: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup):
        MoveSprite.__init__(self, (0, 0), (), *groups,
                            acceleration=0, xy_pixels=xy_pixels)

        self.set_speed(0, -BaseArtifact.fly_speed)
        self.change_direction_ticks = 0

        self.set_image()
        self.set_rect()

    def update(self, delta_t: float):
        self.change_direction_ticks += delta_t
        if self.change_direction_ticks >= BaseArtifact.change_direction_delay:
            self.change_direction_ticks = 0
            self.set_speed(0, -self.vy)
        self.move(delta_t)
