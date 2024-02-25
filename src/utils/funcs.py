import os
import sys
from functools import cache

import pygame as pg
import sqlite3
from src.consts import WALL_SIZE, GAME_WIDTH, CELL_SIZE, GAME_HEIGHT, Moves


def resource_path(*relative_path, use_abs_path: bool = False):
    save_relative = relative_path

    if not use_abs_path and getattr(sys, '_MEIPASS', False):
        base_path = getattr(sys, '_MEIPASS')
        relative_path = relative_path[2:]
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, *relative_path), save_relative, relative_path


@cache
def load_image(name: str,
               colorkey: pg.Color | int | None = None,
               crop_it: bool = False) -> pg.Surface:
    """
    Carga una imagen en pygame.Surface.

    :param name: Ruta del archivo, comenzando desde src/data, por ejemplo "textures/room/basement.png"
    :param colorkey: Píxel que se utilizará para eliminar el fondo. Si es -1, se utilizará el píxel superior izquierdo.
    :param crop_it: Recortar la imagen según el fondo transparente.
    :return: pygame.Surface
    """
    fullname, save_rel, rel = resource_path('src', 'data', *name.split('/'))
    if not os.path.isfile(fullname):
        raise FileNotFoundError(f"Archivo de imagen'{fullname}' no encontrado\n{save_rel}\n{rel}")
    image = pg.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    if crop_it:
        image = crop(image)

    return image


@cache
def load_sound(name, return_path: bool = False) -> pg.mixer.Sound | str:
    """
    Carga un sonido en pygame.Sound.

    :param name: Ruta del archivo, comenzando desde src/data, por ejemplo "sounds/fart.mp3"
    :param return_path: Devuelve la ruta del archivo en lugar del sonido en sí.
    :return: pygame.Sound o ruta del archivo
    """
    fullname, save_rel, rel = resource_path('src', 'data', *name.split('/'))
    if not os.path.isfile(fullname):
        raise FileNotFoundError(f"Archivo de sonido '{fullname}' no encontrado\n{save_rel}\n{rel}")
    if return_path:
        return fullname
    sound = pg.mixer.Sound(fullname)
    return sound


@cache
def crop(screen: pg.Surface) -> pg.Surface:
    """
    Recorta la imagen según los píxeles no vacíos en los bordes.

    :param screen: Imagen.
    :return: Imagen recortada.
    """
    pixels = pg.PixelArray(screen)
    background = pixels[0][0]  # noqa
    width, height = screen.get_width(), screen.get_height()
    min_x = width
    min_y = height
    max_x = 0
    max_y = 0

    for x in range(width):
        for y in range(height):
            current = pixels[x][y]  # noqa
            if current != background:
                max_x = max(x, max_x)
                max_y = max(y, max_y)
                min_x = min(x, min_x)
                min_y = min(y, min_y)

    return screen.subsurface((min_x, min_y, max_x - min_x, max_y - min_y))


def pixels_to_cell(xy_pos: tuple[int, int] | tuple[float, float]) -> tuple[int, int] | None:
    """
    Traduce los píxeles en la pantalla a una celda de la habitación.

    :param xy_pos: Coordenadas en píxeles.
    :return: Coordenadas en celdas.
    """
    x, y = xy_pos
    if WALL_SIZE <= x < GAME_WIDTH - WALL_SIZE and WALL_SIZE <= y < GAME_HEIGHT - WALL_SIZE:
        x_cell = x - WALL_SIZE
        y_cell = y - WALL_SIZE
        return int(x_cell // CELL_SIZE), int(y_cell // CELL_SIZE)
    return None


def cell_to_pixels(xy_pos: tuple[int, int]) -> tuple[int, int]:
    """
    Traduce una celda de la habitación a píxeles en la pantalla (centro de la celda).

    :param xy_pos: Coordenadas de la celda.
    :return: Coordenadas en píxeles (centro).
    """
    x_cell, y_cell = xy_pos
    x = x_cell * CELL_SIZE + WALL_SIZE + CELL_SIZE // 2
    y = y_cell * CELL_SIZE + WALL_SIZE + CELL_SIZE // 2
    return int(x), int(y)


def cut_sheet(sheet: str | pg.Surface, columns: int, rows: int,
              total: int = None, scale_sizes: tuple[int, int] = None) -> list[pg.Surface]:
    """
    Carga de fuente.

    :param sheet: Ruta del archivo, comenzando desde src/data, por ejemplo "font/prices.png" (o directamente una Surface).
    :param columns: Número de columnas.
    :param rows: Número de filas.
    :param total: Total de letras (si hay celdas vacías).
    :param scale_sizes: Tamaño máximo de escala (ancho, alto).
    :return: Lista de Surface, donde cada Surface representa un número o letra de la fuente.
    """

    frames: list[pg.Surface] = []
    if isinstance(sheet, str):
        sheet = load_image(sheet)

    rect = pg.Rect(
        0, 0,
        sheet.get_width() // columns,
        sheet.get_height() // rows
    )

    if scale_sizes:
        scale_sizes = (scale_sizes[0] if scale_sizes[0] != -1 else rect.width,
                       scale_sizes[1] if scale_sizes[0] != -1 else rect.height)

    for y in range(rows):
        if total is not None and len(frames) == total:
            break
        for x in range(columns):
            frame_location = (rect.w * x, rect.h * y)
            part = sheet.subsurface(pg.Rect(frame_location, rect.size))

            if scale_sizes:
                part = pg.transform.scale(part, scale_sizes)

            frames.append(part)

            if total is not None and len(frames) == total:
                break

    return frames


def get_direction(second_rect: pg.Rect, first_rect: pg.Rect):
    """
    Devuelve desde qué lado se produjo la colisión del segundo rectángulo con el primer rectángulo.

    :param first_rect: El cuerpo que colisionó.
    :param second_rect: El cuerpo con el que se produjo la colisión.
    """
    if (
            first_rect.collidepoint(second_rect.midright) and
            (
                    first_rect.collidepoint(second_rect.topright) or
                    first_rect.collidepoint(second_rect.bottomright)
            ) and
            not first_rect.collidepoint(second_rect.midleft) and
            (
                    not first_rect.collidepoint(second_rect.topleft) or
                    not first_rect.collidepoint(second_rect.bottomleft)
            )
    ):
        return Moves.RIGHT

    if (
            first_rect.collidepoint(second_rect.midleft) and
            (
                    first_rect.collidepoint(second_rect.topleft) or
                    first_rect.collidepoint(second_rect.bottomleft)
            ) and
            not first_rect.collidepoint(second_rect.midright) and
            (
                    not first_rect.collidepoint(second_rect.topright) or
                    not first_rect.collidepoint(second_rect.bottomright)
            )
    ):
        return Moves.LEFT

    if (
            first_rect.collidepoint(second_rect.midbottom) and
            (
                    first_rect.collidepoint(second_rect.bottomleft) or
                    first_rect.collidepoint(second_rect.bottomright)
            ) and
            not first_rect.collidepoint(second_rect.midtop) and
            (
                    not first_rect.collidepoint(second_rect.topleft) or
                    not first_rect.collidepoint(second_rect.topright)
            )
    ):
        return Moves.DOWN

    if (
            first_rect.collidepoint(second_rect.midtop) and
            (
                    first_rect.collidepoint(second_rect.topleft) or
                    first_rect.collidepoint(second_rect.topright)
            ) and
            not first_rect.collidepoint(second_rect.midbottom) and
            (
                    not first_rect.collidepoint(second_rect.bottomleft) or
                    not first_rect.collidepoint(second_rect.bottomright)
            )
    ):
        return Moves.UP

    first_rect, second_rect = second_rect, first_rect

    if second_rect.collidepoint(first_rect.topleft):
        return Moves.TOPLEFT

    if second_rect.collidepoint(first_rect.topright):
        return Moves.TOPRIGHT

    if second_rect.collidepoint(first_rect.bottomleft):
        return Moves.BOTTOMLEFT

    if second_rect.collidepoint(first_rect.bottomright):
        return Moves.BOTTOMRIGHT


def create_data_base():
    con = sqlite3.connect(resource_path('stats.sqlite', use_abs_path=True)[0])
    cur = con.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS game_over (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            win_or_loose STRING,
            score INT);
            """)
    con.commit()


def add_db(win_or_loose: str, score: int):
    con = sqlite3.connect(resource_path('stats.sqlite', use_abs_path=True)[0])
    cur = con.cursor()
    cur.execute(f"""INSERT INTO game_over (win_or_loose, score) VALUES (?, ?)""", (win_or_loose, score))
    con.commit()


def select_from_db():
    con = sqlite3.connect(resource_path('stats.sqlite', use_abs_path=True)[0])
    cur = con.cursor()
    res = cur.execute(f"""SELECT * FROM game_over""").fetchall()
    return res
