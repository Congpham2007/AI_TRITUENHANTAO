import folium

# --- BƯỚC 1: XÁC ĐỊNH VỊ TRÍ UEH (Cơ sở A - 59C Nguyễn Đình Chiểu) ---
ueh_coords = [10.7811, 106.6953]

# Khởi tạo bản đồ, bắt đầu tại vị trí UEH với độ phóng (zoom) là 16
my_map = folium.Map(location=ueh_coords, zoom_start=16)

# --- BƯỚC 2: TẠO CÁC LỚP DỮ LIỆU (LAYERS) ---
# Thầy chia làm 2 lớp: Một lớp cho UEH và một lớp cho các địa điểm công cộng
ueh_layer = folium.FeatureGroup(name='Đại học UEH')
public_layer = folium.FeatureGroup(name='Địa điểm công cộng lân cận')

# --- BƯỚC 3: THÊM MARKER CHO UEH ---
folium.Marker(
    location=ueh_coords,
    popup='Đại học Kinh tế TP.HCM (UEH) - Cơ sở A',
    tooltip='Bấm để xem chi tiết',
    icon=folium.Icon(color='red', icon='university', prefix='fa')
).add_to(ueh_layer)

# --- BƯỚC 4: THÊM 5 ĐỊA ĐIỂM CÔNG CỘNG LÂN CẬN ---
# Danh sách địa điểm: [Tọa độ], Tên, Loại hình
locations = [
    ([10.7828, 106.6958], "Hồ Con Rùa", "Địa điểm văn hóa/Công cộng"),
    ([10.7815, 106.6985], "Diamond Plaza", "Trung tâm thương mại"),
    ([10.7835, 106.6995], "Bệnh viện Nhi Đồng 2", "Bệnh viện"),
    ([10.7790, 106.6915], "Dinh Độc Lập", "Cơ quan hành chính/Di tích"),
    ([10.7775, 106.6945], "Nhà thờ Đức Bà", "Địa điểm du lịch công cộng")
]

for coords, name, desc in locations:
    folium.Marker(
        location=coords,
        popup=f"<b>{name}</b><br>{desc}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(public_layer)

# --- BƯỚC 5: TÍCH HỢP VÀO BẢN ĐỒ ---
ueh_layer.add_to(my_map)
public_layer.add_to(my_map)

# Thêm bộ điều khiển bật/tắt lớp dữ liệu
folium.LayerControl().add_to(my_map)

# --- BƯỚC 6: LƯU BẢN ĐỒ ---
my_map.save("ueh_map.html")
print("Đã tạo xong bản đồ! Bạn hãy mở file ueh_map.html bằng trình duyệt.")