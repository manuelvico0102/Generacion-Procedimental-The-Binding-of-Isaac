"""
Generador de piso.
Llamar a generate_level(width, height, rooms) para obtener un mapa del nivel.
"""

import random
import math
import collections

from src.utils.graph import make_neighbors_graph
from src.consts import RoomsTypes, Moves

from src.modules.levels.algoritmoGenetico import steady_state_genetic_algorithm, generational_genetic_algorithm

# Optimice esto trazando una ruta desde el inicio hasta todos los puntos posibles y verificando que todos los puntos estén involucrados.
def all_rooms_have_path_to_start(rooms: list[list[RoomsTypes | str]], *, ignore_secret: bool = True) -> bool:
    """
     Comprobando si todas las habitaciones tienen un camino a la sala de inicio.

     :param rooms: matriz bidimensional de valores de RoomsTypes.
     :param ignore_secret: si se ignora la habitación secreta.
     :return: ¿Todas las habitaciones tienen un camino hacia la sala de inicio?
    """
    graph = make_neighbors_graph(rooms, ignore_secret=ignore_secret)
    ignored = (RoomsTypes.EMPTY, RoomsTypes.SECRET)
    for y, row in enumerate(rooms):
        for x, col in enumerate(row):
            if rooms[y][x] not in ignored:
                if not has_path_to_start((x, y), rooms, ignore_secret=ignore_secret, graph=graph):
                    return False
    return True


def has_path_to_start(start_pos: tuple[int, int], rooms: list[list[RoomsTypes | str]],
                      *,
                      ignore_secret: bool = True, graph: dict[tuple[int, int], list[tuple[int, int]]] = None) -> bool:
    """
     Comprobar si es posible caminar desde la celda hasta la sala de salida.

     :param start_pos: La posición de la celda desde la que comienza la ruta.
     :param rooms: matriz bidimensional de valores de RoomTypes.
     :param ignore_secret: si se ignora la habitación secreta.
     :param graph: un diccionario similar a un gráfico (transmitido para no recrearlo para verificar cada habitación).
     :return: ¿Todas las habitaciones tienen un camino hacia la sala de inicio?
     """
    map_width, map_height = len(rooms[0]), len(rooms)
    end_pos = math.ceil(map_width / 2) - 1, math.ceil(map_height / 2) - 1,
    if graph is None:
        graph = make_neighbors_graph(rooms, ignore_secret=ignore_secret)
    queue = collections.deque([start_pos])
    visited: dict[tuple[int, int], tuple[int, int]] = {start_pos: None}
    while queue:
        current_cell = queue.popleft()
        if current_cell == end_pos:
            break
        next_cells = graph.get(current_cell, [])
        for next_cell in next_cells:
            if next_cell not in visited.keys():
                queue.append(next_cell)
                visited[next_cell] = current_cell
    return end_pos in visited.keys()


def set_secret_room(rooms: list[list[RoomsTypes | str]]) -> bool:
    """
    Montar una habitación secreta.

    :param rooms: matriz bidimensional de valores de RoomsTypes.
    :return: ¿Se instaló correctamente la habitación secreta?
    """
    graph = make_neighbors_graph(rooms)
    is_okay = False

    # Primero, coloca un secreto donde hay 4 vecinos, luego donde hay 3, luego donde hay 2.
    # Ahora funciona más lento :)
    for neighbors_rooms in range(4, 1, -1):
        secrets = [room for room in graph if len(graph[room]) >= neighbors_rooms
                   and rooms[room[1]][room[0]] == RoomsTypes.DEFAULT]
        random.shuffle(secrets)
        for x, y in secrets:
            rooms[y][x] = RoomsTypes.SECRET
            if all_rooms_have_path_to_start(rooms):
                is_okay = True
                break
            else:
                rooms[y][x] = RoomsTypes.DEFAULT
        if is_okay:
            break
    return is_okay


def set_special_rooms(rooms: list[list[RoomsTypes | str]]) -> bool:
    """
    Disposición de salas especiales (tesorería, tienda, jefe).

    :param rooms: matriz bidimensional de valores de RoomsTypes.
    :return: ¿Se han instalado correctamente todas las salas especiales?
    """
    # Busque habitaciones con un vecino para configurar una tesorería, una tienda y una sala de jefe
    graph = make_neighbors_graph(rooms, ignore_secret=True)
    solo = [room for room in graph if len(graph[room]) == 1 and rooms[room[1]][room[0]] == RoomsTypes.DEFAULT]
    if len(solo) < 3:
        return False

    # Configura la sala del jefe lo más lejos posible de la ubicación de generación
    map_width, map_height = len(rooms[0]), len(rooms)
    spawn_x, spawn_y = math.ceil(map_width / 2) - 1, math.ceil(map_height / 2) - 1
    boss_x, boss_y = max(solo, key=lambda c: math.sqrt((spawn_x - c[0]) ** 2 + (spawn_y - c[1]) ** 2))
    rooms[boss_y][boss_x] = RoomsTypes.BOSS
    solo.remove((boss_x, boss_y))

    # Colocación aleatoria de tienda y tesoro.
    random.shuffle(solo)
    for coords, room_type in zip(solo, (RoomsTypes.SHOP, RoomsTypes.TREASURE)):
        x, y = coords
        rooms[y][x] = room_type

    return True


def set_other_rooms(rooms: list[list[RoomsTypes | str]]) -> bool:
    """
     Disposición de salas distintas a las de generación y predeterminadas.

     :param rooms: matriz bidimensional de valores de RoomsTypes.
     :return: ¿Se han instalado correctamente todas las salas?
    """
    # Configuración de la sala secreta
    if not set_secret_room(rooms):
        return False

    # Configuración de las salas especiales
    if not set_special_rooms(rooms):
        return False

    return True


def set_default_rooms(rooms: list[list[RoomsTypes | str]], room_numbers: int) -> None:
    """
     Colocar RoomsTypes.DEFAULT y RoomsTypes.SPAWN en un mapa vacío.

     :param rooms: una matriz bidimensional de valores de RoomsTypes (en este caso, RoomsTypes.EMPTY).
     :param room_numbers: cuántas habitaciones se deben llenar con el valor de habitación predeterminado.
     :retorno: Ninguno
    """

    map_width, map_height = len(rooms[0]), len(rooms)
    cur_x, cur_y = math.ceil(map_width / 2) - 1, math.ceil(map_height / 2) - 1
    room_numbers -= 1
    rooms[cur_y][cur_x] = RoomsTypes.SPAWN
    moves = [move.value for move in Moves]
    # Un intento de crear un algoritmo de "perro corriendo" a partir de un vídeo sobre la generación de niveles en Isaac
    while room_numbers > 0:
        step_x, step_y = random.choice(moves)
        cur_x = max(0, min(map_width - 1, cur_x + step_x))
        cur_y = max(0, min(map_height - 1, cur_y + step_y))
        if rooms[cur_y][cur_x] == RoomsTypes.EMPTY:
            room_numbers -= 1
            rooms[cur_y][cur_x] = RoomsTypes.DEFAULT


def generate_level(map_width: int, map_height: int, room_numbers: tuple[int,int], algorithm: int = 0) -> list[list[RoomsTypes | str]]:
    """
     Generador de piso (nivel).

     :param map_width: ancho del piso.
     :param map_height: altura del piso.
     :param room_numbers: - número de habitaciones teniendo en cuenta la generación, la tienda, el jefe, etc.
     """
    minRooms = room_numbers[0]
    maxRooms = room_numbers[1]

    assert 3 <= map_width <= 10                        # Comprobando el tamaño de la tarjeta
    assert 3 <= map_height <= 10                       # Comprobando el tamaño de la tarjeta
    assert minRooms >= 5                               # Generación, tienda, tesorería, jefe, habitación secreta.
    assert maxRooms < map_width * map_height - 3   # Es posible generar todas las habitaciones.

    rooms = []
    """
    # Implementación inicial del algoritmo de generación de niveles
    successful_generation = False
    while not successful_generation:
        # Generación de niveles hasta que aparezca un diseño adecuado
        rooms = [[RoomsTypes.EMPTY] * map_width for _ in range(map_height)]
        set_default_rooms(rooms, room_numbers)
        successful_generation = set_other_rooms(rooms)"""
    
    if algorithm == 0:
        rooms = steady_state_genetic_algorithm(10, map_width, map_height, room_numbers, 50)
    else:
        rooms = generational_genetic_algorithm(10, map_width, map_height, room_numbers, 50)
        
    assert rooms
    return rooms


def print_map(rooms: list[list[RoomsTypes | str]]) -> None:
    """
     Salida del mapa a la consola.

     :param rooms: matriz bidimensional de valores de RoomsTypes.
     :return: Ninguno.
     """
    for row in rooms:
        for col in row:
            print(col.value.center(8, ' '), end=' ')
        print()


def main():
    mapa = generate_level(10, 10, 50)
    print_map(mapa)


if __name__ == '__main__':
    main()
