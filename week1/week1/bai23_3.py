import folium
from folium.plugins import HeatMap
import numpy as np

# --- BƯỚC 1: XÁC ĐỊNH KHU VỰC TRUNG TÂM (Tân Bình) ---
center_coords = [10.8015, 106.6508]
m = folium.Map(location=center_coords, zoom_start=14)

# --- BƯỚC 2: GIẢ LẬP DỮ LIỆU (1000 điểm đơn hàng) ---
# Chúng ta tạo ra các tọa độ ngẫu nhiên xung quanh khu vực trung tâm
# Trong thực tế, dữ liệu này bạn sẽ lấy từ file Excel hoặc Database
data = (
    np.random.normal(size=(1000, 2)) * 0.01 + center_coords
).tolist()

# --- BƯỚC 3: TẠO BẢN ĐỒ NHIỆT (HEATMAP) ---
# Thêm lớp dữ liệu nhiệt vào bản đồ
HeatMap(data, radius=15, blur=10, min_opacity=0.5).add_to(m)

# Thêm một Marker để đánh dấu tâm khu vực
folium.Marker(center_coords, popup="Tâm khu vực phân tích").add_to(m)

# --- BƯỚC 4: LƯU VÀ XEM KẾT QUẢ ---
m.save("heatmap_tan_binh.html")
print("Đã tạo xong bản đồ nhiệt! Bạn hãy mở file heatmap_tan_binh.html.")