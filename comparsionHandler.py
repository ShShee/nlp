from ast import keyword
import networkx as nx

from conceptualGraph import ConceptualGraph
from enums import DataPathTypes, AdditionScores


class ComparisonHandler(ConceptualGraph):
    def __init__(self, graph_1, graph_2):
        """
        Input: graph_1 and graph_2 for initialization of same graph between them
        """
        self.graph = nx.Graph()

        same_nodes = graph_2.getSameNodes(graph_1)
        self.graph.add_nodes_from(same_nodes)

        # Size of nodes in graph
        self.nGcs = self.countNodes()
        self.nG1s = graph_1.countNodes()
        self.nG2s = graph_2.countNodes()

        # Size of same edges in comparison with this graph
        if len(same_nodes) != 0:
            self.mGcG1 = self.__getRelevantEdges(graph_1, same_nodes)
            self.mGcG2 = self.__getRelevantEdges(graph_2, same_nodes)

            self.graph.clear()
            self.graph.add_nodes_from(same_nodes)

            init_edges = self._create_edges(same_nodes)
            init_edges.append((same_nodes[0], same_nodes[len(same_nodes)-1]))
            self.graph.add_edges_from(graph_2.getSameEdges(init_edges))
            self.mGc = len(self.getEdges())
        else:
            self.mGc = 0
            self.mGcG1 = 0
            self.mGcG2 = 0

    def __getRelevantEdges(self, graph, same_nodes):
        """
        Input: graph that we need to find nodes of this graph in its edges
        Output: size of edges that satisfy the condition
        """
        self.graph.clear()
        self.graph.add_nodes_from(same_nodes)

        for node in list(self.getNodes()):
            self.graph.add_edges_from(graph.getParentsEdges(node))

        return len(self.getEdges())

    def __conceptual_similarity(self):
        return (2*self.nGcs)/(self.nG1s + self.nG2s)

    def __relational_similarity(self):
        denominator = self.mGcG1 + self.mGcG2
        return (2*self.mGc)/denominator if denominator != 0 else 0

    def __calculate_a(self):
        denominator = 2*self.nGcs + self.mGcG1 + self.mGcG2
        return (2*self.nGcs)/denominator if denominator != 0 else 0

    def getSimilarityScore(self, dataType):
        addition_type_score = AdditionScores.IS_ARTICLE.value if dataType == DataPathTypes.ARTICLES else 0
        similariy_score = self.__conceptual_similarity() * (self.__calculate_a() +
                                                            (1 - self.__calculate_a()) * self.__relational_similarity())

        total = round(similariy_score +
                      addition_type_score if similariy_score != 0 else 0, 5)
        return total if total < 1 else 1
