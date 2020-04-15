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
    map1 = folium.Map(location=location, zoom_start=13)
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
    new_filepath = filepath + 'population_map.html'
    map1.save(new_filepath)
    webbrowser.open('file://' + new_filepath)


def view_home_work_locations(filepath, home_location=None, work_location=None):
    if home_location is None and work_location is None:
        print('XXX home location or work location is not provided with data inputs XXX')
    elif filepath is None:
        print('XXX file path is not given with the inputs XXX')
    else:
        map1 = folium.Map(location=home_location,
                          zoom_start=11)
        if home_location is None:
            map1 = folium.Map(location=work_location,
                              zoom_start=11)
        if home_location is not None:
            folium.Marker(location=home_location,
                          popup='Home',
                          icon=folium.Icon(color='green', icon_color='white', icon='home', angle=0, prefix='fa'),
                          tooltip='Home Location'
                          ).add_to(map1)
        if work_location is not None:
            folium.Marker(location=work_location,
                          popup='Work Location',
                          icon=folium.Icon(color='darkblue', icon_color='white', icon='building', angle=0, prefix='fa'),
                          tooltip='Work Location'
                          ).add_to(map1)
        # visualize in web browser
        new_filepath = filepath + 'home&work_locations.html'
        map1.save(new_filepath)
        webbrowser.open('file://' + new_filepath)
