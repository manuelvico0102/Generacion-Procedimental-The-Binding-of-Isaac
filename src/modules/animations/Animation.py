import random

import pygame as pg

from src.utils.funcs import cut_sheet


class Animation:
    """
    Clase para reproducir animaciones.

    :param sheet: Superficie que se recorta en fotogramas.
    :param columns: Número de fotogramas en el ancho.
    :param rows: Número de fotogramas en el alto.
    :param fps: Velocidad de la animación.
    :param single_play: Reproducir la animación solo una vez.
    :param scale_sizes: Tamaño al que escalar el fotograma.
    :param frame: Desde qué fotograma comenzar, -1 - aleatorio.
    """
    def __init__(self,
                 sheet: pg.Surface,
                 columns: int,
                 rows: int,
                 fps: int,
                 single_play: bool = False,
                 scale_sizes: tuple[int, int] = None,
                 frame: int = 0,
                 total_frames: int = None):
        self.frames = cut_sheet(sheet, columns, rows, scale_sizes=scale_sizes, total=total_frames)
        self.rect = pg.Rect(0, 0, *self.frames[0].get_size())

        self.cur_frame = frame if frame != -1 else random.randint(0, len(self.frames) - 1)
        self.image = self.frames[self.cur_frame]

        self.ticks_counter = 0
        self.frame_delimiter = 1 / fps
        self.single_play = single_play

    def reset(self):
        self.ticks_counter = 0
        self.cur_frame = 0

    def update(self, delta_t: float) -> bool | None:
        """
        Actualiza el fotograma de la animación si ha llegado su momento.

        :param delta_t: Tiempo transcurrido desde el último fotograma.
        :return: True - el fotograma se actualizó. False - el fotograma no se actualizó. None - la animación de reproducción única ha terminado.
        """
        self.ticks_counter += delta_t

        if self.ticks_counter >= self.frame_delimiter:
            self.ticks_counter = 0

            index = self.cur_frame + 1

            if self.single_play and index == len(self.frames):
                return None

            self.cur_frame = index % len(self.frames)
            self.image = self.frames[self.cur_frame]

            return True

        return False
