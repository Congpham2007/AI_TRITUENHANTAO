# bài 1
import osmnx as ox
import matplotlib.pyplot as plt

place_name = "Tan Binh District, Ho Chi Minh City, Vietnam"

print(f"Đang tải dữ liệu giao thông của: {place_name}...")

graph = ox.graph_from_place(place_name, network_type='drive')

print("Đang vẽ bản đồ Quận Tân Bình...")
ox.plot_graph(graph, node_size=5, node_color='blue', edge_color='green')

# Lấy diện tích (dùng features_from_place thay vì geometries_from_place)
# try:
area = ox.features_from_place(place_name, tags={'boundary':'administrative'}).area.sum() / 1000000
# except:
#     # Nếu vẫn lỗi, dùng cách khác
#     gdf = ox.geocode_to_gdf(place_name)
#     area = gdf.area.sum() / 1000000

# Tính mật độ
stats = ox.basic_stats(graph)
total_length_km = stats['street_length_total'] / 1000
street_density = total_length_km / area

print("\n--- KẾT QUẢ PHÂN TÍCH TÂN BÌNH ---")
print(f"1. Số lượng nút giao: {stats['n']}")
print(f"2. Chiều dài đường trung bình: {stats['edge_length_avg']:.2f} mét")
print(f"3. Mật độ mạng giao thông: {street_density:.5f} km/km²")

