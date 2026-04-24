import osmnx as ox
import networkx as nx
import folium
import numpy as np
from geopy.distance import geodesic

# --- BƯỚC 1: CÀI ĐẶT BẢN ĐỒ VÀ DỮ LIỆU ---
place_name = "Tan Binh District, Ho Chi Minh City, Vietnam"
G = ox.graph_from_place(place_name, network_type='drive')

# Tọa độ 2 Kho hàng (Depots)
depots = {
    'Kho A (Phía Bắc)': [10.815, 106.655],
    'Kho B (Phía Nam)': [10.785, 106.645]
}

# Giả lập 10 điểm giao hàng (Customers)
customers = [
    [10.810, 106.650], [10.820, 106.660], [10.805, 106.670], [10.812, 106.640], [10.798, 106.655],
    [10.780, 106.640], [10.790, 106.635], [10.775, 106.650], [10.782, 106.655], [10.795, 106.648]
]

# --- BƯỚC 2: PHÂN VÙNG (Gán khách hàng về kho gần nhất) ---
assignments = {name: [] for name in depots}
for cust in customers:
    closest_depot = min(depots.keys(), key=lambda d: geodesic(cust, depots[d]).meters)
    assignments[closest_depot].append(cust)

# --- BƯỚC 3: THUẬT TOÁN TỐI ƯU TUYẾN ĐƯỜNG (TSP Heuristic) ---
def find_optimized_route(depot_coords, customer_list):
    route = [depot_coords]
    unvisited = list(customer_list)
    total_dist = 0
    
    current = depot_coords
    while unvisited:
        # Tìm khách hàng gần nhất với vị trí hiện tại
        next_cust = min(unvisited, key=lambda c: geodesic(current, c).meters)
        total_dist += geodesic(current, next_cust).meters
        route.append(next_cust)
        unvisited.remove(next_cust)
        current = next_cust
    
    # Quay trở về kho
    total_dist += geodesic(current, depot_coords).meters
    route.append(depot_coords)
    return route, total_dist

# --- BƯỚC 4: TÍNH TOÁN VÀ TRỰC QUAN HÓA ---
m = folium.Map(location=[10.8015, 106.6508], zoom_start=14)
colors = ['blue', 'green']
total_opt_dist = 0
total_random_dist = 0

for i, (name, cust_list) in enumerate(assignments.items()):
    # 1. Tính toán lộ trình tối ưu
    opt_route, d_opt = find_optimized_route(depots[name], cust_list)
    total_opt_dist += d_opt
    
    # 2. Giả lập lộ trình không tối ưu (đi theo thứ tự ngẫu nhiên)
    _, d_random = find_optimized_route(depots[name], sorted(cust_list, key=lambda x: np.random.rand()))
    total_random_dist += d_random # Giả lập này đơn giản để so sánh
    
    # Vẽ lên bản đồ
    folium.PolyLine(opt_route, color=colors[i], weight=5, opacity=0.8, popup=f"Tuyến {name}").add_to(m)
    folium.Marker(depots[name], popup=name, icon=folium.Icon(color='red', icon='home')).add_to(m)
    for c in cust_list:
        folium.CircleMarker(c, radius=5, color=colors[i], fill=True).add_to(m)

m.save("delivery_optimization.html")

# --- BƯỚC 5: ĐÁNH GIÁ HIỆU QUẢ ---
print(f"--- KẾT QUẢ SO SÁNH ---")
print(f"Tổng quãng đường KHÔNG tối ưu: {total_random_dist/1000:.2f} km")
print(f"Tổng quãng đường TỐI ƯU (AI): {total_opt_dist/1000:.2f} km")
efficiency = (total_random_dist - total_opt_dist) / total_random_dist * 100
print(f"=> Hiệu quả tiết kiệm: {efficiency:.1f}%")