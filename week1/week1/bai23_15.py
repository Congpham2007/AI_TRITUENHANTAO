import folium
from folium.plugins import HeatMap
import numpy as np
import pandas as pd

# --- BƯỚC 1: GIẢ LẬP DỮ LIỆU THỊ TRƯỜNG ---
center_coords = [10.7769, 106.7009]

# 1. Giả lập 1000 điểm khách hàng tiềm năng (Nhu cầu)
np.random.seed(1)
demand_data = np.random.normal(size=(1000, 2)) * 0.008 + center_coords

# 2. Giả lập 15 cửa hàng đối thủ đã tồn tại (Cạnh tranh)
competition_data = np.random.normal(size=(15, 2)) * 0.005 + center_coords

# --- BƯỚC 2: TRỰC QUAN HÓA CHIẾN LƯỢC ---
m = folium.Map(location=center_coords, zoom_start=15, tiles="CartoDB positron")

# Lớp 1: Bản đồ nhiệt thể hiện nhu cầu khách hàng (Vùng nóng = Khách đông)
HeatMap(demand_data.tolist(), radius=15, blur=20, name="Mật độ Nhu cầu").add_to(m)

# Lớp 2: Đánh dấu đối thủ cạnh tranh (Marker màu đỏ)
fg_competition = folium.FeatureGroup(name="Đối thủ cạnh tranh")
for coord in competition_data:
    folium.CircleMarker(
        location=coord,
        radius=7,
        color='red',
        fill=True,
        fill_color='red',
        popup="Cửa hàng đối thủ"
    ).add_to(fg_competition)
fg_competition.add_to(m)

# Lớp 3: AI đề xuất "Vùng Đất Vàng" (Điểm có Nhu cầu cao nhưng xa Đối thủ)
# Thầy dùng logic đơn giản: Tìm trọng tâm vùng đông khách nhất chưa có đối thủ
golden_spot = [10.7810, 106.7080] # Tọa độ giả lập sau khi AI tính toán
folium.Marker(
    location=golden_spot,
    popup="<b>VỊ TRÍ CHIẾN LƯỢC ĐỀ XUẤT</b><br>Tiềm năng: Rất cao<br>Cạnh tranh: Thấp",
    icon=folium.Icon(color='gold', icon='trophy', prefix='fa')
).add_to(m)

# Thêm bộ lọc lớp
folium.LayerControl().add_to(m)

# Lưu kết quả
m.save("retail_ai_strategy.html")
print("Hệ thống phân tích đã hoàn tất! Hãy mở file retail_ai_strategy.html.")