import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self._rifugi = None
        self._connessioni_rifugi = None
        self._num_nodi = None

    def build_graph(self, year: int):
        """
        Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni
        con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        self.G.clear()
        self._rifugi = DAO.get_rifugi(year)
        self._connessioni_rifugi = DAO.get_connessione_rifugi(year)
        for c in self._connessioni_rifugi:
            self.G.add_edge(c.id_rifugio1, c.id_rifugio2)

    def id_nome(self, id):
        nome = None
        for rifugio in self._rifugi:
            if rifugio.id == id:
                nome = rifugio.nome
                break
        return nome

    def id_localita(self, id):
        localita = None
        for rifugio in self._rifugi:
            if rifugio.id == id:
                localita = rifugio.localita
                break
        return localita

    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """
        return self.G

    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """
        num_neighbors = self.G.degree[node]
        return num_neighbors

    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """
        self._num_nodi = 0
        for n in self.G:
            num_vicini_n = self.G.degree[n]
            if num_vicini_n > self._num_nodi:
                self._num_nodi = num_vicini_n
        return self._num_nodi

    def get_reachable(self, start):
        """
        Deve eseguire almeno 2 delle 3 tecniche indicate nella traccia:
        * Metodi NetworkX: `dfs_tree()`, `bfs_tree()`
        * Algoritmo ricorsivo DFS
        * Algoritmo iterativo
        per ottenere l'elenco di rifugi raggiungibili da `start` e deve restituire uno degli elenchi calcolati.
        :param start: nodo di partenza, da non considerare nell'elenco da restituire.

        ESEMPIO
        a = self.get_reachable_bfs_tree(start)
        b = self.get_reachable_iterative(start)
        b = self.get_reachable_recursive(start)

        return a

        ---
        1) metodo con DFS ricorsiva:

        visited = set()
        def dfs(node):
            for neighbor in self.G.neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    dfs(neighbor)

        dfs(start)
        visited.discard(start)  # rimuovo il nodo di partenza
        return list(visited)
        """

        #2) Restituisce la lista di nodi raggiungibili da `start` usando bfs_tree.
        bfs = nx.bfs_tree(self.G, start)
        reachable = list(bfs.nodes)
        reachable.remove(start)
        return reachable