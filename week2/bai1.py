import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================
# 1. KHỞI TẠO HỆ THỐNG MỜ (Giữ nguyên như cũ)
# ==========================================
# Biến đầu vào
distance = ctrl.Antecedent(np.arange(0, 51, 1), 'distance')
traffic = ctrl.Antecedent(np.arange(0, 101, 1), 'traffic')
demand = ctrl.Antecedent(np.arange(0, 101, 1), 'demand')
weather = ctrl.Antecedent(np.arange(0, 11, 0.1), 'weather')
rating = ctrl.Antecedent(np.arange(1.0, 5.1, 0.1), 'rating')
punctuality = ctrl.Antecedent(np.arange(0, 101, 1), 'punctuality')

# Biến đầu ra
price = ctrl.Consequent(np.arange(0, 101, 1), 'price')
points = ctrl.Consequent(np.arange(0, 101, 1), 'points')

# Hàm liên thuộc (Membership Functions)
distance['ngan'] = fuzz.trimf(distance.universe, [0, 0, 3])
distance['trung_binh'] = fuzz.trimf(distance.universe, [2, 5, 8])
distance['xa'] = fuzz.trimf(distance.universe, [6, 13, 20])
distance['rat_xa'] = fuzz.trimf(distance.universe, [15, 50, 50])

traffic['thap'] = fuzz.trimf(traffic.universe, [0, 0, 30])
traffic['trung_binh'] = fuzz.trimf(traffic.universe, [20, 45, 70])
traffic['cao'] = fuzz.trimf(traffic.universe, [60, 100, 100])

demand['thap'] = fuzz.trimf(demand.universe, [0, 0, 30])
demand['trung_binh'] = fuzz.trimf(demand.universe, [20, 45, 70])
demand['cao'] = fuzz.trimf(demand.universe, [60, 100, 100])

weather['tot'] = fuzz.trimf(weather.universe, [0, 0, 4])
weather['vua_phai'] = fuzz.trimf(weather.universe, [3, 5, 7])
weather['xau'] = fuzz.trimf(weather.universe, [6, 10, 10])

rating['kem'] = fuzz.trimf(rating.universe, [1.0, 1.0, 2.5])
rating['trung_binh'] = fuzz.trimf(rating.universe, [2.0, 3.0, 4.0])
rating['tot'] = fuzz.trimf(rating.universe, [3.5, 5.0, 5.0])

punctuality['tre'] = fuzz.trimf(punctuality.universe, [0, 0, 50])
punctuality['dung_gio'] = fuzz.trimf(punctuality.universe, [40, 60, 80])
punctuality['som'] = fuzz.trimf(punctuality.universe, [70, 100, 100])

price['thap'] = fuzz.trimf(price.universe, [0, 0, 30])
price['trung_binh'] = fuzz.trimf(price.universe, [20, 50, 80])
price['cao'] = fuzz.trimf(price.universe, [60, 80, 100])
price['rat_cao'] = fuzz.trimf(price.universe, [80, 100, 100])

points['khong_co'] = fuzz.trimf(points.universe, [0, 0, 10])
points['it'] = fuzz.trimf(points.universe, [5, 25, 45])
points['trung_binh'] = fuzz.trimf(points.universe, [30, 50, 70])
points['cao'] = fuzz.trimf(points.universe, [60, 100, 100])

# 20 Luật Mờ
rule1 = ctrl.Rule(distance['ngan'] & traffic['thap'] & demand['thap'], price['thap'])
rule2 = ctrl.Rule(distance['ngan'] & traffic['trung_binh'] & demand['cao'], price['trung_binh'])
rule3 = ctrl.Rule(distance['trung_binh'] & traffic['cao'] & demand['cao'], price['cao'])
rule4 = ctrl.Rule(distance['xa'] & traffic['trung_binh'] & weather['tot'], price['trung_binh'])
rule5 = ctrl.Rule(distance['xa'] & traffic['cao'] & weather['xau'], price['rat_cao'])
rule6 = ctrl.Rule(distance['rat_xa'] & traffic['cao'] & demand['cao'], price['rat_cao'])
rule7 = ctrl.Rule(distance['trung_binh'] & traffic['thap'] & demand['thap'], price['trung_binh'])
rule8 = ctrl.Rule(distance['ngan'] & traffic['cao'] & weather['xau'], price['cao'])
rule9 = ctrl.Rule(distance['rat_xa'] & weather['xau'], price['rat_cao'])
rule10 = ctrl.Rule(distance['trung_binh'] & traffic['trung_binh'] & weather['vua_phai'], price['trung_binh'])
rule11 = ctrl.Rule(rating['tot'] & punctuality['som'], points['cao'])
rule12 = ctrl.Rule(rating['trung_binh'] & punctuality['dung_gio'], points['trung_binh'])
rule13 = ctrl.Rule(rating['kem'] & punctuality['tre'], points['khong_co'])
rule14 = ctrl.Rule(distance['xa'] & traffic['cao'] & punctuality['dung_gio'], points['cao'])
rule15 = ctrl.Rule(distance['trung_binh'] & traffic['trung_binh'] & rating['tot'], points['trung_binh'])
rule16 = ctrl.Rule(rating['kem'] & punctuality['tre'], points['khong_co'])
rule17 = ctrl.Rule(distance['rat_xa'] & weather['xau'] & rating['tot'], points['cao'])
rule18 = ctrl.Rule(distance['ngan'] & rating['trung_binh'] & punctuality['dung_gio'], points['it'])
rule19 = ctrl.Rule(distance['xa'] & traffic['cao'] & punctuality['tre'], points['it'])
rule20 = ctrl.Rule(distance['trung_binh'] & weather['vua_phai'] & rating['tot'], points['trung_binh'])

# Khởi tạo mô phỏng
grab_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10,
                                rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20])
grab_simulation = ctrl.ControlSystemSimulation(grab_ctrl)


# ==========================================
# 2. XÂY DỰNG GIAO DIỆN NGƯỜI DÙNG (GUI)
# ==========================================

def calculate_fuzzy():
    try:
        # Lấy giá trị từ các thanh trượt
        grab_simulation.input['distance'] = distance_scale.get()
        grab_simulation.input['traffic'] = traffic_scale.get()
        grab_simulation.input['demand'] = demand_scale.get()
        grab_simulation.input['weather'] = weather_scale.get()
        grab_simulation.input['rating'] = rating_scale.get()
        grab_simulation.input['punctuality'] = punctuality_scale.get()

        # Tính toán
        grab_simulation.compute()

        # Hiển thị kết quả lên màn hình
        lbl_result_price.config(text=f"Mức Giá Đi Xe: {grab_simulation.output['price']:.2f} %")
        lbl_result_points.config(text=f"Điểm Thưởng: {grab_simulation.output['points']:.2f} điểm")
        
    except Exception as e:
        messagebox.showwarning("Cảnh báo", "Các thông số nhập vào không kích hoạt bất kỳ luật mờ nào. Hãy thử điều chỉnh lại!")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Hệ Thống Logic Mờ: Grab-Bike Giá & Điểm Thưởng")
root.geometry("450x650")
root.configure(padx=20, pady=20)

# Tiêu đề
tk.Label(root, text="HỆ THỐNG MÔ PHỎNG GRAB-BIKE", font=("Arial", 14, "bold")).pack(pady=10)

# Tạo khung chứa các thanh trượt (sliders)
frame_inputs = tk.Frame(root)
frame_inputs.pack(fill="both", expand=True)

def create_slider(parent, label_text, from_, to_, resolution, default_val):
    frame = tk.Frame(parent)
    frame.pack(fill="x", pady=5)
    tk.Label(frame, text=label_text, width=25, anchor="w", font=("Arial", 10)).pack(side="left")
    scale = tk.Scale(frame, from_=from_, to=to_, orient="horizontal", resolution=resolution, length=200)
    scale.set(default_val)
    scale.pack(side="right")
    return scale

# Khởi tạo các thanh trượt
distance_scale = create_slider(frame_inputs, "Khoảng cách (km):", 0, 50, 1, 5)
traffic_scale = create_slider(frame_inputs, "Tình trạng giao thông (%):", 0, 100, 1, 50)
demand_scale = create_slider(frame_inputs, "Mức cầu/Nhu cầu (%):", 0, 100, 1, 50)
weather_scale = create_slider(frame_inputs, "Thời tiết (0=Tốt, 10=Bão):", 0, 10, 0.1, 2)
rating_scale = create_slider(frame_inputs, "Đánh giá tài xế (Sao):", 1.0, 5.0, 0.1, 4.5)
punctuality_scale = create_slider(frame_inputs, "Đúng giờ (%):", 0, 100, 1, 80)

# Nút tính toán
btn_calc = tk.Button(root, text="TÍNH TOÁN & GIẢI MỜ", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=calculate_fuzzy)
btn_calc.pack(pady=20)

# Khung hiển thị kết quả
frame_results = tk.LabelFrame(root, text="Kết Quả Đầu Ra", font=("Arial", 11, "bold"), padx=10, pady=10)
frame_results.pack(fill="x")

lbl_result_price = tk.Label(frame_results, text="Mức Giá Đi Xe: -- %", font=("Arial", 12), fg="blue")
lbl_result_price.pack(pady=5)

lbl_result_points = tk.Label(frame_results, text="Điểm Thưởng: -- điểm", font=("Arial", 12), fg="red")
lbl_result_points.pack(pady=5)

# Chạy vòng lặp giao diện
root.mainloop()