import random as rn

from node import Node, Arc


class NetworkGraph:

    def __init__(self, arcs: list[Arc] | None = None) -> None:
        """Network graph class.
        Args:
            arcs (list[Arc], optional): A list of the arcs making up the graph.
        """
        
        if arcs is None:
            self.arcs = []
        else:
            self.arcs = arcs
            # remove duplicates
            for a in arcs:
                while self.arcs.count(a) > 1:
                    self.arcs.remove(a)
            self.arcs.sort()
        
        self.nodes = self.get_nodes()
    
    def __str__(self):
        s = ''

        for n in self.nodes:
            s += f'{str(n)} -> {', '.join(str(c) for c in n.connections())}\n'
        
        return s

    def random(self, *, n: int | None = None, min_degree: int=1, max_degree: int | float = float('inf')) -> 'NetworkGraph':
        """Generate a random NetworkGraph.
        Args:
            n (int, optional): The number of nodes. if not given, generate between 10-100 nodes inclusive.
            min_degree (int, default=1): The minimum degree of each node.
            max_degree (int, default=inf): The maximum degree of each node.
        Returns:
            NetworkGraph: The randomly-generated NetworkGraph.
        """
        
        # init
        n = (rn.randint(10, 100) if n is None else n)
        arcs = []
        complete_nodes = []

        # loop until every node is joined
        while len(complete_nodes) < n * min_degree:
            # establish start and end
            start = rn.randint(1, n)
            end = rn.randint(1, n)
            if start == end:
                continue

            # create the arc
            arc = Arc(Node(start), Node(end))
            if arc in arcs:
                continue
            if complete_nodes.count(start) == max_degree or complete_nodes.count(end) == min_degree:
                continue
            arcs.append(arc)

            # add the node to the joined nodes if not present
            for node in [start, end]:
                if complete_nodes.count(node) < min_degree:
                    complete_nodes.append(node)
        
        return NetworkGraph(arcs)

    def num_nodes(self) -> int:
        """Minifunc to get the number of nodes in the network graph.
        Returns:
            int: The number of nodes in the network graph."""
    
        nodes = []
        for a in self.arcs:
            for node in [a.start, a.end]:
                if node not in nodes:
                    nodes.append(node)
        return len(nodes)

    def get_nodes(self) -> list[Node]:
        """Get the node connections.
        Returns:
            list[Node]: The list of node connections retrieved."""
        
        nodes: list[Node] = [Node(name=(i)) for i in range(1, self.num_nodes() + 1)]
        for a in self.arcs:
            nodes[a.start.name - 1].connect(a.end)
            nodes[a.end.name - 1].connect(a.start)
        return nodes
    
    def recur_hamiltonian(self, path: list[Node], node: Node) -> list[list[Node]] | None:
        """Minifunc to find Hamiltonian cycles within the network graph.
        Args:
            path: (list[Node], optional): The path to track recursion progress. Passing this argument *may impact its ability to function correctly*.
            node (Node, optional): The current node in the path. Passing this argument *may impact its ability to function correctly*.
        Returns:
            list[list[Node]] | None: The sequences of nodes if found, otherwise None.
        """

        if node == path[0] and len(path) == len(self.nodes):
            return path + [path[0]]
    
        for c in node.connections():
            if c.name in [n.name for n in path]:
                continue
            path = self.recur_hamiltonian(path + [c], c)
        
        return path
    
    def hamiltonian(self) -> list[Node]:
        """Function to find a Hamiltonian path in the graph.
        Returns:
            list[Node]: The sequence of nodes found.
        """

        n = rn.choice(self.nodes)
        return self.recur_hamiltonian([n], n) + [n]


def main() -> None:
    """The main program."""

    graph = NetworkGraph().random(n=100, min_degree=2, max_degree=10)
    print(graph)
    hamils = graph.hamiltonian()
    print([str(n) for n in hamils])

if __name__ == '__main__':
    main()