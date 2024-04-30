import random
import math
import collections
from enum import Enum
from src.consts import RoomsTypes, Moves
from src.utils.graph import make_neighbors_graph
import src.utils.comprobaciones as comprobaciones

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


def generate_level(map_width: int, map_height: int, room_numbers: int) -> list[list[RoomsTypes | str]]:
    """
     Generador de piso (nivel).

     :param map_width: ancho del piso.
     :param map_height: altura del piso.
     :param room_numbers: - número de habitaciones teniendo en cuenta la generación, la tienda, el jefe, etc.
     """
    assert 3 <= map_width <= 10                        # Comprobando el tamaño de la tarjeta
    assert 3 <= map_height <= 10                       # Comprobando el tamaño de la tarjeta
    assert room_numbers >= 5                           # Generación, tienda, tesorería, jefe, habitación secreta.
    assert room_numbers < map_width * map_height - 3   # Es posible generar todas las habitaciones.

    rooms = []
    successful_generation = False
    while not successful_generation:
        # Generación de niveles hasta que aparezca un diseño adecuado
        rooms = [[RoomsTypes.EMPTY] * map_width for _ in range(map_height)]
        set_default_rooms(rooms, room_numbers)
        successful_generation = set_other_rooms(rooms)
    assert rooms
    return rooms


def generate_initial_population(population_size: int, map_width: int, map_height: int, room_numbers: int) -> list:
    population = []
    for _ in range(population_size):
        rooms = generate_level(map_width, map_height, room_numbers)
        population.append(rooms)
    return population

def fitness(rooms: list[list[RoomsTypes]]) -> float:
    # Comprobar conectividad
    # ¿Distancia entre la sala de inicio y la sala del jefe? + cantidad de bifurcaciones
    # ¿Número de habitaciones secretas accesibles?
    # En caso de que de malos resultados puedo cambiar la generacion inicial para que haya tiendas y habitaciones secretas desde un principio
    puntuacion = 0

    if all_rooms_have_path_to_start(rooms):
        puntuacion += 100

    if(comprobaciones.exists_special_room(rooms, RoomsTypes.BOSS)):
        puntuacion += 50
    
    if(comprobaciones.get_number_of_roomtype(rooms, RoomsTypes.BOSS) > 1):
        puntuacion -= 50

    if comprobaciones.exists_special_room(rooms, RoomsTypes.TREASURE):
        puntuacion += 10
    
    if comprobaciones.exists_special_room(rooms, RoomsTypes.SHOP):
        puntuacion += 10

    if comprobaciones.exists_special_room(rooms, RoomsTypes.SECRET):
        puntuacion += 10
        if comprobaciones.get_number_of_roomtype(rooms, RoomsTypes.SECRET) > 1:
            puntuacion += 10

    if comprobaciones.distance_between_start_and_boss(rooms) > 10:
        puntuacion += 10

    
    return puntuacion

def crossover(parent1: list[list[RoomsTypes]], parent2: list[list[RoomsTypes]]) -> list[list[RoomsTypes]]:
    # Cruce por punto de corte (crossover) Este método elige un punto aleatorio en los cromosomas de los padres 
    # y combina las partes antes y después de ese punto para producir los hijos.

    # Seleccionar un punto de corte aleatorio, tanto en el eje x como en el y
    crossover_point_x = random.randint(0, len(parent1[0]) - 1)
    crossover_point_y = random.randint(0, len(parent1) - 1)

    # Crear una nueva matriz para el hijo
    child = [[None] * len(parent1[0]) for _ in range(len(parent1))]

    # Copiar las partes antes y después del punto de corte del primer padre al hijo
    for y in range(len(parent1)):
        for x in range(len(parent1[0])):
            if y < crossover_point_y or (y == crossover_point_y and x <= crossover_point_x):
                child[y][x] = parent1[y][x]
            else:
                child[y][x] = parent2[y][x]
    
    #child = comprobaciones.fix_special_rooms(child)

    return child

def mutate(rooms: list[list[RoomsTypes]], mutation_rate: float) -> list[list[RoomsTypes]]:
    # Intercambio de habitaciones
    # Tal vez sea mejor especificar que no sea una habitación empty

    mutated_rooms = [row[:] for row in rooms]   # Copiar la matriz de habitaciones

    for i in range(len(rooms)):
        for j in range(len(rooms[i])):
            if random.random() < mutation_rate:
                # Seleccionar dos ubicaciones aleatorias distintas
                new_i, new_j = random.randint(0, len(rooms) - 1), random.randint(0, len(rooms[i]) - 1)
                # Intercambiar las salas en las dos ubicaciones seleccionadas
                mutated_rooms[i][j], mutated_rooms[new_i][new_j] = mutated_rooms[new_i][new_j], mutated_rooms[i][j]
    
    return mutated_rooms
