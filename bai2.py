import osmnx as ox
import matplotlib.pyplot as plt
import random
import pandas as pd

# --- BƯỚC 1: TẢI BẢN ĐỒ ---
place_name = "Tan Binh District, Ho Chi Minh City, Vietnam"
print("Đang tải bản đồ khu vực...")
graph = ox.graph_from_place(place_name, network_type='drive')
nodes, edges = ox.graph_to_gdfs(graph)

# --- BƯỚC 2: TẠO DỮ LIỆU GIẢ LẬP (XE VÀ KHÁCH) ---
# Chọn ngẫu nhiên 5 vị trí làm Khách hàng và 3 vị trí làm Xe công nghệ
all_node_ids = list(graph.nodes)
customer_nodes = random.sample(all_node_ids, 5)
car_nodes = random.sample(all_node_ids, 3)

# Lấy tọa độ (x, y) của khách và xe để tính toán
customers = nodes.loc[customer_nodes, ['x', 'y']]
cars = nodes.loc[car_nodes, ['x', 'y']]

# --- BƯỚC 3: THUẬT TOÁN HEURISTIC (NEAREST NEIGHBOR CÓ LOẠI TRỪ) ---
assignments = []
used_cars = []  # Lưu xe đã được gán

for c_id, customer in customers.iterrows():
    best_car_id = None
    min_dist = float('inf')
    
    for car_id, car in cars.iterrows():
        if car_id in used_cars:  # Xe đã có khách thì bỏ qua
            continue
            
        dist = ((customer['x'] - car['x'])**2 + (customer['y'] - car['y'])**2)**0.5
        
        if dist < min_dist:
            min_dist = dist
            best_car_id = car_id
    
    if best_car_id:
        assignments.append((c_id, best_car_id))
        used_cars.append(best_car_id)

print(f"\nĐã ghép được {len(assignments)}/{len(customers)} khách với xe")

# --- BƯỚC 4: TRỰC QUAN HÓA ---
print("Đang xử lý hình ảnh ghép cặp...")
fig, ax = ox.plot_graph(graph, show=False, close=False, edge_color='#ddd', node_size=0)

# Vẽ Khách hàng (Màu đỏ) và Xe (Màu xanh dương)
ax.scatter(customers['x'], customers['y'], c='red', s=100, label='Khách hàng', zorder=5)
ax.scatter(cars['x'], cars['y'], c='blue', s=150, marker='s', label='Xe trống', zorder=5)

# Vẽ đường nối giữa khách và xe được gán (Đường màu xanh lá)
for c_id, car_id in assignments:
    start = nodes.loc[c_id]
    end = nodes.loc[car_id]
    ax.plot([start['x'], end['x']], [start['y'], end['y']], 
            c='green', linestyle='--', linewidth=2, zorder=6)

plt.legend()
print("Hoàn thành! Bạn hãy xem bản đồ mô phỏng.")
plt.show()