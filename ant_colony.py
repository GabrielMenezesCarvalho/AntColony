# ant_colony.py
import random as rn
import numpy as np
from numpy.random import choice as np_choice

class AntColony(object):

    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha, beta):
        """
        Construtor da classe `AntColony`.

        Args:
            distances (2D numpy.array): Matriz quadrada de distâncias entre cidades. A diagonal é infinita (np.inf), indicando que uma cidade não pode se conectar a si mesma.
            n_ants (int): Número de formigas que serão simuladas por iteração.
            n_best (int): Número de melhores formigas cujos caminhos serão usados para depositar feromônio.
            n_iterations (int): Número de iterações do algoritmo.
            decay (float): Taxa de decaimento do feromônio. Multiplicado após cada iteração para diminuir o impacto de feromônios antigos.
            alpha (int ou float): Peso dado ao feromônio na fórmula de probabilidade. Valores altos dão mais importância ao feromônio.
            beta (int ou float): Peso dado à distância na fórmula de probabilidade. Valores altos dão mais importância à distância.

        Atributos:
            self.distances: Matriz de distâncias fornecida.
            self.pheromone: Matriz de feromônio inicializada com valores iguais.
            self.all_inds: Lista de índices de cidades.
            self.n_ants, self.n_best, self.n_iterations, self.decay, self.alpha, self.beta: Parâmetros definidos pelo usuário.
        """
        self.distances = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)  # Matriz de feromônio inicializada com valores iguais.
        self.all_inds = range(len(distances))  # Índices de todas as cidades.
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        """
        Executa o algoritmo da colônia de formigas.

        Retorna:
            all_time_shortest_path (tuple): O menor caminho e sua distância após todas as iterações.
        """
        shortest_path = None  # Variável para armazenar o menor caminho encontrado em uma iteração.
        all_time_shortest_path = ("placeholder", np.inf)  # Menor caminho encontrado em todas as iterações.

        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()  # Gera todos os caminhos criados pelas formigas nesta iteração.
            self.spread_pheronome(all_paths, self.n_best, shortest_path=shortest_path)  # Deposita feromônio com base nos melhores caminhos.
            shortest_path = min(all_paths, key=lambda x: x[1])  # Seleciona o menor caminho desta iteração.

            # Formata a saída da iteração
            print(f"Iteração {i + 1}: Menor caminho = {self.format_path(shortest_path[0])}, Distância = {shortest_path[1]:.2f}")
            
            if shortest_path[1] < all_time_shortest_path[1]:  # Atualiza o menor caminho de todas as iterações se necessário.
                all_time_shortest_path = shortest_path
            self.pheromone = self.pheromone * self.decay  # Aplica o decaimento no feromônio.

        print("\nMelhor caminho encontrado em todas as iterações:")
        print(f"Caminho = {self.format_path(all_time_shortest_path[0])}, Distância = {all_time_shortest_path[1]:.2f}")
        return all_time_shortest_path

    def format_path(self, path):
        """
        Formata um caminho em uma string legível, removendo repetições consecutivas.

        Args:
            path (list): Lista de tuplas representando o caminho percorrido.

        Retorna:
            str: Caminho formatado como string.
        """
        formatted_path = [path[0][0]]  # Adiciona a cidade inicial
        for step in path:
            if step[1] != formatted_path[-1]:  # Evita repetições consecutivas
                formatted_path.append(step[1])
        return " → ".join(map(str, formatted_path))

    def spread_pheronome(self, all_paths, n_best, shortest_path):
        """
        Deposita feromônio nos caminhos percorridos pelas melhores formigas.

        Args:
            all_paths (list): Lista de caminhos gerados por todas as formigas.
            n_best (int): Número de melhores caminhos para usar no depósito de feromônio.
            shortest_path (tuple): O menor caminho encontrado.
        """
        sorted_paths = sorted(all_paths, key=lambda x: x[1])  # Ordena os caminhos pela distância (custo).
        for path, dist in sorted_paths[:n_best]:  # Itera pelos n melhores caminhos.
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]  # Adiciona feromônio proporcional ao inverso da distância.

    def gen_path_dist(self, path):
        """
        Calcula a distância total de um caminho.

        Args:
            path (list): Caminho percorrido (lista de tuplas (cidade_origem, cidade_destino)).

        Retorna:
            total_dist (float): Distância total do caminho.
        """
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]  # Soma as distâncias de cada movimento no caminho.
        return total_dist

    def gen_all_paths(self):
        """
        Gera todos os caminhos percorridos pelas formigas nesta iteração.

        Retorna:
            all_paths (list): Lista de caminhos e suas respectivas distâncias.
        """
        all_paths = []
        for i in range(self.n_ants):  # Cada formiga gera um caminho.
            path = self.gen_path(0)  # Começa da cidade 0.
            all_paths.append((path, self.gen_path_dist(path)))  # Adiciona o caminho e sua distância à lista.
        return all_paths

    def gen_path(self, start):
        """
        Gera um caminho completo para uma formiga, começando em `start`.

        Args:
            start (int): Índice da cidade inicial.

        Retorna:
            path (list): Caminho percorrido (inclui retorno à cidade inicial).
        """
        path = []
        visited = set()  # Conjunto de cidades já visitadas.
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):  # Continua até visitar todas as cidades.
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)  # Escolhe a próxima cidade.
            path.append((prev, move))  # Adiciona o movimento ao caminho.
            prev = move  # Atualiza a cidade atual.
            visited.add(move)  # Marca a cidade como visitada.
        path.append((prev, start))  # Adiciona o retorno à cidade inicial.
        return path

    def pick_move(self, pheromone, dist, visited):
        """
        Escolhe a próxima cidade com base no feromônio e nas distâncias.

        Args:
            pheromone (numpy.array): Vetor de feromônios das arestas partindo da cidade atual.
            dist (numpy.array): Vetor de distâncias das arestas partindo da cidade atual.
            visited (set): Conjunto de cidades já visitadas.

        Retorna:
            move (int): Índice da próxima cidade.
        """
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0  # Zera o feromônio das cidades já visitadas.

        row = pheromone ** self.alpha * ((1.0 / dist) ** self.beta)  # Calcula o score de cada cidade.
        norm_row = row / row.sum()  # Normaliza os scores para formar uma distribuição de probabilidade.
        move = np_choice(self.all_inds, 1, p=norm_row)[0]  # Escolhe a próxima cidade com base na probabilidade.
        return move


