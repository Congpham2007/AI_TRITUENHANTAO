import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from PIL import Image

# 1. Cấu hình trang web
st.set_page_config(page_title="Hệ thống Nhận diện Khuôn mặt", layout="centered")
st.title("🤖 AI Nhận Diện Học Sinh Trong Lớp")
st.write("Vui lòng tải lên một bức ảnh để AI dự đoán.")

# 2. Danh sách lớp (Dictionary đảo ngược: Key là số, Value là Tên)
CLASS_LABELS = {
    0: 'BUI DANG KHOI', 1: 'DANG NGUYEN PHUONG NGHI', 2: 'HA PHUONG THAO', 3: 'HOANG BAO TRAN', 
    4: 'HOANG BUI TRA MY', 5: 'LE HUYNH DUC HUY', 6: 'LE MINH TRIET', 7: 'LE THAI BAO', 
    8: 'LE THI NHU QUYNH', 9: 'LE TRAN QUY ANH', 10: 'LE TRONG DAI', 11: 'MAI HO QUOC TUY', 
    12: 'NGUYEN BAO HAN', 13: 'NGUYEN DONG HAI', 14: 'NGUYEN HOANG BAO', 15: 'NGUYEN HUU TOAN', 
    16: 'NGUYEN KHAC LUU VU', 17: 'NGUYEN NGOC KHANH UYEN', 18: 'NGUYEN NGOC KIM TUYET', 19: 'NGUYEN THI THANH HA', 
    20: 'NGUYEN TRONG MINH', 21: 'NHAN MANH TUAN', 22: 'PHAM DUC THANH CONG', 23: 'PHAM LY BAO LAM', 
    24: 'PHAM MAI PHUONG', 25: 'THAI TUAN PHAT', 26: 'TRAN GIA HAN', 27: 'TRAN MINH HOANG', 
    28: 'TRAN NGOC THAO ANH', 29: 'TRAN THE DANG KHOA', 30: 'TRINH THUY HANG'
}

# 3. Hàm tải mô hình (Dùng cache để không bị load lại mỗi lần đổi ảnh)
@st.cache_resource
def load_face_model():
    # Đảm bảo tên file ở đây khớp với tên file bạn đã tải về
    return load_model('face_model_31_classes.h5')

model = load_face_model()

# 4. Giao diện tải ảnh lên
uploaded_file = st.file_uploader("Chọn một bức ảnh (JPG, PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Hiển thị ảnh vừa tải lên
    image = Image.open(uploaded_file).convert('RGB') 
    st.image(image, caption="Ảnh đã tải lên", use_container_width=True)
    
    # 5. Nút bấm dự đoán
    if st.button("Dự đoán ngay"):
        with st.spinner("AI đang suy nghĩ..."):
            # Tiền xử lý ảnh (giống hệt lúc train)
            img = image.resize((128, 128)) # Ép về 128x128
            img_array = img_to_array(img)
            img_array = img_array / 255.0  # Chuẩn hóa
            img_array = np.expand_dims(img_array, axis=0) # Thêm chiều batch (1, 128, 128, 3)
            
            # Đưa vào mô hình dự đoán
            predictions = model.predict(img_array)
            predicted_class_index = np.argmax(predictions)
            confidence = np.max(predictions) * 100
            
            # Lấy tên từ dictionary
            predicted_name = CLASS_LABELS.get(predicted_class_index, "Không xác định")
            
            # 6. In kết quả ra màn hình
            st.success(f"🎉 Kết quả: **{predicted_name}**")
            st.info(f"Độ tự tin (Confidence): {confidence:.2f}%")