import random

import pygame as pg

from typing import Type
from src.utils.funcs import cell_to_pixels, get_direction, load_image, crop, load_sound
from src.modules.animations.Animation import Animation
from src.consts import CELL_SIZE, ROOM_WIDTH, ROOM_HEIGHT, GAME_OVER, GG_HURT, Moves, HeartsTypes
from src.modules.BaseClasses.Based.MoveSprite import MoveSprite
from src.modules.BaseClasses.Based.BaseTear import BaseTear


class TexturesHeroes:
    """
    Clase de texturas para el héroe.
    """
    textures: dict[str, dict] = {
        name:
            {'body':
                {"DOWN": [crop(load_image(f'textures/heroes/body/forward/{name}_{i}.png')) for i in range(10)],
                 "LEFT": [crop(load_image(f'textures/heroes/body/left/{name}_{i}.png')) for i in range(10)],
                 "RIGHT": [crop(load_image(f'textures/heroes/body/right/{name}_{i}.png')) for i in range(10)],
                 "UP": [crop(load_image(f'textures/heroes/body/up/{name}_{i}.png')) for i in range(10)],
                 "death": crop(load_image(f'textures/heroes/death/{name}.png'))
                 },
             'head':
                {"DOWN": crop(load_image(f'textures/heroes/head/{name}_forward.png')),
                 "LEFT": crop(load_image(f'textures/heroes/head/{name}_left.png')),
                 "RIGHT": crop(load_image(f'textures/heroes/head/{name}_right.png')),
                 "UP": crop(load_image(f'textures/heroes/head/{name}_up.png'))}
             }
        for name in ('isaac', 'cain', 'lost')
    }


class ParamsHeroes(TexturesHeroes):
    """
    Clase de configuración del personaje principal.
    """
    settings_body: list[int] = [pg.K_a, pg.K_d, pg.K_w, pg.K_s]                # Configuración de movimiento del héroe
    # settings_head: list[int] = [pg.K_KP_4, pg.K_KP_6, pg.K_KP_8, pg.K_KP_5]    # ajustes de rotación de la cabeza
    settings_head: list[int] = [pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN]    # ajustes de rotación de la cabeza

    directions_head = {settings_head[0]: "LEFT",
                       settings_head[1]: "RIGHT",
                       settings_head[2]: "UP",
                       settings_head[3]: "DOWN"}
    body_images_dict: dict | None  # Diccionario de texturas de movimiento del cuerpo. Clave: Dirección, Valor: Lista de imágenes.
    head_images_dict: dict | None  # Diccionario de texturas de rotación de la cabeza. Clave - Dirección, Valor - Imagen.
    characterizations: dict[str, dict] = {
        'isaac': {
            'hp': 6,
            'speed': 4,
            'damage': 2,
            'is_flying': False,
            'offset': 10
        },
        'cain': {
            'hp': 4,
            'speed': 6,
            'damage': 3,
            'is_flying': False,
            'offset': 10
        },
        'lost': {
            'hp': 1,
            'speed': 4,
            'damage': 2,
            'is_flying': True,
            'offset': 18
        }
    }     # Diccionario de características base de los personajes. Clave - nombre del personaje

    def set_images(self, name: str):
        """
        Configuración de las imágenes del héroe, según su nombre.

        :param name: nombre del héroe.
        """
        self.body_images_dict = self.textures[name]['body']
        self.head_images_dict = self.textures[name]['head']

    def get_characters(self, name: str):
        """
        Devuelve las características iniciales del héroe, según su nombre.

        :param name: nombre del héroe.
        :return: lista de puntos de vida, velocidad, daño, si puede volar o no, y desplazamiento de la cabeza en el eje 0y con respecto al cuerpo.
        """
        return self.characterizations[name].values()

    def set_move_params(self, body: list[int], head: list[int]):
        """
        Configuración de control (cuerpo - movimiento, cabeza - disparo).

        :param body: configuración de movimiento del cuerpo.
        :param head: configuración de rotación de la cabeza.
        """
        self.settings_body = body
        self.settings_head = head


class Head(pg.sprite.Sprite):
    """
    Clase de la cabeza del personaje.

    :param shot_damage: daño del disparo.
    :param tears: lágrimas.
    :param params: parámetros de configuración de rotación e imágenes.
    """
    shot_max_distance: int | float = 5
    shot_speed: int | float = 5
    shot_delay: int | float = 0.5
    tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...]

    def __init__(self,
                 shot_damage: int | float,
                 tears: pg.sprite.AbstractGroup,
                 params: ParamsHeroes):
        super().__init__()

        self.shot_ticks: float = 0                           # tiempo desde el último disparo
        self.shot_damage: float = shot_damage                # daño del disparo
        self.vx_tear: float = 0                              # velocidad de la lagrima a lo largo del eje 0x
        self.vy_tear: float = 0                              # velocidad de la lagrima a lo largo del eje 0y
        self.player_speed: tuple[float, float] = 0, 0        # velocidad actual del personaje (para desviar una bala cuando corre)

        self.tears = tears
        self.tear_class: Type[BaseTear] = HeroTear

        self.is_rotated = False   # indica si la cabeza está girada

        self.last_name_direction: str = "DOWN"      # última dirección de la cabeza (básicamente, el último botón presionado)
        self.on_directions: list[str, ...] = []     # lista de direcciones activas (esencialmente, una lista de botones presionados)

        self.params_hero = params
        self.image = self.params_hero.head_images_dict["DOWN"]
        self.rect = pg.Rect((0, 0, self.image.get_width(), self.image.get_height()))

    def set_tear_collide_groups(self, tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...]):
        """
        Establece de los grupos en los que la lágrima puede colisionar.

        :param tear_collide_groups: tupla de grupos en los que la lágrima puede colisionar.
        """
        self.tear_collide_groups = tear_collide_groups

    def settings_vx_vy_tear(self):
        """
        Configuración de la velocidad de la lágrima.
        """
        if self.is_rotated:
            if self.last_name_direction in ["LEFT", "RIGHT"]:
                self.vx_tear = self.shot_speed if self.last_name_direction == "RIGHT" else -self.shot_speed
                # if self.player_speed[1] != 0:
                self.vy_tear += self.player_speed[1] * 0.3  # constante obtenida empíricamente
            elif self.last_name_direction in ["UP", "DOWN"]:
                self.vy_tear = self.shot_speed if self.last_name_direction == "DOWN" else -self.shot_speed
                # if self.player_speed[0] != 0:
                self.vx_tear += self.player_speed[0] * 0.3  # constante obtenida empíricamente

    def set_player_speed(self, vx: int | float, vy: int | float):
        """
        Guarda (¡no cambia!) la velocidad del personaje (necesaria para desviar una bala cuando se mueve).
        
        :param vx: velocidad en el eje 0x.
        :param vy: velocidad en el eje 0y.
        """
        self.vy_tear, self.vx_tear = 0, 0
        self.player_speed = vx, vy

    def update(self, delta_t) -> None:
        """
        Actualización del fotograma.

        :param delta_t: tiempo desde el último fotograma.
        """
        self.shot_ticks += delta_t
        if self.shot_ticks >= self.shot_delay and self.is_rotated:
            self.shot()
        self.tears.update(delta_t)

    def shot(self) -> None:
        """
        Disparo.
        """
        self.shot_ticks = 0
        self.settings_vx_vy_tear()
        self.tear_class((0, 0), self.rect.center, int(self.shot_damage), self.shot_max_distance,
                        self.vx_tear, self.vy_tear, self.tear_collide_groups, self.tears)

    def set_directions(self, direction: str, is_down: bool):
        self.on_directions.append(direction) if is_down else self.on_directions.remove(direction)
        if self.on_directions:
            self.last_name_direction, self.is_rotated = self.on_directions[-1], True
        else:
            self.last_name_direction, self.is_rotated = "DOWN", False
        self.animating()

    def animating(self):
        """
        Rotación de la cabeza.
        """
        self.image = self.params_hero.head_images_dict[self.last_name_direction]

    def draw_tears(self, screen: pg.Surface):
        """
        Dibujo de las lágrimas.
        """
        self.tears.draw(screen)


class Player(MoveSprite):
    """
    Clase del personaje principal.

    :param name: nombre del personaje seleccionado.
    """
    death: pg.Surface | None = None
    death_sound = load_sound("sounds/isaac_death2.mp3")  # mover
    hurt_sounds: list[pg.mixer.Sound] = [load_sound(f"sounds/isaac_hurt{i}.mp3") for i in range(1, 4)]

    a: float = 0.35  # Aceleración. Determinada empíricamente

    def __init__(self, name: str):

        center_room = ROOM_WIDTH // 2, ROOM_HEIGHT // 2
        super().__init__(center_room, (), acceleration=self.a)
        self.params_hero = ParamsHeroes()
        self.params_hero.set_images(name)
        self.death = self.params_hero.body_images_dict['death']

        self.indexes = {"DOWN": 0, "LEFT": 0, "RIGHT": 0, "UP": 0}  # cantidad de cuadros/fotogramas transcurridos en cada dirección

        self.tears = pg.sprite.Group()  # lagrimas
        self.max_red_hp, self.max_speed, damage, self.is_flying, self.offset = self.params_hero.get_characters(name)
        self.head = Head(damage, self.tears, self.params_hero)  # cabeza del personaje

        self.collide_groups: tuple[pg.sprite.AbstractGroup, ...] | None = None  # Grupos con los que el personaje principal puede chocar.
        self.player_sprites = pg.sprite.LayeredUpdates()
        self.player_sprites.add(self, layer=1)
        self.player_sprites.add(self.head, layer=2)

        # variables varias
        self.damage_from_blow: int = 1                  # daño de la explosión a sí mismo
        self.count_cadrs: int = 0                       # cantidad de cuadros/fotogramas transcurridos (para animación)
        self.score: int = 0                             # cantidad de puntos

        # variables de vida
        self.red_hp: int = self.max_red_hp              # número de HP rojos (mitades de corazón)
        self.blue_hp: int = 0                           # similar al rojo, solo azul
        self.black_hp: int = 0                          # similar al rojo, solo negro

        self.count_bombs: int = 3                       # número de bombas
        self.count_key: int = 0                         # numero de llaves
        self.count_money: int = 10                       # número de monedas/dinero

        # temporizadores
        self.use_bombs_delay: int | float = 1           # intervalo entre activaciones de bombas
        self.use_bombs_ticks: float = 0                 # tiempo desde la última activación de bomba
        self.timer_hurt: float = 2                      # intervalo entre recibir daño
        self.timer: float = 2                           # tiempo desde el último daño recibido
        self.score_sub_tick: float = 1                  # intervalo de eliminación de puntos
        self.score_sub_timer: float = 0                 # tiempo desde que se retiraron los últimos puntos

        # flags para movimiento
        self.flag_move_down: bool = False               # abajo
        self.flag_move_left: bool = False               # izquierda
        self.flag_move_right: bool = False              # derecha
        self.flag_move_up: bool = False                 # arriba
        self.is_move: bool = False                      # ¿Se está moviendo el personaje principal?
        self.is_alive: bool = True                      # ¿Está vivo el personaje?

        # flags de colisión
        self.x_collide: bool = False                    # La colisión se produjo a la izquierda o a la derecha. (x)
        self.y_collide: bool = False                    # La colisión se produjo desde arriba o desde abajo. (y)

        # flags de direccion
        self.last_name_direction: str = "DOWN"          # En el último fotograma la animación estaba en esta dirección.
        self.move_last_direction: str | None = None     # En el último fotograma el personaje principal se movía en esta dirección

        self.image = self.params_hero.body_images_dict["DOWN"][0]
        self.image = crop(self.image)
        size = max(self.image.get_width(), self.image.get_height())
        self.rect = pg.Rect((0, 0, size, size))

        self.soul = Soul()                              # alma personaje principal

    def hurt(self, damage: int):
        """
        Recibir daño.

        :param damage: daño recibido.
        """
        if self.timer > self.timer_hurt:
            if self.blue_hp:
                self.blue_hp -= damage
            elif self.black_hp:
                self.black_hp -= damage
            else:
                self.red_hp -= damage
            self.timer = 0
            if self.red_hp > 0:
                random.choice(Player.hurt_sounds).play()
            pg.event.post(pg.event.Event(GG_HURT))

    def kill_tears(self):
        """
        Eliminación de lágrimas (al cambiar de habitación).
        """
        self.head.tears.empty()

    def update_timer(self, delta_t):
        """
        Actualización de los temporizadores.

        :param delta_t: tiempo desde el último fotograma.
        """
        self.timer += delta_t
        self.score_sub_timer += delta_t
        if self.score_sub_timer >= self.score_sub_tick:
            self.score -= 1
            self.score_sub_timer -= self.score_sub_tick

    def blow(self):
        """
        Obtener daño de una explosión de bomba.
        """
        self.hurt(self.damage_from_blow)

    def setting_flags(self, key, is_down: bool):
        """
        Configuración de las flags de movimiento.

        :param key: tecla presionada o soltada.
        :param is_down: indica si la tecla está presionada.
        """

        if key == self.params_hero.settings_body[0]:
            self.flag_move_left = is_down
        elif key == self.params_hero.settings_body[1]:
            self.flag_move_right = is_down
        elif key == self.params_hero.settings_body[2]:
            self.flag_move_up = is_down
        elif key == self.params_hero.settings_body[3]:
            self.flag_move_down = is_down

    def animating(self):
        """
        Animación de movimiento.
        """
        if self.count_cadrs == 0:
            last_name = self.last_name_direction
            peremennaya = self.indexes[last_name] + 1
            self.indexes = {"DOWN": 0, "LEFT": 0, "RIGHT": 0, "UP": 0,
                            last_name: peremennaya % len(self.params_hero.body_images_dict["DOWN"])}

            if self.is_move:
                self.image = self.params_hero.body_images_dict[last_name][self.indexes[last_name]]
            else:
                self.image = self.params_hero.body_images_dict["DOWN"][0]

    def settings_move_speed(self, delta_t: float):
        """
        Configuración de la velocidad de movimiento, según las teclas presionadas.

        :param delta_t: tiempo desde el último fotograma.
        """
        max_speed, a = self.max_speed, self.a * CELL_SIZE
        if (self.flag_move_up or self.flag_move_down) and not \
                (self.flag_move_up and self.flag_move_down) and \
                (self.flag_move_left or self.flag_move_right) and not \
                (self.flag_move_left and self.flag_move_right) and not \
                (self.x_collide or self.y_collide):
            max_speed *= 0.7  # cos 45
            a *= 0.7  # sin 45

        if self.flag_move_up and not self.flag_move_down and not self.y_collide:
            self.vy = max(-max_speed, self.vy - a * delta_t)
        elif self.vy < 0:
            self.vy = min(0, self.vy + a * delta_t)

        if self.flag_move_down and not self.flag_move_up and not self.y_collide:
            self.vy = min(max_speed, self.vy + a * delta_t)
        elif self.vy > 0:
            self.vy = max(0, self.vy - a * delta_t)

        if self.flag_move_left and not self.flag_move_right and not self.x_collide:
            self.vx = max(-max_speed, self.vx - a * delta_t)
        elif self.vx < 0:
            self.vx = min(0, self.vx + a * delta_t)

        if self.flag_move_right and not self.flag_move_left and not self.x_collide:
            self.vx = min(max_speed, self.vx + a * delta_t)
        elif self.vx > 0:
            self.vx = max(0, self.vx - a * delta_t)

        if self.flag_move_up or self.flag_move_down:
            self.last_name_direction = "UP" if self.flag_move_up else "DOWN"
        elif self.flag_move_right or self.flag_move_left:
            self.last_name_direction = "LEFT" if self.flag_move_left else "RIGHT"

        self.is_move = self.vx != 0 or self.vy != 0

    def collide(self, other):
        """
        Colisión con algo.

        :param other: lo con lo que ha ocurrido la colisión.
        """
        if not MoveSprite.collide(self, other):
            return

        if isinstance(other, BaseTear) and other not in self.tears.sprites():
            self.hurt(other.damage)
            other.destroy()

    def reset_collides(self):
        """
        Resetear los flags de colisión.
        """
        self.x_collide = self.y_collide = False

    def move_back(self, rect: pg.Rect):
        """
        Manejo de colisiones y cambio de velocidades al colisionar.

        :param rect: Rectángulo con el que hubo colisión.
        """

        direction = get_direction(self.rect, rect)

        self.y_collide = direction in (Moves.UP, Moves.DOWN) or self.y_collide
        self.x_collide = direction in (Moves.LEFT, Moves.RIGHT) or self.x_collide

        if direction == Moves.RIGHT and self.vx > 0:
            self.move_last_direction = "UP" if self.vy < 0 else "DOWN"
            if self.vy:
                self.vy = (-1 if self.vy < 0 else 1) * (abs(self.vy) + abs(self.vx * 0.7))
            self.vx = 0

        elif direction == Moves.LEFT and self.vx < 0:
            self.move_last_direction = "UP" if self.vy < 0 else "DOWN"
            if self.vy:
                self.vy = (-1 if self.vy < 0 else 1) * (abs(self.vy) + abs(self.vx * 0.7))
            self.vx = 0

        elif direction == Moves.UP and self.vy < 0:
            self.move_last_direction = "LEFT" if self.vx < 0 else "RIGHT"
            if self.vx:
                self.vx = (-1 if self.vx < 0 else 1) * (abs(self.vx) + abs(self.vy * 0.7))
            self.vy = 0

        elif direction == Moves.DOWN and self.vy > 0:
            self.move_last_direction = "LEFT" if self.vx < 0 else "RIGHT"
            if self.vx:
                self.vx = (-1 if self.vx < 0 else 1) * (abs(self.vx) + abs(self.vy * 0.7))
            self.vy = 0

        if direction in (Moves.TOPLEFT, Moves.TOPRIGHT) and self.vy < 0:
            self.y_collide = True
            if self.vx != 0:
                self.vy = 0
        if direction in (Moves.BOTTOMLEFT, Moves.BOTTOMRIGHT) and self.vy > 0:
            self.y_collide = True
            if self.vx != 0:
                self.vy = 0
        if direction in (Moves.TOPLEFT, Moves.BOTTOMLEFT) and self.vx < 0:
            self.x_collide = True
            if self.vy != 0:
                self.vx = 0
        if direction in (Moves.TOPRIGHT, Moves.BOTTOMRIGHT) and self.vx > 0:
            self.x_collide = True
            if self.vy != 0:
                self.vx = 0

        if self.x_collide:
            self.x_center = self.x_center_last
            self.rect.centerx = self.x_center
        if self.y_collide:
            self.y_center = self.y_center_last
            self.rect.centery = self.y_center

        if self.vx > self.max_speed:
            self.vx = self.max_speed
        elif self.vx < -self.max_speed:
            self.vx = -self.max_speed
        if self.vy > self.max_speed:
            self.vy = self.max_speed
        elif self.vy < -self.max_speed:
            self.vy = -self.max_speed

    def update_room_groups(self, required_groups, hero_collide_groups, tear_collide_groups) -> None:
        """
        Actualiza los grupos de colisión al cambiar de habitación / piso.

        :param required_groups: grupo de colisión para el personaje volador.
        :param hero_collide_groups: grupo de colisión para el personaje caminante.
        :param tear_collide_groups: grupos en los que las lágrimas del personaje pueden colisionar.
        """
        self.head.set_tear_collide_groups(tear_collide_groups)
        self.collide_groups = required_groups if self.is_flying else hero_collide_groups

    def pickup_heart(self, count: int, heart_type: HeartsTypes) -> bool:
        """
        Subir corazón.

        :param count: cantidad de corazones subidos.
        :param heart_type: tipo de corazón.
        :return: True - se puede subir el corazón. False - la salud está llena.
        """
        if heart_type == HeartsTypes.RED:
            if self.red_hp >= self.max_red_hp:
                return False
            self.red_hp += count
            self.red_hp = min(self.red_hp, self.max_red_hp)
        elif heart_type == HeartsTypes.BLUE:
            self.blue_hp += count
        elif heart_type == HeartsTypes.BLACK:
            self.black_hp += count
        return True

    def is_buy(self, count: int, price: int, heart_type: HeartsTypes | None) -> bool:
        """
        Compra de un objeto.

        :param count: cantidad de corazones subidos.
        :param price: precio.
        :param heart_type: tipo de corazón.
        :return: True - compra exitosa. False - no se puede comprar.
        """
        if self.count_money >= price:
            if heart_type:
                if not self.pickup_heart(count, heart_type):
                    return False
            self.count_money -= price
            return True
        return False

    def move_to_cell(self, xy_pos):
        """
        Mover al personaje principal a la celda deseada al cambiar de habitación.

        :param xy_pos: coordenadas de la celda.
        """
        x, y = cell_to_pixels(xy_pos)
        self.x_center = x
        self.x_center_last = x
        self.y_center = y
        self.y_center_last = y
        self.vx, self.vy = 0, 0

    def set_flags_move(self, event: pg.event.Event, is_down: bool):
        """
        Configuración de las flags de movimiento.

        :param event: tecla presionada.
        :param is_down: True - tecla presionada. False - tecla soltada.
        """
        key = event.key
        if key in self.params_hero.settings_body:
            self.setting_flags(key, is_down)

        elif key in self.params_hero.settings_head:
            self.head.set_directions(self.params_hero.directions_head[key], is_down)

    def reset_speed(self):
        """
        Reiniciar flags y velocidades.
        """
        self.flag_move_up = False
        self.flag_move_left = False
        self.flag_move_right = False
        self.flag_move_down = False
        self.vx, self.vy = 0, 0

    def update(self, delta_t: float):
        """
        Actualización de fotograma.

        :param delta_t: tiempo desde el último fotograma.
        """
        if self.red_hp > 0:
            self.use_bombs_ticks += delta_t
            self.count_cadrs += 1
            self.count_cadrs %= 3

            self.animating()
            self.head.update(delta_t)
            self.move(delta_t, use_a=False)
            self.update_timer(delta_t)
            self.reset_collides()
            self.settings_move_speed(delta_t)
            self.check_collides()

            self.head.set_player_speed(*self.get_speed())
            coords = self.rect.midtop
            self.head.rect.center = coords[0], coords[1] - self.offset
            # self.offset se ha ajustado en la práctica (para que la cabeza se vea normal)
        else:
            if self.is_alive:
                self.image = self.death
                self.player_sprites.remove(self.head)
                self.soul.set_coords(self.rect.center)
                Player.death_sound.play()
            self.is_alive = False
            self.soul.update(delta_t)
            if self.soul.is_end_animation():
                pg.event.post(pg.event.Event(GAME_OVER, {'score': self.score}))

    def activate_bombs(self) -> bool:
        """
        Activación de la bomba.

        :return: True - la bomba ha sido activada. False - no hay suficientes bombas o se ha utilizado recientemente.
        """
        if self.count_bombs > 0 and self.use_bombs_ticks > self.use_bombs_delay:
            self.count_bombs -= 1
            self.use_bombs_ticks = 0
            return True
        return False

    def scoring_points(self, counts: int):
        """
        Conteo de puntos.

        :param counts: cantidad de puntos.
        """
        self.score += counts

    def get_speed(self) -> tuple[int, int]:
        """
        Retorna la velocidad del personaje.

        :return: una tupla de velocidades (primero en el eje x, luego en el eje y).
        """
        return self.vx, self.vy

    def render(self, screen: pg.Surface):
        """
        Renderiza el personaje y sus lágrimas.

        :param screen: superficie en la que se debe dibujar.
        """
        self.player_sprites.draw(screen)
        self.head.draw_tears(screen)
        if not self.is_alive:
            self.soul.render(screen)


class Soul(pg.sprite.Sprite):
    """
    Clase Soul.
    """
    start_image = load_image('textures/heroes/soul/soul0.png')
    images = load_image('textures/heroes/soul/move_soul.png')
    fps_animation = 15

    def __init__(self):
        super().__init__()
        self.image = self.start_image
        self.animation = Animation(self.images, 10, 1, self.fps_animation, False)
        self.xy_pos: tuple[int, int] | None = None  # coordenadas actuales (х, у)
        self.start_x_pos: int | None = None         # coordenada inicial a lo largo del eje 0x
        self.vx, self.vy = -50, -50                 # velocidad
        self.timer: int | float = 3                 # duración de la animación

    def set_coords(self, xy_pos: tuple[int, int]):
        """
        Establece el punto inicial del alma.

        :param xy_pos: tupla de coordenadas de la muerte (x, y).
        """
        self.xy_pos = xy_pos
        self.start_x_pos = xy_pos[0]

    def is_end_animation(self) -> bool:
        """
        ¿Ha terminado la animación de muerte?

        :return: True - la animación ha terminado. False - aún no ha terminado.
        """
        return self.timer <= 0

    def update(self, delta_t):
        """
        Actualización del fotograma.

        :param delta_t: tiempo transcurrido desde el último fotograma.
        """
        if self.timer > 0:
            self.animation.update(delta_t)
            self.image = self.animation.image
            self.move(delta_t)
            self.timer -= delta_t

    def move(self, delta_t):
        """
        Movimiento del alma.

        :param delta_t: tiempo transcurrido desde el último fotograma.
        """
        if self.xy_pos[0] <= self.start_x_pos - CELL_SIZE // 4 or self.xy_pos[0] >= self.start_x_pos + CELL_SIZE // 4:
            self.vx *= -1
        self.xy_pos = self.xy_pos[0] + self.vx * delta_t, self.xy_pos[1] + self.vy * delta_t

    def render(self, screen: pg.Surface):
        """
        Renderiza el alma.

        :param screen: superficie en la que se debe renderizar.
        """
        if self.timer > 0:
            screen.blit(self.image, self.xy_pos)


class HeroTear(BaseTear):
    """
    Clase de lágrimas del personaje principal.

    :param xy_pos: Posición en la habitación.
    :param xy_pixels: Coordenada de aparición en píxeles, centro de la lágrima.
    :param damage: Daño.
    :param max_distance: Distancia máxima de vuelo en celdas (convertida a píxeles/segundo).
    :param vx: Velocidad horizontal en celdas (convertida a píxeles/segundo).
    :param vy: Velocidad vertical en celdas (convertida a píxeles/segundo).
    :param collide_groups: Grupos con los que se debe comprobar la colisión.
    :param groups: Grupos de sprites.
    :param is_friendly: Ignora al personaje principal.
    """
    pop_animation = BaseTear.all_ends.subsurface(0, 0, BaseTear.width, BaseTear.height)
    fps_animation = 30

    def __init__(self,
                 xy_pos: tuple[int, int],
                 xy_pixels: tuple[int, int],
                 damage: int,
                 max_distance: int | float,
                 vx: int | float,
                 vy: int | float,
                 collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup):
        is_friendly = True
        BaseTear.__init__(self, xy_pos, xy_pixels, damage, max_distance, vx, vy, collide_groups, *groups,
                          is_friendly=is_friendly)

        self.animation = Animation(HeroTear.pop_animation, 16, 1, self.fps_animation, True)
        self.set_image()
        self.set_rect()

    def set_image(self):
        """
        Establece la imagen de la lágrima.
        """
        max_size = len(BaseTear.all_tears[0]) - 1
        self.image = crop(BaseTear.all_tears[0][min(int(self.damage + 2), max_size)])
