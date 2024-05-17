import math
from src.consts import RoomsTypes, Moves
from collections import deque

def distance_between_start_and_boss(rooms: list[list[RoomsTypes]]) -> int:
    """
    Calcular la distancia entre la sala de inicio y la sala del jefe,
    contando el número mínimo de salas necesarias para llegar.
    Algortimo de búsqueda en anchura.

    :param rooms: una matriz bidimensional de valores de RoomsTypes.
    :return: la distancia entre la sala de inicio y la sala del jefe.
    """
    map_width, map_height = len(rooms[0]), len(rooms)
    start_pos = math.ceil(map_width / 2) - 1, math.ceil(map_height / 2) - 1
    visited = set()  # Para evitar visitar la misma sala más de una vez
    queue = deque([(start_pos, 0)])  # Iniciar la cola con la posición de inicio y la distancia 0

    while queue:
        (x, y), distance = queue.popleft()
        visited.add((x, y))

        # Si encontramos la sala del jefe, devolvemos la distancia
        if rooms[y][x] == RoomsTypes.BOSS:
            return distance

        # Obtener vecinos no vacíos ni secretos
        neighbors = [(x+dx, y+dy) for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Movimientos arriba, derecha, abajo, izquierda
                     if 0 <= x+dx < map_width and 0 <= y+dy < map_height and rooms[y+dy][x+dx] not in [RoomsTypes.EMPTY, RoomsTypes.SECRET]]

        # Añadir vecinos no visitados a la cola
        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append((neighbor, distance + 1))

    # Si no se encuentra un camino hasta la sala del jefe se devuelve 0
    return 0

def get_number_of_roomtype(rooms: list[list[RoomsTypes]], especial: RoomsTypes) -> int:
    """
    Obtener el número de salas de un tipo en la matriz de habitaciones.

    :param rooms: una matriz bidimensional de valores de RoomsTypes.
    :return: el número de salas secretas.
    """
    return sum(room == especial for row in rooms for room in row)

def exists_special_room(rooms: list[list[RoomsTypes]], especial: RoomsTypes) -> bool:
    """
    Comprueba si existe una sala especial en la matriz de habitaciones.

    :param rooms: una matriz bidimensional de valores de RoomsTypes.
    :param especial: el tipo de sala especial a buscar.
    :return: True si existe una sala especial, False en caso contrario.
    """
    return any(room == especial for row in rooms for room in row)


def count_rooms(rooms: list[list[RoomsTypes]]) -> int:
    """
    Contar el número de habitaciones en la matriz de habitaciones.

    :param rooms: una matriz bidimensional de valores de RoomsTypes.
    :return: el número de habitaciones que hay en el mapa.
    """
    return sum(room != RoomsTypes.EMPTY for row in rooms for room in row)