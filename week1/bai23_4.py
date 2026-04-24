import geopandas as gpd
import osmnx as ox
import matplotlib.pyplot as plt
import pandas as pd

# --- BƯỚC 1: ĐỌC DỮ LIỆU RANH GIỚI HÀNH CHÍNH ---
# Thầy chọn 3 quận tiêu biểu để em dễ quan sát
districts_names = [
    "District 1, Ho Chi Minh City, Vietnam",
    "District 3, Ho Chi Minh City, Vietnam",
    "Tan Binh District, Ho Chi Minh City, Vietnam"
]

print("Đang tải dữ liệu ranh giới các quận...")
# ox.geocode_to_gdf trả về một GeoDataFrame chứa ranh giới các quận
boundaries = ox.geocode_to_gdf(districts_names)

# --- BƯỚC 2: TẠO TẬP DỮ LIỆU SỐ (Giả lập doanh thu) ---
# Chúng ta tạo một bảng dữ liệu thông thường (DataFrame)
data = {
    'display_name': boundaries['display_name'].tolist(),
    'revenue': [850, 420, 680]  # Doanh thu giả lập cho từng quận (triệu USD)
}
df_revenue = pd.DataFrame(data)

# --- BƯỚC 3: KẾT HỢP DỮ LIỆU (MERGE) ---
# Kết hợp ranh giới và doanh thu dựa trên cột tên quận
# Đây chính là kỹ năng Merge bảng mà em đã học ở phần Pandas
merged = boundaries.merge(df_revenue, on='display_name')

# --- BƯỚC 4: VẼ BẢN ĐỒ CHOROPLETH ---
fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Vẽ bản đồ phân màu theo cột 'revenue'
merged.plot(column='revenue', 
            ax=ax, 
            legend=True, 
            cmap='YlOrRd',  # Màu từ Vàng sang Đỏ (vùng đỏ là doanh thu cao)
            legend_kwds={'label': "Doanh thu (triệu USD)", 'orientation': "horizontal"})

# Thêm tên quận lên bản đồ cho trực quan
for idx, row in merged.iterrows():
    # Lấy tọa độ tâm của mỗi quận để đặt nhãn
    centroid = row['geometry'].centroid
    plt.annotate(text=row['display_name'].split(',')[0], 
                 xy=(centroid.x, centroid.y),
                 horizontalalignment='center', fontsize=8, fontweight='bold')

plt.title("BẢN ĐỒ PHÂN BỔ DOANH THU THEO KHU VỰC")
plt.axis('off') # Tắt trục tọa độ cho đẹp
plt.show()