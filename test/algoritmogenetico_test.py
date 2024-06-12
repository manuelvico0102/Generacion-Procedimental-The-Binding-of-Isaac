import sys
import os
import unittest
from unittest.mock import patch

# Obtener la ruta del directorio raíz
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Agregar la ruta del directorio raíz al PATH de Python
sys.path.append(root_dir)

from src import consts
import src.modules.levels.algoritmoGenetico as ag

class TestAlgoritmoGenetico(unittest.TestCase):

    def test_generate_initial_population(self):
        population_size = 10
        map_width = 5
        map_height = 5
        room_numbers = 7
        population = ag.generate_initial_population(population_size, map_width, map_height, room_numbers)
        
        self.assertEqual(len(population), population_size, "La población generada no tiene el tamaño esperado.")
        for i, individual in enumerate(population):
            self.assertEqual(len(individual), map_height, f"El individuo {i} no tiene la altura esperada.")
            self.assertEqual(len(individual[0]), map_width, f"El individuo {i} no tiene el ancho esperado.")

    def test_fitness_function(self):
        rooms = [[consts.RoomsTypes.DEFAULT for _ in range(5)] for _ in range(5)]
        rooms[0][0] = consts.RoomsTypes.SPAWN
        rooms[4][4] = consts.RoomsTypes.BOSS
        nRooms = (5, 10)
        
        score = ag.fitness(rooms, nRooms)
        self.assertGreater(score, 0, "La función de aptitud no ha devuelto un puntaje mayor que 0.")

    def test_crossover(self):
        parent1 = [[consts.RoomsTypes.DEFAULT for _ in range(5)] for _ in range(5)]
        parent2 = [[consts.RoomsTypes.BOSS for _ in range(5)] for _ in range(5)]
        
        child = ag.crossover(parent1, parent2)
        
        self.assertEqual(len(child), 5, "El hijo generado no tiene la altura esperada.")
        self.assertEqual(len(child[0]), 5, "El hijo generado no tiene el ancho esperado.")
        self.assertTrue(any(cell == consts.RoomsTypes.DEFAULT for row in child for cell in row), "El hijo no contiene habitaciones de tipo DEFAULT.")

    def test_mutate(self):
        rooms = [[consts.RoomsTypes.DEFAULT for _ in range(5)] for _ in range(5)]
        rooms[0][0] = consts.RoomsTypes.SPAWN
        mutation_prob = 0.5
        mutation_rate = 0.2
        
        mutated_rooms = ag.mutate(rooms, mutation_prob, mutation_rate)
        
        self.assertEqual(len(mutated_rooms), 5, "Las habitaciones mutadas no tienen la altura esperada.")
        self.assertEqual(len(mutated_rooms[0]), 5, "Las habitaciones mutadas no tienen el ancho esperado.")
        self.assertEqual(mutated_rooms[0][0], consts.RoomsTypes.SPAWN, "La habitación de inicio no debería mutarse.")

    @patch('random.choices')
    def test_select_parents_baker(self, mock_choices):
        population = [[consts.RoomsTypes.DEFAULT for _ in range(5)] for _ in range(5)]
        fitness_scores = [(individual, 10) for individual in population]
        mock_choices.return_value = [population[0], population[1]]
        
        parent1, parent2 = ag.select_parents_baker(population, fitness_scores)
        
        self.assertEqual(parent1, population[0], "El primer padre seleccionado no es el esperado.")
        self.assertEqual(parent2, population[1], "El segundo padre seleccionado no es el esperado.")
        
if __name__ == '__main__':
    unittest.main()
    
