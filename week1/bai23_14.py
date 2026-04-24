import osmnx as ox
import networkx as nx
import folium
from folium.plugins import TimestampedGeoJson
import pandas as pd
from datetime import datetime, timedelta

# --- BƯỚC 1: TẢI ĐỒ THỊ VÀ TÌM ĐƯỜNG ĐI ---
place_name = "Tan Binh District, Ho Chi Minh City, Vietnam"
G = ox.graph_from_place(place_name, network_type='drive')

# Chọn 2 tọa độ (Sân bay -> Lotte Mart Cộng Hòa)
orig_node = ox.distance.nearest_nodes(G, 106.6635, 10.8165)
dest_node = ox.distance.nearest_nodes(G, 106.6533, 10.7925)

# Tìm đường ngắn nhất
route = nx.shortest_path(G, orig_node, dest_node, weight='length')

# --- BƯỚC 2: TẠO DỮ LIỆU THỜI GIAN (SIMULATION LOGIC) ---
features = []
start_time = datetime(2026, 4, 24, 10, 0, 0) # Thời gian bắt đầu simulation

for i, node in enumerate(route):
    # Lấy tọa độ nút
    lat = G.nodes[node]['y']
    lon = G.nodes[node]['x']
    
    # Giả lập mỗi bước di chuyển mất 30 giây
    current_time = (start_time + timedelta(seconds=i * 30)).isoformat()
    
    # Tạo Feature cho từng vị trí của xe tại thời điểm đó
    feature = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [lon, lat], # GeoJSON dùng [lon, lat]
        },
        'properties': {
            'time': current_time,
            'style': {'color': 'red'},
            'icon': 'marker',
            'iconstyle': {
                'iconSize': [20, 20],
                'className': 'fa fa-car', # Icon xe hơi
            },
            'popup': f"Trạng thái: Đang di chuyển<br>Bước: {i}<br>Thời gian: {current_time}"
        }
    }
    features.append(feature)

# --- BƯỚC 3: TRỰC QUAN HÓA TRÊN BẢN ĐỒ ---
m = folium.Map(location=[10.8015, 106.6508], zoom_start=14)

# Thêm plugin TimestampedGeoJson
TimestampedGeoJson(
    {'type': 'FeatureCollection', 'features': features},
    period='PT30S', # Bước nhảy 30 giây
    add_last_point=True,
    auto_play=False,
    loop=False,
    max_speed=1,
    loop_button=True,
    date_options='YYYY-MM-DD HH:mm:ss',
    time_slider_drag_update=True
).add_to(m)

# Lưu file
m.save("vehicle_simulation.html")
print("Mô phỏng đã sẵn sàng! Hãy mở file vehicle_simulation.html và nhấn nút Play.")