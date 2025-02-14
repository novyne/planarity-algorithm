class Node:

    NODE_CONNECTIONS = {}

    def __init__(self, name: int, *, connections: list['Node'] | None = None) -> None:
        """Node class.
        Args:
            name (int): The name of the node.
            connections (list['Node']): A list of nodes the Node joins to.
        """

        self.name = name
        Node.NODE_CONNECTIONS[name] = [] if connections is None else connections
    
    def connect(self, node: 'Node') -> None:
        """Add a node to the connection."""

        conns = self.connections()
        conns.append(node)
        Node.NODE_CONNECTIONS[self.name] = conns
    
    def connections(self) -> list['Node']:
        """Get the connections of the node."""

        return Node.NODE_CONNECTIONS[self.name]
        
    
    def __str__(self):
        if self.name + 96 <= ord('z'):
            return chr(self.name + 96)
        return str(self.name - 26)

    def __eq__(self, value):
        if isinstance(value, int):
            return self.name == value
        return self.name == value.name
    def __ne__(self, value):
        if isinstance(value, int):
            return self.name != value
        return self.name != value.name

    def __lt__(self, value):
        return self.name < value.name
    def __gt__(self, value):
        return self.name > value.name
    

class Arc:

    def __init__(self, start: Node, end: Node) -> None:
        """Arc class.
        Args:
            start (Node): The start node of the arc.
            end (Node): The end of the arc.
        """

        # start is always ordinally lower
        if start < end:
            self.start = start
            self.end = end
        else:
            self.start = end
            self.end = start
    
    def __str__(self):
        return f"{str(self.start)} -> {str(self.end)}"

    def __eq__(self, value: 'Arc'):
        return (self.start == value.start or self.start == value.end) and (self.end == value.start or self.end == value.end)
    
    def __lt__(self, value: 'Arc'):
        if self.start != value.start:
            return self.start < value.start
        return self.end < value.end
    
    def __gt__(self, value: 'Arc'):
        if self.start != value.start:
            return self.start > value.start
        return self.end > value.end