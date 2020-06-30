"""
Graphing classes and Mapping classes are modeled here
"""
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import folium
from folium.plugins import MarkerCluster
import webbrowser
import os
import base64
from io import BytesIO

matplotlib.use("agg")

plt.rcParams['figure.dpi'] = 200

try:
    os.mkdir('outputs')
except OSError as error:
    print(error)


def network_graph(edge_list, directed, gui, fig_id, font_size=6, users="All"):
    """
    Visualize the connections of the given list of users in a graph
    Nodes are users and Edges are the connections
    The arrow head from A to B represent a call from user A to B
    The edge value near the arrow head represents the number of calls made from A to B
    :param edge_list: list of 2 user couples with 1st user made a call to the 2nd
    :param directed: Bool value to switch between directed and undirected graphs
    :param fig_id: unique ID to the figure
    :param users: list of users
    :return: None, visualizes the graph in a web page
    """
    plt.figure(fig_id)
    if directed:
        g = nx.DiGraph()
    else:
        g = nx.Graph()
    for edge in edge_list:
        g.add_edge(edge[0], edge[1], weight=edge[2])

    pos = nx.circular_layout(g)
    labels = nx.get_edge_attributes(g, 'weight')
    nx.draw_networkx(g, pos, font_size=font_size, node_size=800, node_color="lightcoral", node_shape="o",
                     edge_color="dodgerblue", style="solid", width=2, )
    nx.draw_networkx_edge_labels(g, pos, edge_labels=labels, with_labels=True, font_size=font_size, label_pos=0.3)

    tmpfile = BytesIO()
    plt.title('Connections of : {}'.format(users), fontsize=8)
    plt.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    html = '<div>' + '<img src=\'data:image/png;base64,{}\'>'.format(encoded) + '</div>'
    with open('outputs\\connection_network.html', 'w') as f:
        f.write(html)
    webbrowser.open("outputs\\connection_network.html")


def active_time_bar_chart(time_dict, gui=False, user='xxx', dataset_id='1'):
    """
    Generates a bar chart of the active time of a given user.
    X-axis represents the time(hour of the day)
    Y-axis number of records
    :param time_dict: Dictionary of hour and activities as key,value pairs
    :param user: Given User
    :return: None, visualizes the chart in a web page
    """
    fig_id = user + dataset_id
    plt.figure(fig_id)
    hours = []
    activity = []
    for key, value in time_dict.items():
        hours.append(key)
        activity.append(value)

    y_pos = np.arange(len(hours))
    plt.bar(y_pos, activity, align='center', alpha=0.9)
    plt.xticks(y_pos, hours, fontsize=6)
    plt.ylabel("Activity", fontsize=8)
    plt.xlabel("Hours", fontsize=8)
    plt.title("Most active times during day - user: " + user, fontsize=8)

    tmpfile = BytesIO()
    plt.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    html = '<div>' + '<img src=\'data:image/png;base64,{}\'>'.format(encoded) + '</div>'
    with open('outputs\\active_time_bar_chart.html', 'w') as f:
        f.write(html)
    webbrowser.open("outputs\\active_time_bar_chart.html")


def cell_population_visualization(cell_list, map_name="population_map", notebook=False):
    """
    Visualize a map with population around cells

    :param cell_list: cells and its respective number of calls
    :param map_name: name of the map to be displayed
    :param notebook: set to True of runs in a notebook
    :return: shows a map with population around cells
    """
    location = [cell_list[0]['latitude'], cell_list[0]['longitude']]
    map1 = folium.Map(location=location, zoom_start=12)
    marker_cluster = folium.plugins.MarkerCluster().add_to(map1)
    location_list = []
    for cell in cell_list:
        cell_location = [cell['latitude'], cell['longitude']]
        for i in range(int(cell['population_around_cell'])):
            location_list.append(cell_location)
    for point in location_list:
        folium.Marker(location=point,
                      popup='nothing').add_to(marker_cluster)
    if notebook:
        return map1
    else:
        # visualize in web browser
        file_path = 'outputs\\' + map_name + '.html'
        map1.save(file_path)
        webbrowser.open(file_path)


def view_home_work_locations(home_location=None, work_location=None, map_name="home_work_location", notebook=False):
    """
    Visualize a map of home and work locations
    :param home_location: home locations
    :param work_location: work locations
    :param map_name: name of the map to be displayed
    :param notebook: set True if run in notebook
    :return: shows a map with home/work locations around cells
    """

    if home_location is None and work_location is None:
        print('XXX home location or work location is not provided with data inputs XXX')
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
        if notebook:
            return map1
        else:
            # visualize in web browser
            file_path = 'outputs\\' + map_name + '.html'
            map1.save(file_path)
            webbrowser.open(file_path)


def create_marked_map(location_list, location="location", value="timestamp"):
    if not location_list:
        return None
    initial_location = location_list[0][location]
    marked_map = folium.Map(location=initial_location, tiles="OpenStreetMap", zoom_start=13)
    marker_cluster = folium.plugins.MarkerCluster().add_to(marked_map)

    for item in location_list:
        loc = item[location]
        val = item[value].strftime('%d.%m.%Y %H:%M:%S')
        folium.Marker(location=loc, popup=val).add_to(marker_cluster)
    return marked_map


def trip_visualization(locations, map_name="trip_map", notebook=False):
    """
    Visualize the trips/routes of a given user in a map
    :param locations: Locations visited by the user (sorted in timestamp)
    :param map_name: name of the map to be displayed
    :param notebook: set true if runs in notebook
    :return: shows a map of routes of the user
    """
    if not locations:
        print("No trips to visualize")
        return None
    marked_map = create_marked_map(locations, value="timestamp")
    location_list = []
    for item in locations:
        location_list.append(item["location"])

    folium.PolyLine(location_list, color='red', weight=12, opacity=0.5).add_to(marked_map)
    if notebook:
        return marked_map
    else:
        marked_map.save('outputs\\' + map_name + '.html')
        webbrowser.open('outputs\\' + map_name + '.html')
