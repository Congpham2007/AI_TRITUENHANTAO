import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import folium

# --- BƯỚC 1: GIẢ LẬP DỮ LIỆU VỊ TRÍ ĐƠN HÀNG ---
# Tọa độ trung tâm Tân Bình
center_lat, center_lon = 10.8015, 106.6508

# Tạo 200 đơn hàng ngẫu nhiên quanh khu vực này
np.random.seed(42)
lats = center_lat + (np.random.rand(200) - 0.5) * 0.05
lons = center_lon + (np.random.rand(200) - 0.5) * 0.05
data = pd.DataFrame({'lat': lats, 'lon': lons})

# --- BƯỚC 2: ÁP DỤNG THUẬT TOÁN K-MEANS ---
# Giả sử chúng ta muốn đặt 3 kho hàng (n_clusters=3)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
data['cluster'] = kmeans.fit_predict(data[['lat', 'lon']])

# Lấy tọa độ các tâm cụm (Centroids) - Đây chính là vị trí kho hàng tối ưu
centroids = kmeans.cluster_centers_

# --- BƯỚC 3: TRỰC QUAN HÓA TRÊN BẢN ĐỒ ---
m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

# Màu sắc cho từng cụm
colors = ['red', 'blue', 'green']

# Vẽ các đơn hàng (nhỏ) theo màu cụm
for i, row in data.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=3,
        color=colors[int(row['cluster'])],
        fill=True,
        opacity=0.5
    ).add_to(m)

# Vẽ các vị trí kho hàng tối ưu (Marker lớn)
for i, coord in enumerate(centroids):
    folium.Marker(
        location=[coord[0], coord[1]],
        popup=f"Vị trí kho tối ưu {i+1}",
        icon=folium.Icon(color='black', icon='home', prefix='fa')
    ).add_to(m)

# Lưu bản đồ
m.save("clustering_analysis.html")
print("Đã tạo xong bản đồ phân cụm! Hãy mở file clustering_analysis.html.")