import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time

# --- BƯỚC 1: XÁC ĐỊNH ĐIỂM TRUNG TÂM (UEH) ---
center_address = "59C Nguyễn Đình Chiểu, Quận 3, Hồ Chí Minh"
center_coords = (10.7811, 106.6953) # Tọa độ UEH Cơ sở A

# --- BƯỚC 2: GIẢ LẬP DANH SÁCH 10 ĐỊA CHỈ ---
addresses = [
    "Dinh Độc Lập, Quận 1, Hồ Chí Minh",
    "Nhà thờ Đức Bà, Quận 1, Hồ Chí Minh",
    "Chợ Bến Thành, Quận 1, Hồ Chí Minh",
    "Bảo tàng Chứng tích Chiến tranh, Quận 3, Hồ Chí Minh",
    "Diamond Plaza, Quận 1, Hồ Chí Minh",
    "Hồ Con Rùa, Quận 3, Hồ Chí Minh",
    "Công viên Tao Đàn, Quận 1, Hồ Chí Minh",
    "Thảo Cầm Viên, Quận 1, Hồ Chí Minh",
    "Bitexco Financial Tower, Quận 1, Hồ Chí Minh",
    "Sân vận động Thống Nhất, Quận 10, Hồ Chí Minh"
]

# Khởi tạo công cụ chuyển đổi địa chỉ (Geocoding)
geolocator = Nominatim(user_agent="my_ai_app")

# Tạo bản đồ ban đầu
m = folium.Map(location=center_coords, zoom_start=14)

# Thêm Marker cho điểm trung tâm UEH
folium.Marker(
    location=center_coords,
    popup="ĐIỂM TRUNG TÂM: UEH",
    icon=folium.Icon(color='red', icon='star')
).add_to(m)

print("Đang xử lý địa chỉ và tính khoảng cách...")

# --- BƯỚC 3: XỬ LÝ TỪNG ĐỊA CHỈ ---
for addr in addresses:
    try:
        # Chuyển địa chỉ thành tọa độ
        location = geolocator.geocode(addr)
        
        if location:
            point_coords = (location.latitude, location.longitude)
            
            # Tính khoảng cách đến trung tâm (đơn vị: km)
            dist = geodesic(center_coords, point_coords).kilometers
            
            # Vẽ Marker cho từng địa điểm
            folium.Marker(
                location=point_coords,
                popup=f"{addr}<br>Khoảng cách: {dist:.2f} km",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)
            
            # Vẽ đường thẳng (PolyLine) nối từ trung tâm đến điểm đó để thấy mối quan hệ không gian
            folium.PolyLine(
                locations=[center_coords, point_coords],
                color='green',
                weight=2,
                dash_array='5, 5'
            ).add_to(m)
            
            print(f"Đã xử lý: {addr} ({dist:.2f} km)")
            
        # Nghỉ 1 giây để không bị chặn bởi dịch vụ bản đồ
        time.sleep(1) 
        
    except Exception as e:
        print(f"Lỗi khi xử lý {addr}: {e}")

# --- BƯỚC 4: LƯU VÀ XEM KẾT QUẢ ---
m.save("geopy_distance_map.html")
print("\nHoàn thành! Bạn hãy mở file geopy_distance_map.html để xem bản đồ.")