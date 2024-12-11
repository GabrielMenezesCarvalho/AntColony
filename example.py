import numpy as np
from ant_colony import AntColony

# Define a matriz de distâncias entre as cidades. Diagonal = np.inf, pois uma cidade não pode se conectar a si mesma.
distances = np.array([[np.inf, 2, 2, 5, 7],
                      [2, np.inf, 4, 8, 2],
                      [2, 4, np.inf, 1, 3],
                      [5, 8, 1, np.inf, 2],
                      [7, 2, 3, 2, np.inf]])

# Cria uma instância da classe AntColony com os parâmetros definidos.
# def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
ant_colony = AntColony(distances, 1, 1, 100, 0.95, alpha=1, beta=1)

# Executa o algoritmo e obtém o menor caminho.
shortest_path = ant_colony.run()


