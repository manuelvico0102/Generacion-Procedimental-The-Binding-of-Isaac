import numpy as np
from src import consts

# Definir los tipos de entidades
EMPTY = 0
ROCK = 1
POOP = 2
WEB = 3
FIRE = 4
UNIQUE_OBJECT = 5
ENEMY_1 = 6
ENEMY_2 = 7
ENEMY_3 = 8
SPIKES = 9

def cellular_automatan():
    """
    Crea un mapa de celdas para la generación de entidades
    inspirado en el juego de la vida de Conway.
    """
    
    step = 5
    initial_density = 0.5
    
    room = np.zeros((consts.ROOM_HEIGHT, consts.ROOM_WIDTH), dtype=int)

    # entidades iniciales
    num_entities = int(initial_density * consts.ROOM_HEIGHT * consts.ROOM_WIDTH)
    indices = np.random.choice(consts.ROOM_HEIGHT * consts.ROOM_WIDTH, num_entities, replace=False)
    y, x = np.unravel_index(indices, (consts.ROOM_HEIGHT, consts.ROOM_WIDTH))
    room[y,x] = np.random.choice([ROCK, POOP, WEB, FIRE, UNIQUE_OBJECT, ENEMY_1, ENEMY_2, ENEMY_3, SPIKES], num_entities)

    """print("Habitacion inicial")
    print(room)
    print("Numero de enemigos: ", count_enemy(room))"""

    for _ in range(step):
        new_room = room.copy()
        for y in range(consts.ROOM_HEIGHT):
            for x in range(consts.ROOM_WIDTH):

                neighbors = count_neighbors(room, y, x)
                num_neighbors = count_neighbors_not_empty(room, y, x)

                entity = room[y,x]
                
                if (y in [0, consts.ROOM_HEIGHT - 1]) and (x in [0, consts.ROOM_WIDTH - 1]):
                    #esquina
                    new_room[y, x] = FIRE
                elif entity in [ENEMY_1, ENEMY_2, ENEMY_3]:
                    # Reglas del juego de la vida de Conway para reducir el número de enemigos
                    if num_neighbors < 2 or num_neighbors > 3:
                        new_room[y,x] = EMPTY
                    else:
                        new_room[y,x] = entity
                elif entity == EMPTY:
                    if neighbors[ROCK] > 0 and np.random.random() > 0.9:
                        new_room[y,x] = ROCK
                    elif neighbors[POOP] > 0 and np.random.random() > 0.95:
                        new_room[y,x] = POOP
                    elif neighbors[UNIQUE_OBJECT] == 0 and np.random.random() > 0.99:
                        new_room[y,x] =  UNIQUE_OBJECT
                elif entity == UNIQUE_OBJECT:
                    if neighbors[EMPTY] > 8:
                        new_room[y,x] = np.random.choice([EMPTY, UNIQUE_OBJECT])
                elif entity == POOP:
                    if neighbors[POOP] > 2:
                        new_room[y,x] = SPIKES
                elif neighbors[WEB] == 0:
                    new_room[y,x] = WEB
                else:
                    new_room[y,x] = entity

        room = new_room
    
    return room

def count_neighbors(room, i, j):
    """
    Cuenta el número de vecinos de cada tipo de entidad.
    """
    neighbors = {EMPTY: 0, ROCK: 0, POOP: 0, WEB: 0, FIRE: 0, UNIQUE_OBJECT: 0, ENEMY_1: 0, ENEMY_2: 0, ENEMY_3: 0, SPIKES: 0}

    for x in range(max(0, j - 1), min(consts.ROOM_WIDTH, j + 2)):
        for y in range(max(0, i - 1), min(consts.ROOM_HEIGHT, i + 2)):
            if x == j and y == i:
                continue
            neighbors[room[y, x]] += 1
    
    return neighbors


def count_neighbors_not_empty(room, i, j):
    neighbors = count_neighbors(room, i, j)
    return (neighbors[ROCK] + neighbors[POOP] + neighbors[WEB] + neighbors[FIRE]
             + neighbors[UNIQUE_OBJECT] + neighbors[ENEMY_1] + neighbors[ENEMY_2]
               + neighbors[ENEMY_3] + neighbors[SPIKES])


def count_enemy(room):
    count = 0
    for i in range(consts.ROOM_HEIGHT):
        for j in range(consts.ROOM_WIDTH):
            if room[i,j] == ENEMY_1 or room[i,j] == ENEMY_2 or room[i,j] == ENEMY_3:
                count += 1
    return count
