"""
Graphing classes and Mapping classes are modeled here

Graphing - matplotlib, networkx
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import folium
from folium.plugins import MarkerCluster
import webbrowser


def network_graph(edge_list, directed):
    if directed:
        g = nx.DiGraph()
    else:
        g = nx.Graph()

    # print(weighted_edges)
    for edge in edge_list:
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


def cell_population_visualization(cell_list, filepath):
    location = [cell_list[0]['latitude'], cell_list[0]['longitude']]
    map1 = folium.Map(location=location, tiles='CartoDB dark_matter', zoom_start=13)
    marker_cluster = folium.plugins.MarkerCluster().add_to(map1)
    location_list = []
    for cell in cell_list:
        cell_location = [cell['latitude'], cell['longitude']]
        for i in range(int(cell['population_around_cell'])):
            location_list.append(cell_location)
    for point in location_list:
        folium.Marker(location=point,
                      popup='nothing').add_to(marker_cluster)
    # visualize in web browser
    new_filepath = filepath+'map.html'
    map1.save(new_filepath)
    webbrowser.open('file://' + new_filepath)

