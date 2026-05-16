import osmnx as ox
import networkx as nx
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import math
geolocator = Nominatim(user_agent = "geoapi")
place = "District 1, Ho Chi Minh City, Viet Nam"
G = ox.graph_from_place(place, network_type ="drive")

#Điểm đầu
start = "Ben Thanh Market, TP.HCM"
start_location = geolocator.geocode(start)
start_coords = (start_location.latitude, start_location.longitude)
#Diểm cuối
last = "Bitexco Financial Tower, TP.HCM"
last_location = geolocator.geocode(last)
last_coords = (last_location.latitude, last_location.longitude)

#Tìm node gần nhất
start_node = ox.distance.nearest_nodes(G, start_location.longitude, start_location.latitude)
last_node = ox.distance.nearest_nodes(G, last_location.longitude, last_location.latitude)

#dijkstra
dijkstra_path = nx.dijkstra_path(G, start_node, last_node, weight='length')
dijkstra_length = nx.dijkstra_path_length(G, start_node, last_node, weight='length')

#heuristic
def heuristic(u, v):
    y1 = G.nodes[u]['y']
    x1 = G.nodes[u]['x']
    y2 = G.nodes[v]['y']
    x2 = G.nodes[v]['x']
    return geodesic((y1, x1), (y2, x2)).meters
#A*
astar_path = nx.astar_path(G, start_node, last_node, heuristic=heuristic, weight='length')
astar_length = nx.astar_path_length(G, start_node, last_node, heuristic=heuristic, weight='length')

#Vẽ
fig1, ax1 = ox.plot_graph_route(
    G,
    dijkstra_path,
    route_color='red',
    route_linewidth=4,
    node_size=0,
    bgcolor='white',
    show=False,
    close=False
)
ax1.set_title("Dijkstra Shortest Path")

fig2, ax2 = ox.plot_graph_route(
    G,
    astar_path,
    route_color='red',
    route_linewidth=4,
    node_size=0,
    bgcolor='white',
    show=False,
    close=False
)
ax2.set_title("A* Shortest Path")
plt.show()


print("Dijkstra path:", dijkstra_path)
print(f"Dijkstra distance: {(dijkstra_length/1000):.2f} km")

print("A* path:", astar_path)
print(f"A* distance: {(astar_length/1000):.2f} km")




