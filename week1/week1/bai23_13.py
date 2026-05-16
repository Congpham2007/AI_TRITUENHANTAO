import folium
from folium import plugins

# --- BƯỚC 1: KHỞI TẠO DASHBOARD ---
center_coords = [10.7769, 106.7009] # Trung tâm Quận 1
m = folium.Map(location=center_coords, zoom_start=15, control_scale=True)

# --- BƯỚC 2: TẠO CÁC LỚP DỮ LIỆU RIÊNG BIỆT (FEATURE GROUPS) ---
fg_stores = folium.FeatureGroup(name="Cửa hàng bán lẻ (Điểm)", show=True)
fg_coverage = folium.FeatureGroup(name="Vùng phủ sóng (Vùng)", show=False)
fg_logistics = folium.FeatureGroup(name="Tuyến vận tải (Tuyến)", show=True)

# Dữ liệu giả lập
stores = {
    "Vincom Center": [10.7780, 106.7020],
    "Diamond Plaza": [10.7815, 106.6985],
    "Takashimaya": [10.7735, 106.7015]
}

# 1. THÊM LỚP ĐIỂM: Các cửa hàng
for name, coords in stores.items():
    folium.Marker(
        location=coords,
        popup=f"<b>Cửa hàng:</b> {name}<br><b>Trạng thái:</b> Đang hoạt động",
        icon=folium.Icon(color='blue', icon='shopping-cart', prefix='fa')
    ).add_to(fg_stores)

# 2. THÊM LỚP VÙNG: Bán kính 500m quanh cửa hàng để phân tích mật độ khách hàng
for coords in stores.values():
    folium.Circle(
        location=coords,
        radius=500,
        color='orange',
        fill=True,
        fill_opacity=0.2,
        popup="Vùng ảnh hưởng 500m"
    ).add_to(fg_coverage)

# 3. THÊM LỚP TUYẾN: Kết nối giữa các điểm để biểu thị luồng hàng hóa
route_coords = [stores["Diamond Plaza"], stores["Vincom Center"], stores["Takashimaya"]]
folium.PolyLine(
    locations=route_coords,
    color='green',
    weight=4,
    opacity=0.7,
    popup="Tuyến vận chuyển nội bộ"
).add_to(fg_logistics)

# --- BƯỚC 3: TÍCH HỢP CÁC TIỆN ÍCH TƯƠNG TÁC ---
# Thêm các lớp vào bản đồ
fg_stores.add_to(m)
fg_coverage.add_to(m)
fg_logistics.add_to(m)

# Thêm công cụ Bật/Tắt lớp (Trái tim của Dashboard)
folium.LayerControl(collapsed=False).add_to(m)

# Thêm công cụ tìm kiếm vị trí
plugins.Search(layer=fg_stores, geom_type='Point', placeholder="Tìm kiếm cửa hàng...", 
               collapsed=True, search_label='popup').add_to(m)

# Thêm công cụ xem bản đồ toàn màn hình
plugins.Fullscreen().add_to(m)

# --- BƯỚC 4: LƯU DASHBOARD ---
m.save("management_dashboard.html")
print("Dashboard đã sẵn sàng! Hãy mở file management_dashboard.html bằng trình duyệt.")