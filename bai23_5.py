import folium

# --- BƯỚC 1: XÁC ĐỊNH VỊ TRÍ KHO HÀNG ---
warehouse_coords = [10.8165, 106.6635]  # Gần sân bay Tân Sơn Nhất

m = folium.Map(location=warehouse_coords, zoom_start=12)

# --- BƯỚC 2: VẼ CÁC VÒNG BÁN KÍNH ---
radii = [
    (10000, 'red', 'Vùng xa (10km) - Cần hỗ trợ đối tác'),
    (5000, 'orange', 'Vùng tiêu chuẩn (5km) - Giao hàng 2-4h'),
    (3000, 'green', 'Vùng ưu tiên (3km) - Giao hỏa tốc <1h')
]

for radius, color, label in radii:
    folium.Circle(
        location=warehouse_coords,
        radius=radius,
        color=color,
        fill=True,
        fill_opacity=0.2,
        popup=label
    ).add_to(m)

# --- BƯỚC 3: MARKER KHO HÀNG ---
folium.Marker(
    location=warehouse_coords,
    popup="<b>Trung tâm phân phối Tân Bình</b>",
    icon=folium.Icon(color='blue', icon='home')
).add_to(m)

# --- BƯỚC 4: GIẢ LẬP KHÁCH HÀNG ---
customers = [
    ([10.8250, 106.6300], "Khách A - Trong vùng 3km"),
    ([10.7900, 106.7000], "Khách B - Trong vùng 5km"),
    ([10.7500, 106.6600], "Khách C - Trong vùng 10km")
]

for c_coords, c_name in customers:
    folium.CircleMarker(
        location=c_coords,
        radius=5,
        color='black',
        fill=True,
        popup=c_name
    ).add_to(m)

m.save("service_area_analysis.html")

# --- BƯỚC 5: ĐÁNH GIÁ VÀ ĐỀ XUẤT ---
print("\n" + "="*65)
print("PHÂN TÍCH VÙNG PHỤC VỤ & ĐỀ XUẤT PHẠM VI TỐI ƯU")
print("="*65)

print("\n ĐÁNH GIÁ KHẢ NĂNG TIẾP CẬN:")
print(" Vùng 3km: Tiếp cận nhanh (<1h) - Phù hợp giao hàng hỏa tốc")
print(" Vùng 5km: Tiếp cận trung bình (2-4h) - Phù hợp giao hàng ngày")
print(" Vùng 10km: Tiếp cận chậm (4-8h) - Cần đối tác vận chuyển")

print("\n ĐỀ XUẤT PHẠM VI HOẠT ĐỘNG TỐI ƯU: 5km")
print("   - Lý do: Cân bằng giữa chi phí vận chuyển và độ phủ khách hàng")
print("   - Trong 3km: Áp dụng giao hàng hỏa tốc, phí cao")
print("   - 3-5km: Giao hàng tiêu chuẩn, phí trung bình")
print("   - Ngoài 5km: Hợp tác với đối tác logistics")

print("\n Đã xuất bản đồ: service_area_analysis.html")