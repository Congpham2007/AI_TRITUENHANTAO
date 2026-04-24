import osmnx as ox
import folium
import random
import networkx as nx

# --- BƯỚC 1: TẢI DỮ LIỆU KHU VỰC (Ví dụ: Quận 1) ---
place_name = "District 1, Ho Chi Minh City, Vietnam"
print("Đang phân tích mạng lưới giao thông...")
G = ox.graph_from_place(place_name, network_type='drive')

# --- BƯỚC 2: GIẢ LẬP DỮ LIỆU TẮC NGHẼN (Mô hình logic đơn giản) ---
# Chúng ta giả lập mỗi con đường có một "chỉ số tắc nghẽn" từ 0 đến 1
# 0.0 - 0.7: Giao thông thông suốt
# 0.7 - 1.0: Nguy cơ tắc nghẽn cao
edge_risk = {}
for u, v, k, data in G.edges(keys=True, data=True):
    # Trong thực tế, AI sẽ tính số này dựa trên camera hoặc GPS
    risk_score = random.uniform(0, 1) 
    G[u][v][k]['risk_score'] = risk_score
    # Nếu tắc nghẽn, ta tăng "chi phí" đi qua đường đó để AI tìm đường tránh
    G[u][v][k]['travel_weight'] = data['length'] * (1 + risk_score * 5)

# --- BƯỚC 3: TÌM TUYẾN ĐƯỜNG THAY THẾ ---
# Chọn 2 điểm bất kỳ để mô phỏng việc tìm đường tránh tắc đường
nodes_list = list(G.nodes)
orig, dest = nodes_list[0], nodes_list[len(nodes_list)//2]

# Tuyến đường ngắn nhất (nhưng có thể bị tắc)
route_shortest = nx.shortest_path(G, orig, dest, weight='length')
# Tuyến đường AI đề xuất (tránh các vùng có risk_score cao)
route_ai_avoid = nx.shortest_path(G, orig, dest, weight='travel_weight')

# --- BƯỚC 4: TRỰC QUAN HÓA TRÊN BẢN ĐỒ FOLIUM ---
m = folium.Map(location=[10.7769, 106.7009], zoom_start=15)

# 1. Vẽ các vùng rủi ro tắc nghẽn (Màu đỏ đậm cho vùng nguy cơ cao)
for u, v, k, data in G.edges(keys=True, data=True):
    if data['risk_score'] > 0.8: # Ngưỡng nguy cơ cao
        point1 = [G.nodes[u]['y'], G.nodes[u]['x']]
        point2 = [G.nodes[v]['y'], G.nodes[v]['x']]
        folium.PolyLine([point1, point2], color="red", weight=5, opacity=0.8, 
                        popup="Vùng nguy cơ tắc nghẽn cao").add_to(m)

# 2. Vẽ tuyến đường AI đề xuất (Màu xanh lá)
path_coords = [[G.nodes[node]['y'], G.nodes[node]['x']] for node in route_ai_avoid]
folium.PolyLine(path_coords, color="green", weight=7, opacity=1, 
                popup="Tuyến đường thay thế AI đề xuất").add_to(m)

# Lưu bản đồ
m.save("traffic_congestion_analysis.html")
print("Hoàn thành! Hãy mở file traffic_congestion_analysis.html để xem vùng rủi ro.")