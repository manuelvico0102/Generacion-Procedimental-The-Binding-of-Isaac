"""
Generador de piso.
Llamar a generate_level(width, height, rooms) para obtener un mapa del nivel.
"""

from src.consts import RoomsTypes
from src.modules.levels.algoritmoGenetico import steady_state_genetic_algorithm, generational_genetic_algorithm, set_default_rooms, set_other_rooms

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
    map = generate_level(10, 10, [5, 10])
    print_map(map)


if __name__ == '__main__':
    main()
