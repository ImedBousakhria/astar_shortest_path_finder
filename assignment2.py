# import tkinter as tk
# from tkinter import messagebox
# import osmnx as ox
# import networkx as nx
# import xml.etree.ElementTree as ET
# import matplotlib.pyplot as plt

# def preprocess_osm_data(osm_file):
#     with open(osm_file, "r", encoding="utf-8") as file:
#         osm_data = file.read()

#     root = ET.fromstring(osm_data)
#     node_names = {}
#     for node in root.findall(".//node"):
#         node_id = int(node.attrib['id'])
#         name_tag = node.find("./tag[@k='name']")
#         if name_tag is not None:
#             name_value = name_tag.attrib['v']
#             node_names[name_value] = node_id
#     return node_names

# def build_graph_from_osm(osm_file):
#     G = ox.graph_from_xml(osm_file)
#     return G

# def a_star_search(graph, source_node, destination_node):
#     try:
#         path = nx.astar_path(graph, source_node, destination_node)
#         return path
#     except nx.NetworkXNoPath:
#         return None

# def find_shortest_path():
#     source_city = source_city_entry.get()
#     destination_city = destination_city_entry.get()

#     source_node_id = node_names.get(source_city)
#     destination_node_id = node_names.get(destination_city)

#     print("Source Node ID:", source_node_id)
#     print("Destination Node ID:", destination_node_id)

#     if not source_node_id or not destination_node_id:
#         messagebox.showerror("Error", "Source or destination city not found in OSM data.")
#         return

#     if source_node_id not in graph.nodes or destination_node_id not in graph.nodes:
#         messagebox.showerror("Error", "Source or destination node ID not present in the graph.")
#         return

#     path = a_star_search(graph, source_node_id, destination_node_id)
#     if path:
#         shortest_path_label.config(text=f"Shortest path: {path}")
#         plot_map_with_path(graph, path)
#     else:
#         shortest_path_label.config(text="No path found.")

# def plot_map_with_path(graph, path):
#     fig, ax = ox.plot_graph_route(graph, path, node_size=0, figsize=(15, 15), show=False, close=False)
#     plt.tight_layout()
#     plt.axis('off')
#     plt.show()

# # GUI
# root = tk.Tk()
# root.title("A* Search GUI")

# osm_file = "./map_amizour.osm"
# node_names = preprocess_osm_data(osm_file)
# graph = build_graph_from_osm(osm_file)

# print("Node IDs from OSM data:", node_names)
# # print("Node IDs in the graph:", graph.nodes())

# source_label = tk.Label(root, text="Source City:")
# source_label.grid(row=0, column=0, padx=10, pady=5)
# source_city_entry = tk.Entry(root)
# source_city_entry.grid(row=0, column=1, padx=10, pady=5)

# destination_label = tk.Label(root, text="Destination City:")
# destination_label.grid(row=1, column=0, padx=10, pady=5)
# destination_city_entry = tk.Entry(root)
# destination_city_entry.grid(row=1, column=1, padx=10, pady=5)

# find_path_button = tk.Button(root, text="Find Shortest Path", command=find_shortest_path)
# find_path_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

# shortest_path_label = tk.Label(root, text="")
# shortest_path_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# root.mainloop()
import tkinter as tk
from tkinter import messagebox
import osmnx as ox
import networkx as nx
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

def plot_shortest_path(graph, path):
    gdf_nodes, gdf_edges = ox.graph_to_gdfs(graph)

    fig, ax = plt.subplots()
    gdf_nodes.plot(ax=ax, color='gray')

    gdf_edges.plot(ax=ax, color='gray')

    shortest_path_edges = gdf_edges.loc[path]
    shortest_path_edges.plot(ax=ax, color='red')

    plt.show()
    
    
def preprocess_osm_data(osm_file):
    with open(osm_file, "r", encoding="utf-8") as file:
        osm_data = file.read()

    root = ET.fromstring(osm_data)
    nodes_info = {}
    for node in root.findall(".//node"):
        node_id = node.attrib['id']
        lat = node.attrib['lat']
        lon = node.attrib['lon']
        name_tag = node.find("./tag[@k='name']")
        if name_tag is not None:
            name_value = name_tag.attrib['v']
            nodes_info[name_value] = {'id': node_id, 'lat': float(lat), 'lon': float(lon)}
    return nodes_info

def build_graph_from_osm(osm_file):
    G = ox.graph_from_xml(osm_file)
    return G

def find_matching_node(graph, node_info):
    for node, data in graph.nodes(data=True):
        if 'name' in data and data['name'] == node_info['name']:
            node_lat = data['y']
            node_lon = data['x']
            if abs(node_lat - node_info['lat']) < 0.0001 and abs(node_lon - node_info['lon']) < 0.0001:
                return node
    return None

def a_star_search(graph, source_node, destination_node):
    try:
        path = nx.astar_path(graph, source_node, destination_node)
        return path
    except nx.NetworkXNoPath:
        return None

def find_shortest_path():
    source_city = source_city_entry.get()
    destination_city = destination_city_entry.get()

    source_node_info = node_names.get(source_city)
    destination_node_info = node_names.get(destination_city)

    if not source_node_info or not destination_node_info:
        # messagebox.showerror("Error", "Source or destination city not found in OSM data.")
        # return
        pass 
    source_node = find_matching_node(graph, source_node_info)
    destination_node = find_matching_node(graph, destination_node_info)

    # if source_node is None or destination_node is None:
    #     messagebox.showerror("Error", "Matching nodes not found in the graph.")
    #     return

    
    path = a_star_search(graph, 5358969815, 2657673363)
    if path:
        plot_shortest_path(graph, path)
        shortest_path_label.config(text=f"Shortest path: {path}")
    else:
        shortest_path_label.config(text="No path found.")
# GUI
root = tk.Tk()
root.title("A* Search GUI")

osm_file = "./map_amizour.osm"
node_names = preprocess_osm_data(osm_file)
graph = build_graph_from_osm(osm_file)


source_label = tk.Label(root, text="Source City:")
source_label.grid(row=0, column=0, padx=10, pady=5)
source_city_entry = tk.Entry(root)
source_city_entry.grid(row=0, column=1, padx=10, pady=5)

destination_label = tk.Label(root, text="Destination City:")
destination_label.grid(row=1, column=0, padx=10, pady=5)
destination_city_entry = tk.Entry(root)
destination_city_entry.grid(row=1, column=1, padx=10, pady=5)

find_path_button = tk.Button(root, text="Find Shortest Path", command=find_shortest_path)
find_path_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

shortest_path_label = tk.Label(root, text="")
shortest_path_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()
