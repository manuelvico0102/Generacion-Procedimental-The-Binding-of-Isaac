import random

import pygame as pg

from src.consts import CELL_SIZE, FirePlacesTypes
from src.modules.animations.Animation import Animation
from src.modules.BaseClasses import MoveSprite, DestroyableItem, ShootingEnemy
from src.modules.characters.parents import Player
from src.utils.funcs import load_image, load_sound
from src.modules.entities.tears.ExampleTear import ExampleTear


class FireImage:
    fires = load_image("textures/room/fireplaces.png")
    width = fires.get_width()
    height = CELL_SIZE


class FireTextures(FireImage):
    fires_100 = [
        FireImage.fires.subsurface(0, y * CELL_SIZE, FireImage.fires.get_width(), CELL_SIZE)
        for y in range(2)
    ]

    fires_67 = [
        pg.transform.scale(
            FireImage.fires.subsurface(0, y * CELL_SIZE, FireImage.fires.get_width(), CELL_SIZE),
            (FireImage.width * 0.875, FireImage.height * 0.875)
        )
        for y in range(2)
    ]

    fires_33 = [
        pg.transform.scale(
            FireImage.fires.subsurface(0, y * CELL_SIZE, FireImage.fires.get_width(), CELL_SIZE),
            (FireImage.width * 0.75, FireImage.height * 0.75)
        )
        for y in range(2)
    ]

    fires_wood = [
        (
            load_image("textures/room/firewoods.png").subsurface(x * CELL_SIZE, 0,
                                                                 CELL_SIZE, CELL_SIZE),
            load_image("textures/room/firewoods.png").subsurface(x * CELL_SIZE, CELL_SIZE,
                                                                 CELL_SIZE, CELL_SIZE),
        )
        for x in range(6)
    ]

    fireplace_destoryed = [load_sound("sounds/pop1.wav"), load_sound("sounds/pop2.mp3")]
    fireplace_shot = load_sound("sounds/fire_shot.wav")


class FirePlace(DestroyableItem, ShootingEnemy, FireTextures):
    """
    Kostyor. Late. Se destruye.

    :param xy_pos: Posición en la habitación.
    :param groups: Grupos de sprites.
    :param fire_type: Tipo de fuego.
    :param tear_collide_groups: Grupos con los que colisiona la lágrima del kostyor, si el kostyor es hostil.
    :param main_hero: Héroe principal, si el fuego es hostil.
    :param hurtable: Si causa daño al ser tocado.
    """

    max_hp = 10
    fps = 16

    def __init__(self,
                 xy_pos: tuple[int, int],
                 *groups: pg.sprite.Group,
                 fire_type: FirePlacesTypes = FirePlacesTypes.DEFAULT,
                 tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...] = None,
                 main_hero: Player = None,
                 hurtable: bool = True):
        tear_damage = 1
        tear_distance = 4
        tear_speed = 2
        tear_delay = 7
        tear_class = ExampleTear

        DestroyableItem.__init__(self, xy_pos, *groups, hurtable=hurtable)
        if fire_type == FirePlacesTypes.RED:
            assert tear_collide_groups and main_hero
            ShootingEnemy.__init__(self, xy_pos, FirePlace.max_hp, FirePlace.max_hp, dict(), main_hero, (),
                                   tear_damage, tear_distance, tear_speed, tear_delay, tear_class, tear_collide_groups,
                                   *groups)

        self.fire_type = fire_type
        self.stages: list[pg.Surface] = []
        self.stage_sheet: pg.Surface = pg.Surface((0, 0))
        self.woods: list[pg.Surface] = []
        self.ticks = 0
        self.frame = 0
        self.hp = FirePlace.max_hp
        self.animation: Animation | None = None
        self.is_alive = True

        self.set_image()
        # El daño es incorrecto debido a que la imagen tiene una altura de CELL_SIZE * 1.25,
        # y no sé cómo dibujar la imagen en una posición diferente a la esquina superior izquierda del rectángulo.
        self.set_rect()

        self.event_rect = pg.Rect(0, 0, 50, 50)
        self.event_rect.center = self.rect.center

    def set_image(self):
        for i, fire_type in enumerate(FirePlacesTypes):
            if fire_type == self.fire_type:
                self.stages = [FireTextures.fires_100[i], FireTextures.fires_67[i],
                               FireTextures.fires_33[i], [pg.Surface((0, 0))]]
                break
        assert self.stages

        self.update_stage_sheet(self.stages[0])
        self.woods = random.choice(FireTextures.fires_wood)
        self.update_image()

    def update_image(self):
        """
        Actualiza la imagen, establece las superficies de la madera y luego del fuego si está encendido.
        """
        self.image = pg.Surface((CELL_SIZE, CELL_SIZE * 1.25), pg.SRCALPHA, 32)
        self.image.blit(self.woods[not self.is_alive], (0, CELL_SIZE * 0.25))
        if self.is_alive:
            self.image.blit(self.animation.image, (
                    (CELL_SIZE - self.animation.image.get_width()) // 2,
                    (CELL_SIZE - self.animation.image.get_height()) // 2
                )
            )

    def update(self, delta_t: float):
        if self.fire_type == FirePlacesTypes.RED:
            ShootingEnemy.update(self, delta_t)

        if not self.is_alive:
            return

        if self.animation.update(delta_t):
            self.update_image()

    def shot(self):
        """
        Disparo al jugador principal si el fuego es de tipo disparador.
        """
        if self.is_alive and ShootingEnemy.shot(self):
            FireTextures.fireplace_shot.play()

    def hurt(self, damage: int):
        """
        Inflictar daño a la hoguera.

        :param damage: Cantidad de daño.
        """
        if not DestroyableItem.hurt(self, damage):
            return

        percent = self.hp / FirePlace.max_hp
        if percent >= 0.67:
            self.update_stage_sheet(self.stages[0])
        elif percent >= 0.33:
            self.update_stage_sheet(self.stages[1])
        elif percent > 0:
            self.update_stage_sheet(self.stages[2])
        else:
            self.destroy()

    def update_stage_sheet(self, stage_sheet: pg.Surface):
        self.stage_sheet = stage_sheet
        self.animation = Animation(self.stage_sheet, 6, 1, self.fps,
                                   frame=self.animation.cur_frame if self.animation else -1)

    def destroy(self):
        """
        Destrucción del hoguera después de la explosión/rotura.
        """
        DestroyableItem.destroy(self)
        self.update_image()
        random.choice(FireTextures.fireplace_destoryed).play()

    def draw_tears(self, screen: pg.Surface):
        """
        Dibuja las lágrimas si el fuego es de tipo disparador.
        :param screen: Superficie.
        """
        if self.fire_type == FirePlacesTypes.RED:
            ShootingEnemy.draw_tears(self, screen)

    def collide(self, other: MoveSprite):
        if self.fire_type == FirePlacesTypes.RED and other in self.tears:
            return
        if other.rect.colliderect(self.event_rect):
            DestroyableItem.collide(self, other)
