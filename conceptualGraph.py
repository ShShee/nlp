import networkx as nx


class ConceptualGraph:
    def __init__(self, keywords):
        """
        Input: List of keywords to init graph
        """
        self.graph = nx.Graph()
        self.graph.add_nodes_from(keywords)
        self.graph.add_edges_from(self._create_edges(keywords))

    def _create_edges(self, keywords):
        """
        Input: List of keywords to init edges
        Output: Edges that is connected between 2 adjoined keywords
        """
        edges = []

        for idx in range(len(keywords)-1):
            edges.append((keywords[idx], keywords[idx+1]))

        return edges

    def getGraph(self):
        return self.graph

    def getNodes(self):
        """
        Output: Nodes of this graph
        """
        return self.graph.nodes

    def countNodes(self):
        """
        Output: Number of nodes in this graph (every nodes has different score)
        """
        count = 0
        for node in self.graph.nodes:
            count = count + 1 + node[2]
        return count

    def getEdges(self):
        """
        Output: Edges of this graphs
        """
        return self.graph.edges

    def print(self):
        print("Nodes:", self.graph.nodes)
        print("Edges:", self.graph.edges)

    def getSameNodes(self, graph):
        """
        Input: Graph that needs to be found same nodes with this graph
        Output: List of nodes that appear in both graphs
        """
        result = []
        for item in self.getNodes():
            for node in graph.getNodes():
                if item[0] == node[0]:
                    result.append(node)
                    break
        return result

    def getSameEdges(self, edges):
        """
        Input: Edges that needs to be checked is belong to this graph
        Output: Edges that appear in this graph
        """
        result = []
        for edge in self.getEdges():
            for item in edges:
                if (item[0] == edge[0] and item[1] == edge[1]) or (item[0] == edge[1] and item[1] == edge[0]):
                    result.append(edge)

        return result

    def getParentsEdges(self, node):
        """
        Input: Node that needs to be found its edges
        Output: Edges that have input node in it
        """
        result = []
        for edge in self.getEdges():
            if edge[0] == node or edge[1] == node:
                result.append(edge)

        return result
