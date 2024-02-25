import collections

from src import consts


def valid_coords(x: int, y: int, width: int, height: int) -> bool:
    """
    Comprueba si las coordenadas están fuera de los límites de la lista.

    :param x: Coordenada de la columna.
    :param y: Coordenada de la fila.
    :param width: Ancho de la matriz bidimensional.
    :param height: Altura de la matriz bidimensional.
    :return: Si las coordenadas son válidas.
    """
    return width > x >= 0 and height > y >= 0


def get_neighbors_coords(x: int, y: int, rooms: list[list[consts.RoomsTypes | str]],
                         *,
                         ignore_secret: bool = False,
                         use_diagonals: bool = False) -> list[tuple[int, int]]:
    """
    Obtener las coordenadas de las celdas vecinas a las que se puede acceder.

    :param x: Coordenada de la columna.
    :param y: Coordenada de la fila.
    :param rooms: Matriz bidimensional de valores de tipos de habitaciones.
    :param ignore_secret: Ignorar habitaciones secretas.
    :param use_diagonals: Utilizar movimientos diagonales.
    :return: Lista de todas las coordenadas de las celdas vecinas a las que se puede acceder.
    """
    moves = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    if use_diagonals:
        moves += [(1, 1), (-1, -1), (1, -1), (-1, 1)]
    map_width, map_height = len(rooms[0]), len(rooms)
    ignored = [consts.RoomsTypes.EMPTY]
    if ignore_secret:
        ignored.append(consts.RoomsTypes.SECRET)
    return [(x + i, y + j) for i, j in moves if
            valid_coords(x + i, y + j, map_width, map_height) and rooms[y + j][x + i] not in ignored]


# Intentar mover en diagonal si las celdas vecinas en esa dirección están libres
# Tal vez sea necesario experimentar con la creación del grafo
def make_path_to_cell(graph: dict[tuple[int, int]],
                      xy_start: tuple[int, int],
                      xy_end: tuple[int, int]) -> bool | list[tuple[int, int]]:
    """
    Comprueba si es posible llegar desde una celda hasta la habitación de inicio.

    :param graph: Diccionario similar a un grafo que representa las celdas de la habitación.
    :param xy_start: Celda de inicio.
    :param xy_end: Celda de destino.
    :return: Lista de celdas del camino o False.
    """
    queue = collections.deque([xy_start])
    visited: dict[tuple[int, int], tuple[int, int]] = {xy_start: None}
    while queue:
        current_cell = queue.popleft()
        if current_cell == xy_end:
            break
        next_cells = graph.get(current_cell, [])
        for next_cell in next_cells:
            if next_cell not in visited.keys():
                queue.append(next_cell)
                visited[next_cell] = current_cell

    if xy_end not in visited.keys():
        return False

    way: list[tuple[int, int]] = []
    path_segment = xy_end
    while path_segment and path_segment in visited:
        way.append(path_segment)
        path_segment = visited[path_segment]
    way.reverse()
    return way


def make_neighbors_graph(rooms: list[list[consts.RoomsTypes | str]],
                         ignore_secret: bool = False,
                         use_diagonals: bool = False) -> dict[tuple[int, int], list[tuple[int, int]]]:
    """
    Generación del grafo de vecinos.
    Se utiliza tanto para construir el grafo de todo el mapa como para construir el grafo de una habitación específica.
    Para esto, se debe pasar una matriz de habitaciones con los siguientes valores:
        consts.RoomTypes.DEFAULT, si se puede caminar en la celda;
        consts.RoomTypes.EMPTY, si no se puede caminar en la celda.

    :param rooms: Matriz bidimensional de valores de tipos de habitaciones.
    :param ignore_secret: Ignorar habitación secreta.
    :param use_diagonals: Utilizar movimientos diagonales.
    :return: Diccionario similar a un grafo (coordenadas: lista de coordenadas de los vecinos).
    """
    graph = collections.defaultdict(list)  # dict[tuple[int, int], list[tuple[int, int]]]
    # Celda -> Lista de vecinos a los que se puede acceder
    for y, row in enumerate(rooms):
        for x, col in enumerate(row):
            if col != consts.RoomsTypes.EMPTY:
                graph[(x, y)].extend(get_neighbors_coords(x, y, rooms,
                                                          ignore_secret=ignore_secret, use_diagonals=use_diagonals))
    return graph
