"""
Graphing classes and Mapping classes are modeled here

Graphing - matplotlib
Mapping - ipyleaflet / folium
"""

import networkx as nx
import matplotlib.pyplot as plt


def network_graph(edge_list):
    g = nx.Graph()
    for edge in edge_list:
        g.add_edge(edge[0], edge[1])
    nx.draw_shell(g, with_labels=True)
    plt.savefig("connection_network.png")
    plt.show()

# g.add_edge(1, 2)
# g.add_edge(2, 3)
# g.add_edge(3, 4)
# g.add_edge(1, 4)
# g.add_edge(1, 5)
#
# nx.draw(g, with_labels=True)
# plt.savefig("filename.png")
