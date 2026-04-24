import osmnx as ox
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# --- BƯỚC 1: TẢI BẢN ĐỒ VÀ XÁC ĐỊNH CÁC KHU VỰC ---
place_name = "Tan Binh District, Ho Chi Minh City, Vietnam"
print("Đang tải bản đồ...")
graph = ox.graph_from_place(place_name, network_type='drive')
nodes, edges = ox.graph_to_gdfs(graph)

# Chọn 4 khu vực khác nhau trong quận (mỗi khu vực là 1 nút)
area_nodes = nodes.sample(4)
area_names = ['Khu trung tâm', 'Khu dân cư', 'Khu trường học', 'Khu văn phòng']

# --- BƯỚC 2: TẠO DỮ LIỆU LỊCH SỬ CHO TỪNG KHU VỰC ---
# Giả lập: mỗi khu vực có đặc điểm nhu cầu khác nhau
historical_data = {}

area_demand_profiles = {
    'Khu trung tâm': {'peak_hour': 8, 'peak_demand': 90},
    'Khu dân cư': {'peak_hour': 19, 'peak_demand': 70},
    'Khu trường học': {'peak_hour': 7, 'peak_demand': 60},
    'Khu văn phòng': {'peak_hour': 17, 'peak_demand': 85}
}

# Dự đoán nhu cầu cho từng khu vực lúc 17h
predictions = {}
next_hour = 17

print(f"\n--- DỰ BÁO NHU CẦU LÚC {next_hour}:00 ---")

for i, (node_id, node_row) in enumerate(area_nodes.iterrows()):
    area_name = area_names[i]
    profile = area_demand_profiles[area_name]
    
    # Tạo dữ liệu lịch sử cho khu vực (dạng parabol: thấp vào sáng sớm, cao vào giờ cao điểm)
    hours = list(range(6, 22))  # 6h đến 21h
    demands = []
    for h in hours:
        # Công thức giả lập: đỉnh cao tại peak_hour
        demand = profile['peak_demand'] * (1 - 0.02 * abs(h - profile['peak_hour'])**1.5)
        demand = max(10, int(demand))
        demands.append(demand)
    
    # Tạo DataFrame và huấn luyện riêng cho từng khu vực
    df_area = pd.DataFrame({'hour': hours, 'demand': demands})
    model = LinearRegression()
    model.fit(df_area[['hour']], df_area['demand'])
    
    # Dự báo cho next_hour
    pred = model.predict([[next_hour]])[0]
    predictions[area_name] = max(10, int(pred))
    
    print(f"- {area_name}: {predictions[area_name]} cuốc xe")

# --- BƯỚC 3: TRỰC QUAN HÓA TRÊN BẢN ĐỒ ---
print("\nĐang vẽ bản đồ dự báo...")
fig, ax = ox.plot_graph(graph, show=False, close=False, edge_color='#ccc', node_size=0)

# Vẽ từng khu vực với kích thước khác nhau theo nhu cầu dự báo
for i, (node_id, node_row) in enumerate(area_nodes.iterrows()):
    area_name = area_names[i]
    demand = predictions[area_name]
    
    # Kích thước vòng tròn tỷ lệ với nhu cầu
    size = demand * 5
    
    # Màu sắc theo mức nhu cầu
    if demand >= 70:
        color = 'red'
    elif demand >= 40:
        color = 'orange'
    else:
        color = 'green'
    
    ax.scatter(node_row['x'], node_row['y'], s=size, c=color, alpha=0.7, 
               label=f'{area_name}: {demand} cuốc', zorder=5)

plt.title(f"Dự báo nhu cầu gọi xe lúc {next_hour}:00 - Quận Tân Bình")
plt.legend(loc='upper right', fontsize=8)
plt.tight_layout()
plt.show()

# --- BƯỚC 4: PHÂN TÍCH SỰ KHÁC BIỆT GIỮA CÁC KHU VỰC ---
print("\n--- PHÂN TÍCH KHÁC BIỆT NHU CẦU GIỮA CÁC KHU VỰC ---")

max_area = max(predictions, key=predictions.get)
min_area = min(predictions, key=predictions.get)

print(f"Khu vực có nhu cầu cao nhất: {max_area} ({predictions[max_area]} cuốc)")
print(f"Khu vực có nhu cầu thấp nhất: {min_area} ({predictions[min_area]} cuốc)")
print(f"Chênh lệch: {predictions[max_area] - predictions[min_area]} cuốc xe")
