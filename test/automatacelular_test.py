import sys
import os
import unittest
import numpy as np
from unittest.mock import patch

# Obtener la ruta del directorio raíz
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Agregar la ruta del directorio raíz al PATH de Python
sys.path.append(root_dir)

from src import consts
from src.modules.levels import automataCelular as ac

class TestCellularAutomata(unittest.TestCase):

    def setUp(self):
        # Configurar los valores constantes necesarios para las pruebas
        consts.ROOM_HEIGHT = 10
        consts.ROOM_WIDTH = 10
    
    def test_initial_room(self):
        room = ac.cellular_automatan()
        # Verificar que la habitación no está vacía
        self.assertNotEqual(np.count_nonzero(room), 0)
        # Verificar que las dimensiones de la habitación son correctas
        self.assertEqual(room.shape, (consts.ROOM_HEIGHT, consts.ROOM_WIDTH))

    def test_count_neighbors(self):
        room = np.zeros((consts.ROOM_HEIGHT, consts.ROOM_WIDTH), dtype=int)
        room[0, 0] = ac.ROCK
        room[0, 1] = ac.POOP
        room[1, 0] = ac.WEB
        
        neighbors = ac.count_neighbors(room, 1, 1)

        self.assertEqual(neighbors[ac.ROCK], 1)
        self.assertEqual(neighbors[ac.POOP], 1)
        self.assertEqual(neighbors[ac.WEB], 1)
        self.assertEqual(neighbors[ac.EMPTY], 5)

        neighbors = ac.count_neighbors(room, 0, 0)

        self.assertEqual(neighbors[ac.ROCK], 0)
        self.assertEqual(neighbors[ac.POOP], 1)
        self.assertEqual(neighbors[ac.WEB], 1)
        self.assertEqual(neighbors[ac.EMPTY], 1)

    def test_count_neighbors_not_empty(self):
        room = np.zeros((consts.ROOM_HEIGHT, consts.ROOM_WIDTH), dtype=int)
        room[0, 0] = ac.ROCK
        room[0, 1] = ac.POOP
        room[1, 0] = ac.WEB
        non_empty_neighbors = ac.count_neighbors_not_empty(room, 0, 0)
        self.assertEqual(non_empty_neighbors, 2)

    def test_count_enemy(self):
        room = np.zeros((consts.ROOM_HEIGHT, consts.ROOM_WIDTH), dtype=int)
        room[0, 0] = ac.ENEMY_1
        room[1, 1] = ac.ENEMY_2
        room[2, 2] = ac.ENEMY_3
        enemy_count = ac.count_enemy(room)
        self.assertEqual(enemy_count, 3)

    def test_evolution(self):
        initial_density = 0.5
        consts.ROOM_HEIGHT = 10
        consts.ROOM_WIDTH = 10
        num_entities = int(initial_density * consts.ROOM_HEIGHT * consts.ROOM_WIDTH)
        room = np.zeros((consts.ROOM_HEIGHT, consts.ROOM_WIDTH), dtype=int)
        indices = np.random.choice(consts.ROOM_HEIGHT * consts.ROOM_WIDTH, num_entities, replace=False)
        y, x = np.unravel_index(indices, (consts.ROOM_HEIGHT, consts.ROOM_WIDTH))
        room[y, x] = np.random.choice([ac.ROCK, ac.POOP, ac.WEB, ac.FIRE, ac.UNIQUE_OBJECT, ac.ENEMY_1, ac.ENEMY_2, ac.ENEMY_3, ac.SPIKES], num_entities)

        evolved_room = ac.cellular_automatan()

        # Verificar que el número de enemigos se reduce o permanece igual
        initial_enemy_count = ac.count_enemy(room)
        evolved_enemy_count = ac.count_enemy(evolved_room)
        self.assertLessEqual(evolved_enemy_count, initial_enemy_count)

        # Verificar que el tamaño de la habitación evolucionada es correcto
        self.assertEqual(evolved_room.shape, (consts.ROOM_HEIGHT, consts.ROOM_WIDTH))

if __name__ == '__main__':
    unittest.main()