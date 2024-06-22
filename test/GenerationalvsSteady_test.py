import sys
import os
import unittest
import time
import csv
import statistics

# Obtener la ruta del directorio raíz
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Agregar la ruta del directorio raíz al PATH de Python
sys.path.append(root_dir)

import src.modules.levels.algoritmoGenetico as ag

class TestAlgoritmoGenetico(unittest.TestCase):
    """def test_multiple_runs_generational(self):
        num_maps = 30
        map_width = 10
        map_height = 6
        room_numbers = [18, 23]  # un mapa intermedio

        population_sizes = [10, 20, 30]
        generations_list = [50, 100]

        with open('generational_results.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Algorithm', 'Population Size', 'Generations', 'Average Execution Time (s)', 'Execution Time Std Dev (s)', 'Average Fitness Score', 'Fitness Score Std Dev', 'Connectivity Percentage', 'Connectivity Std Dev'])

            for population_size in population_sizes:
                for generations in generations_list:
                    execution_times = []
                    fitness_scores = []
                    connected_maps = []

                    for _ in range(num_maps):
                        start_time = time.time()
                        best_individual = ag.generational_genetic_algorithm(population_size, map_width, map_height, room_numbers, generations)
                        end_time = time.time()

                        execution_time = end_time - start_time
                        execution_times.append(execution_time)

                        best_fitness = ag.fitness(best_individual, room_numbers)
                        fitness_scores.append(best_fitness)

                        # Comprobación de la conectividad del mapa resultante
                        is_connected = ag.all_rooms_have_path_to_start(best_individual)
                        connected_maps.append(1 if is_connected else 0)

                    average_execution_time = sum(execution_times) / num_maps
                    execution_time_std_dev = statistics.stdev(execution_times)

                    average_fitness_score = sum(fitness_scores) / num_maps
                    fitness_score_std_dev = statistics.stdev(fitness_scores)

                    connectivity_percentage = (sum(connected_maps) / num_maps) * 100
                    connectivity_std_dev = statistics.stdev(connected_maps) * 100  # Escalar a porcentaje

                    writer.writerow(['Generational', population_size, generations, average_execution_time, execution_time_std_dev, average_fitness_score, fitness_score_std_dev, connectivity_percentage, connectivity_std_dev])
"""
    def test_multiple_runs_steady_state(self):
        num_maps = 30
        map_width = 10
        map_height = 6
        room_numbers = [18, 23]  # un mapa intermedio

        population_sizes = [10, 20, 30]
        generations_list = [50, 100]

        with open('steady_state_results.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Algorithm', 'Population Size', 'Generations', 'Average Execution Time (s)', 'Execution Time Std Dev (s)', 'Average Fitness Score', 'Fitness Score Std Dev', 'Connectivity Percentage', 'Connectivity Std Dev'])

            for population_size in population_sizes:
                for generations in generations_list:
                    execution_times = []
                    fitness_scores = []
                    connected_maps = []

                    for _ in range(num_maps):
                        start_time = time.time()
                        best_individual = ag.steady_state_genetic_algorithm(population_size, map_width, map_height, room_numbers, generations)
                        end_time = time.time()

                        execution_time = end_time - start_time
                        execution_times.append(execution_time)

                        best_fitness = ag.fitness(best_individual, room_numbers)
                        fitness_scores.append(best_fitness)

                        # Comprobación de la conectividad del mapa resultante
                        is_connected = ag.all_rooms_have_path_to_start(best_individual)
                        connected_maps.append(1 if is_connected else 0)

                    average_execution_time = sum(execution_times) / num_maps
                    execution_time_std_dev = statistics.stdev(execution_times)

                    average_fitness_score = sum(fitness_scores) / num_maps
                    fitness_score_std_dev = statistics.stdev(fitness_scores)

                    connectivity_percentage = (sum(connected_maps) / num_maps) * 100
                    connectivity_std_dev = statistics.stdev(connected_maps) * 100  # Escalar a porcentaje

                    writer.writerow(['Steady State', population_size, generations, average_execution_time, execution_time_std_dev, average_fitness_score, fitness_score_std_dev, connectivity_percentage, connectivity_std_dev])

if __name__ == '__main__':
    unittest.main()
