import pygame as pg

from src.utils.funcs import cell_to_pixels


class BaseSprite(pg.sprite.Sprite):
    """
    Sprite base.

    :param xy_pos: Posición en la habitación.
    :param groups: Grupos de sprites.
    """
    def __init__(self,
                 xy_pos: tuple[int, int],
                 *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.x, self.y = xy_pos

    def update(self, delta_t: float):
        """
        Actualiza la posición/contadores.

        :param delta_t: Tiempo transcurrido desde el último fotograma.
        """
        pass

    def set_image(self):
        """
        Establece la textura
        """
        pass

    def set_rect(self, width: int = None, height: int = None, up: int = 0, left: int = 0):
        """
        Establecer el objeto en el centro de su celda.
        """
        self.rect = self.image.get_rect()
        if width:
            self.rect.width = width
        if height:
            self.rect.height = height
        x, y = cell_to_pixels((self.x, self.y))
        self.rect.center = x - left, y - up

    def hurt(self, damage: int):
        """
        Obtener daño.
        """
        pass

    def blow(self):
        """
        Obtener daño de una explosión.
        """
        pass

    def collide(self, other: pg.sprite.Sprite) -> bool:
        """
        Manejo de colisiones.

        :param other: instancia de BaseSprite
        :return: ¿Habrá colisión? (diferentes objetos)
        """
        return other != self
