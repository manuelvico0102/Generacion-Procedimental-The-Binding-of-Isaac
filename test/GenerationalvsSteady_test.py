import sys
import os
import unittest
import time
import csv

# Obtener la ruta del directorio raíz
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Agregar la ruta del directorio raíz al PATH de Python
sys.path.append(root_dir)

import src.modules.levels.algoritmoGenetico as ag

class TestAlgoritmoGenetico(unittest.TestCase):
    def test_multiple_runs_generational(self):
        num_maps = 30
        map_width = 10
        map_height = 6
        room_numbers = [18, 23]  # un mapa intermedio

        population_sizes = [10, 20, 30]
        generations_list = [50, 100]

        with open('generational_results.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Algorithm', 'Population Size', 'Generations', 'Average Execution Time (s)', 'Average Fitness Score', 'Connectivity Percentage'])

            for population_size in population_sizes:
                for generations in generations_list:
                    total_execution_time = 0
                    total_fitness_score = 0
                    total_connected_maps = 0

                    for _ in range(num_maps):
                        start_time = time.time()
                        best_individual = ag.generational_genetic_algorithm(population_size, map_width, map_height, room_numbers, generations)
                        end_time = time.time()

                        execution_time = end_time - start_time
                        total_execution_time += execution_time

                        best_fitness = ag.fitness(best_individual, room_numbers)
                        total_fitness_score += best_fitness

                        # Comprobación de la conectividad del mapa resultante
                        if ag.all_rooms_have_path_to_start(best_individual):
                            total_connected_maps += 1

                    average_execution_time = total_execution_time / num_maps
                    average_fitness_score = total_fitness_score / num_maps
                    connectivity_percentage = (total_connected_maps / num_maps) * 100

                    writer.writerow(['Generational', population_size, generations, average_execution_time, average_fitness_score, connectivity_percentage])

    def test_multiple_runs_steady_state(self):
        num_maps = 30
        map_width = 10
        map_height = 6
        room_numbers = [18, 23]  # un mapa intermedio

        population_sizes = [10, 20, 30]
        generations_list = [50, 100]

        with open('steady_state_results.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Algorithm', 'Population Size', 'Generations', 'Average Execution Time (s)', 'Average Fitness Score', 'Connectivity Percentage'])

            for population_size in population_sizes:
                for generations in generations_list:
                    total_execution_time = 0
                    total_fitness_score = 0
                    total_connected_maps = 0

                    for _ in range(num_maps):
                        start_time = time.time()
                        best_individual = ag.steady_state_genetic_algorithm(population_size, map_width, map_height, room_numbers, generations)
                        end_time = time.time()

                        execution_time = end_time - start_time
                        total_execution_time += execution_time

                        best_fitness = ag.fitness(best_individual, room_numbers)
                        total_fitness_score += best_fitness

                        # Comprobación de la conectividad del mapa resultante
                        if ag.all_rooms_have_path_to_start(best_individual):
                            total_connected_maps += 1

                    average_execution_time = total_execution_time / num_maps
                    average_fitness_score = total_fitness_score / num_maps
                    connectivity_percentage = (total_connected_maps / num_maps) * 100

                    writer.writerow(['Steady State', population_size, generations, average_execution_time, average_fitness_score, connectivity_percentage])


if __name__ == '__main__':
    unittest.main()
