import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import messagebox

# ==========================================
# 1. KHỞI TẠO HỆ THỐNG MỜ CHO BÀI 2.12 (SHOPEE)
# ==========================================

# --- Biến đầu vào (Antecedents) ---
# Đánh giá cửa hàng (0.0 - 5.0 sao)
rating = ctrl.Antecedent(np.arange(0.0, 5.1, 0.1), 'rating')
# Khối lượng bán hàng (Quy đổi thang 0 - 100%)
sales = ctrl.Antecedent(np.arange(0, 101, 1), 'sales')
# Biên lợi nhuận (0 - 100%)
margin = ctrl.Antecedent(np.arange(0, 101, 1), 'margin')
# Sự kiện theo mùa (Thang điểm mức độ 0 - 10)
season = ctrl.Antecedent(np.arange(0, 11, 1), 'season')
# Giảm giá của đối thủ cạnh tranh (0 - 100%)
competitor = ctrl.Antecedent(np.arange(0, 101, 1), 'competitor')

# --- Biến đầu ra (Consequents) ---
# Tỷ lệ chiết khấu (%) - Dải từ 0 đến 70% theo đề bài
discount = ctrl.Consequent(np.arange(0, 71, 1), 'discount')

# --- Xây dựng các hàm liên thuộc (Membership Functions) ---

# Đánh giá: Thấp (Dưới 4.0), Trung bình (4.0 - 4.5), Cao (Trên 4.5)
rating['thap'] = fuzz.trimf(rating.universe, [0, 0, 4.0])
rating['trung_binh'] = fuzz.trimf(rating.universe, [3.8, 4.25, 4.7])
rating['cao'] = fuzz.trimf(rating.universe, [4.5, 5.0, 5.0])

# Khối lượng bán hàng: Thấp, Trung bình, Cao
sales['thap'] = fuzz.trimf(sales.universe, [0, 0, 40])
sales['trung_binh'] = fuzz.trimf(sales.universe, [20, 50, 80])
sales['cao'] = fuzz.trimf(sales.universe, [60, 100, 100])

# Biên lợi nhuận: Thấp, Trung bình, Cao
margin['thap'] = fuzz.trimf(margin.universe, [0, 0, 30])
margin['trung_binh'] = fuzz.trimf(margin.universe, [20, 50, 80])
margin['cao'] = fuzz.trimf(margin.universe, [60, 100, 100])

# Sự kiện theo mùa: Không có, Trung bình, Cao
season['khong_co'] = fuzz.trimf(season.universe, [0, 0, 3])
season['trung_binh'] = fuzz.trimf(season.universe, [2, 5, 8])
season['cao'] = fuzz.trimf(season.universe, [7, 10, 10])

# Giảm giá của đối thủ: Thấp, Trung bình, Cao
competitor['thap'] = fuzz.trimf(competitor.universe, [0, 0, 30])
competitor['trung_binh'] = fuzz.trimf(competitor.universe, [20, 50, 80])
competitor['cao'] = fuzz.trimf(competitor.universe, [60, 100, 100])

# Tỷ lệ chiết khấu: Rất thấp (0-5%), Thấp (5-10%), Trung bình (10-20%), Cao (20-40%), Rất cao (40-70%)
discount['rat_thap'] = fuzz.trimf(discount.universe, [0, 0, 5])
discount['thap'] = fuzz.trimf(discount.universe, [2, 7.5, 12])
discount['trung_binh'] = fuzz.trimf(discount.universe, [10, 15, 25])
discount['cao'] = fuzz.trimf(discount.universe, [20, 30, 45])
discount['rat_cao'] = fuzz.trimf(discount.universe, [40, 70, 70])


# --- 7 Luật Mờ (Fuzzy Rules) từ sách ---
rule1 = ctrl.Rule(rating['cao'] & sales['cao'] & margin['cao'], discount['rat_thap'])
rule2 = ctrl.Rule(rating['thap'] & sales['thap'] & margin['cao'], discount['cao'])
rule3 = ctrl.Rule(season['cao'] & competitor['cao'], discount['rat_cao'])
rule4 = ctrl.Rule(rating['trung_binh'] & sales['trung_binh'] & margin['trung_binh'], discount['trung_binh'])
rule5 = ctrl.Rule(competitor['thap'] & margin['thap'] & sales['cao'], discount['rat_thap'])
rule6 = ctrl.Rule(rating['thap'] & season['khong_co'], discount['trung_binh'])
rule7 = ctrl.Rule(sales['thap'] & margin['thap'], discount['rat_cao'])

# Khởi tạo mô phỏng
shopee_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
shopee_sim = ctrl.ControlSystemSimulation(shopee_ctrl)


# ==========================================
# 2. XÂY DỰNG GIAO DIỆN NGƯỜI DÙNG (GUI)
# ==========================================

def calculate_discount():
    try:
        # Lấy dữ liệu từ giao diện
        shopee_sim.input['rating'] = rating_scale.get()
        shopee_sim.input['sales'] = sales_scale.get()
        shopee_sim.input['margin'] = margin_scale.get()
        shopee_sim.input['season'] = season_scale.get()
        shopee_sim.input['competitor'] = comp_scale.get()

        # Tính toán
        shopee_sim.compute()

        # Hiển thị
        result = shopee_sim.output['discount']
        lbl_result.config(text=f"Chiết Khấu Đề Xuất: {result:.2f} %")
        
    except Exception as e:
        messagebox.showwarning("Lỗi Suy Diễn", "Các điều kiện hiện tại không thỏa mãn bất kỳ luật mờ nào (Chưa đủ luật để bao phủ mọi trường hợp). Hãy chỉnh lại thanh trượt!")

def load_test_case():
    # Load tình huống ví dụ trong sách:
    # Xếp hạng = 4.3, Khối lượng = TB, Biên lợi nhuận = Thấp, Sự kiện = Cao, Đối thủ = Cao
    rating_scale.set(4.3)
    sales_scale.set(50)   # 50% = Trung bình
    margin_scale.set(15)  # 15% = Thấp
    season_scale.set(9)   # 9 = Cao
    comp_scale.set(85)    # 85% = Cao
    calculate_discount()

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Shopee - Hệ Thống Logic Mờ Chiết Khấu")
root.geometry("500x600")
root.configure(padx=20, pady=20)

tk.Label(root, text="MÔ PHỎNG CHIẾT KHẤU SHOPEE", font=("Arial", 14, "bold"), fg="#EE4D2D").pack(pady=10)

frame_inputs = tk.Frame(root)
frame_inputs.pack(fill="both", expand=True)

def create_slider(parent, label_text, from_, to_, resolution, default_val):
    frame = tk.Frame(parent)
    frame.pack(fill="x", pady=5)
    tk.Label(frame, text=label_text, width=30, anchor="w", font=("Arial", 10)).pack(side="left")
    scale = tk.Scale(frame, from_=from_, to=to_, orient="horizontal", resolution=resolution, length=200)
    scale.set(default_val)
    scale.pack(side="right")
    return scale

# Thanh trượt
rating_scale = create_slider(frame_inputs, "Đánh giá cửa hàng (Sao):", 0.0, 5.0, 0.1, 4.3)
sales_scale = create_slider(frame_inputs, "Khối lượng bán hàng (%):", 0, 100, 1, 50)
margin_scale = create_slider(frame_inputs, "Biên lợi nhuận (%):", 0, 100, 1, 50)
season_scale = create_slider(frame_inputs, "Sự kiện theo mùa (0=Không, 10=Lớn):", 0, 10, 1, 5)
comp_scale = create_slider(frame_inputs, "Giảm giá của đối thủ (%):", 0, 100, 1, 50)

# Nút thao tác
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=15)

btn_test = tk.Button(frame_buttons, text="Chạy Tình Huống Sách", font=("Arial", 10), bg="#FFB534", command=load_test_case)
btn_test.pack(side="left", padx=10)

btn_calc = tk.Button(frame_buttons, text="TÍNH TOÁN CHIẾT KHẤU", font=("Arial", 10, "bold"), bg="#EE4D2D", fg="white", command=calculate_discount)
btn_calc.pack(side="left", padx=10)

# Hiển thị kết quả
frame_results = tk.LabelFrame(root, text="Kết Quả Đầu Ra", font=("Arial", 11, "bold"), padx=10, pady=20)
frame_results.pack(fill="x")

lbl_result = tk.Label(frame_results, text="Chiết Khấu Đề Xuất: -- %", font=("Arial", 14, "bold"), fg="#EE4D2D")
lbl_result.pack()

root.mainloop()