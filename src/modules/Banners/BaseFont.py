import pygame as pg

from src.utils.funcs import cut_sheet


class BaseFont:
    """
    Clase de fuente base.

    :param name: Ruta del archivo, comenzando desde src/data, por ejemplo: "font/prices.png"
    :param alphabet: Letras en orden de la imagen de la fuente.
    :param columns: Número de columnas.
    :param rows: Número de filas.
    :param total: Cantidad total de letras (si hay celdas vacías).
    :param scale_sizes: Tamaños de escala (ancho, alto) a los que se debe ajustar.
    """

    def __init__(self,
                 name: str,
                 alphabet: str,
                 columns: int,
                 rows: int,
                 total: int = None,
                 scale_sizes: tuple[int, int] = None):
        self.letters = cut_sheet(name, columns, rows, total=total, scale_sizes=scale_sizes)
        self.alphabet = alphabet

        assert len(self.letters) == len(alphabet), "Las letras ingresadas son incorrectas o la ruta a la fuente es incorrecta"

    def write_text(self, text: str) -> pg.Surface:
        """
        Escribir texto.

        :param text: El texto a escribir.
        :return: Superficie con el texto.
        """

        text = text.lower()
        width, height = self.letters[0].get_size()
        surface = pg.Surface((len(text) * width, height), pg.SRCALPHA, 32)

        for i, symb in enumerate(text):
            try:
                surface.blit(self.letters[self.alphabet.index(symb)],
                             (i * width, 0))
            except IndexError:
                raise IndexError(f'En la fuente de letras "{self.alphabet}" no se encuentra la letra "{symb}')

        return surface

    def place_text(self, screen: pg.Surface, text: str | pg.Surface,
                   xy_center: tuple[int, int], xy_leftup: tuple[int, int] = None):
        """
        Aplica el texto en la pantalla.

        :param screen: La pantalla en la que se aplica.
        :param text: El texto que se aplica.
        :param xy_center: El centro donde se aplica.
        :param xy_leftup: La esquina superior izquierda.
        """

        if isinstance(text, str):
            text = self.write_text(text)

        if not xy_leftup:
            x, y = xy_center
            x -= text.get_width() // 2
            y -= text.get_height() // 2
        else:
            x, y = xy_leftup
        screen.blit(text, (x, y))
