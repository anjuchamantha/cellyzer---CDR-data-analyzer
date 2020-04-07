"""
Graphing classes and Mapping classes are modeled here

Graphing - matplotlib, networkx
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def get_weighted_edge_list(edge_list, directed):
    weighted_edge_list = []

    if not directed:
        for edge in edge_list:
            count = edge_list.count(edge)
            reversed_edge = edge.copy()
            reversed_edge.reverse()
            r_count = edge_list.count(reversed_edge)
            weight = count + r_count
            weighted_edge = edge.copy()
            weighted_edge.append(weight)

            not_added = True
            for i in weighted_edge_list:
                if (edge == [i[0], i[1]]) or (reversed_edge == [i[0], i[1]]):
                    not_added = False
                    break
            if not_added:
                weighted_edge_list.append(weighted_edge)

        return weighted_edge_list
    if directed:
        for edge in edge_list:
            weight = edge_list.count(edge)
            weighted_edge = edge.copy()
            weighted_edge.append(weight)

            not_added = True
            for i in weighted_edge_list:
                if edge == [i[0], i[1]]:
                    not_added = False
                    break
            if not_added:
                weighted_edge_list.append(weighted_edge)

        return weighted_edge_list


def network_graph(edge_list, directed):
    if directed:
        g = nx.DiGraph()
    else:
        g = nx.Graph()

    weighted_edges = get_weighted_edge_list(edge_list, directed)
    # print(weighted_edges)
    for edge in weighted_edges:
        g.add_edge(edge[0], edge[1], weight=edge[2])

    pos = nx.circular_layout(g)
    labels = nx.get_edge_attributes(g, 'weight')
    nx.draw_networkx(g, pos, font_size=7, node_size=800, node_color="lightcoral", node_shape="o",
                     edge_color="dodgerblue",
                     style="solid", width=2)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=labels, with_labels=True, font_size=8, label_pos=0.3)
    plt.savefig("connection_network.png")
    plt.show()


def active_time_bar_chart(time_dict):
    hours = []
    activity = []
    for key, value in time_dict.items():
        hours.append(key)
        activity.append(value)

    y_pos = np.arange(len(hours))
    plt.bar(y_pos, activity, align='center', alpha=0.9)
    plt.xticks(y_pos, hours)
    plt.ylabel("Activity")
    plt.xlabel("Hours")
    plt.title("Most active times during day")
    plt.show()
