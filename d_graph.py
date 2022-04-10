# Course: CS261 - Data Structures
# Author: Joseph Coiffman
# Assignment: 6
# Description: Directed Graph

import heapq
from collections import deque

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        TODO: Write this implementation
        """
        for x in self.adj_matrix:
            x.append(0)
        self.adj_matrix.append([])
        for y in range(len(self.adj_matrix)):
            self.adj_matrix[len(self.adj_matrix) - 1].append(0)
        self.v_count = len(self.adj_matrix)
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        TODO: Write this implementation
        """
        if src == dst:
            return
        try:
            self.adj_matrix[src][dst] = weight
        except:
            return

    def remove_edge(self, src: int, dst: int) -> None:
        """
        TODO: Write this implementation
        """
        if src == dst or src < 0 or dst < 0:
            return
        try:
            self.adj_matrix[src][dst] = 0
        except:
            return

    def get_vertices(self) -> []:
        """
        TODO: Write this implementation
        """
        v_list = []
        for x in range(len(self.adj_matrix)):
            v_list.append(x)
        return v_list

    def get_edges(self) -> []:
        """
        TODO: Write this implementation
        """
        e_list = []
        for x in range(len(self.adj_matrix)):
            for y in range(len(self.adj_matrix[x])):
                if self.adj_matrix[x][y] > 0:
                   e_list.append((x, y, self.adj_matrix[x][y]))
        return e_list


    def is_valid_path(self, path: []) -> bool:
        """
        TODO: Write this implementation
        """
        for x in range(1, len(path)):
            if self.adj_matrix[path[x - 1]][path[x]] == 0:
                return False
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        TODO: Write this implementation
        """
        stack = deque()
        reachable = []
        stack.append(v_start)
        while stack:
            v = stack.pop()
            if v not in reachable:
                reachable.append(v)
                successors = []
                for x in range(len(self.adj_matrix[v])):
                    if self.adj_matrix[v][x] > 0:
                        successors.append(x)
                for y in range(len(successors) - 1, - 1, - 1):
                    stack.append(successors[y])
            if v == v_end:
                return reachable
        return reachable

    def bfs(self, v_start, v_end=None) -> []:
        """
        TODO: Write this implementation
        """
        que = deque()
        reachable = []
        que.append(v_start)
        while que:
            v = que.popleft()
            if v not in reachable:
                reachable.append(v)
                successors = []
                for x in range(len(self.adj_matrix[v])):
                    if self.adj_matrix[v][x] > 0:
                        successors.append(x)
                for y in successors:
                    que.append(y)
            if v == v_end:
                return reachable
        return reachable

    def has_cycle(self):
        """
        TODO: Write this implementation
        """
        new_list = self.get_vertices()
        for x in range(len(self.adj_matrix)):
            count_x = 0
            count_y = 0
            for y in range(len(self.adj_matrix[x])):
                if self.adj_matrix[x][y] > 0:
                    count_x += 1
                if self.adj_matrix[y][x] > 0:
                    count_y += 1
            if count_x == 0 or count_y == 0:
                new_list.remove(x)
        if len(new_list) > 2:
            dfs = self.dfs(new_list[0])
            need_3 = 0
            for x in new_list:
                if x in dfs:
                    need_3 += 1
            if need_3 > 2:
                return True

        return False

    def dijkstra(self, src: int) -> []:
        """
        TODO: Write this implementation
        """
        visited = {}
        dij = []
        priority = []
        heapq.heappush(priority, (0, src))
        while priority:
            save = heapq.heappop(priority)
            v = save[1]
            d = save[0]
            if v not in visited:
                visited[v] = d
                successors = []
                for x in range(len(self.adj_matrix[v])):
                    if self.adj_matrix[v][x] > 0:
                        successors.append(x)
                        this_d = self.adj_matrix[v][x]
                        heapq.heappush(priority, (this_d + d, x))

        for x in range(self.v_count):
            dij.append(float("inf"))
        for x in visited:
            dij[x] = visited[x]
        return dij


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
        g.remove_edge(6, -2)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')