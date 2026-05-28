import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._drivers = []
        self._idMapD = {}

    def getAllYears(self):
        return DAO.getAllYears()

    def buildGraph(self, year1,year2):
        self._graph.clear()
        self._drivers = DAO.getAllNodes(year1,year2)
        for d in self._drivers:
            self._idMapD[d.driverId] = d
        self._graph.add_nodes_from(self._drivers)

        edges = DAO.getAllEdges(year1,year2, self._idMapD)
        for e in edges:
            self._graph.add_edge(e.d1,e.d2,weight=e.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getTop3Archi(self):
        return sorted(self._graph.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)[:3]

    def getConnessaInfo(self):
        components = list(nx.connected_components(self._graph))
        largest = max(components, key=len)

        subgraph = self._graph.subgraph(largest).copy()
        orderedNodes = sorted(subgraph.nodes(),key=lambda n:self._graph.degree(n),reverse=True)

        details = [(n,self._graph.degree(n)) for n in orderedNodes]
        return len(components), largest, details