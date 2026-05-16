import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import messagebox

# ==========================================
# 1. KHỞI TẠO HỆ THỐNG MỜ CHO BÀI 2.13 (MẶT HÀNG ĐẶC BIỆT)
# ==========================================

# --- Biến đầu vào (Antecedents) ---
# Nhu cầu sản phẩm (0 - 100%)
p_demand = ctrl.Antecedent(np.arange(0, 101, 1), 'p_demand')
# Áp lực định giá của đối thủ cạnh tranh (0 - 100%)
comp_pressure = ctrl.Antecedent(np.arange(0, 101, 1), 'comp_pressure')
# Uy tín cửa hàng (0.0 - 5.0 sao)
reputation = ctrl.Antecedent(np.arange(0.0, 5.1, 0.1), 'reputation')
# Biên lợi nhuận (0 - 100%)
margin = ctrl.Antecedent(np.arange(0, 101, 1), 'margin')
# Nhu cầu theo mùa (Thang 0 - 10)
season = ctrl.Antecedent(np.arange(0, 11, 1), 'season')

# --- Biến đầu ra (Consequents) ---
# Mức giảm giá/Chiết khấu (%) - Dải từ 0 đến 70%
discount = ctrl.Consequent(np.arange(0, 71, 1), 'discount')

# --- Xây dựng các hàm liên thuộc (Membership Functions) ---

# Nhu cầu sản phẩm: Thấp, Trung bình, Cao
p_demand['thap'] = fuzz.trimf(p_demand.universe, [0, 0, 40])
p_demand['trung_binh'] = fuzz.trimf(p_demand.universe, [20, 50, 80])
p_demand['cao'] = fuzz.trimf(p_demand.universe, [60, 100, 100])

# Áp lực đối thủ: Thấp, Trung bình, Cao
comp_pressure['thap'] = fuzz.trimf(comp_pressure.universe, [0, 0, 40])
comp_pressure['trung_binh'] = fuzz.trimf(comp_pressure.universe, [20, 50, 80])
comp_pressure['cao'] = fuzz.trimf(comp_pressure.universe, [60, 100, 100])

# Uy tín cửa hàng: Thấp (<4.0), Trung bình (4.0 - 4.5), Cao (>4.5)
reputation['thap'] = fuzz.trimf(reputation.universe, [0, 0, 4.0])
reputation['trung_binh'] = fuzz.trimf(reputation.universe, [3.8, 4.25, 4.7])
reputation['cao'] = fuzz.trimf(reputation.universe, [4.5, 5.0, 5.0])

# Biên lợi nhuận: Thấp, Trung bình, Cao
margin['thap'] = fuzz.trimf(margin.universe, [0, 0, 30])
margin['trung_binh'] = fuzz.trimf(margin.universe, [20, 50, 80])
margin['cao'] = fuzz.trimf(margin.universe, [60, 100, 100])

# Nhu cầu theo mùa: Không có, Trung bình, Cao
season['khong_co'] = fuzz.trimf(season.universe, [0, 0, 3])
season['trung_binh'] = fuzz.trimf(season.universe, [2, 5, 8])
season['cao'] = fuzz.trimf(season.universe, [7, 10, 10])

# Mức giảm giá: Rất thấp (0-5%), Thấp (5-10%), Trung bình (10-20%), Cao (20-40%), Rất cao (40-70%)
discount['rat_thap'] = fuzz.trimf(discount.universe, [0, 0, 5])
discount['thap'] = fuzz.trimf(discount.universe, [2, 7.5, 12])
discount['trung_binh'] = fuzz.trimf(discount.universe, [10, 15, 25])
discount['cao'] = fuzz.trimf(discount.universe, [20, 30, 45])
discount['rat_cao'] = fuzz.trimf(discount.universe, [40, 70, 70])

# --- 7 Luật Mờ (Fuzzy Rules) từ sách Bài 2.13 ---
rule1 = ctrl.Rule(p_demand['cao'] & comp_pressure['thap'] & margin['thap'], discount['rat_thap'])
rule2 = ctrl.Rule(p_demand['thap'] & comp_pressure['cao'] & margin['cao'], discount['cao'])
rule3 = ctrl.Rule(reputation['cao'] & margin['trung_binh'] & season['cao'], discount['trung_binh'])
rule4 = ctrl.Rule(comp_pressure['cao'] & season['cao'] & margin['cao'], discount['rat_cao'])
rule5 = ctrl.Rule(reputation['thap'] & p_demand['trung_binh'] & margin['thap'], discount['trung_binh'])
rule6 = ctrl.Rule(p_demand['cao'] & season['khong_co'] & comp_pressure['thap'], discount['rat_thap'])
rule7 = ctrl.Rule(margin['cao'] & comp_pressure['trung_binh'] & season['trung_binh'], discount['trung_binh'])

# Lưu ý: Tình huống trong sách (Đồng hồ xa xỉ) có: Biên lợi nhuận=Cao, Mùa=Cao, Áp lực ĐT=TB.
# Sách kết luận giảm giá là "Trung bình". Để hệ thống chạy ra đúng như sách, giáo sư bổ sung thêm 1 luật phụ khớp với mô tả văn bản của sách:
rule8 = ctrl.Rule(margin['cao'] & season['cao'] & comp_pressure['trung_binh'], discount['trung_binh'])

# Khởi tạo mô phỏng
luxury_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8])
luxury_sim = ctrl.ControlSystemSimulation(luxury_ctrl)


# ==========================================
# 2. XÂY DỰNG GIAO DIỆN NGƯỜI DÙNG (GUI)
# ==========================================

def calculate_discount():
    try:
        luxury_sim.input['p_demand'] = p_demand_scale.get()
        luxury_sim.input['comp_pressure'] = comp_scale.get()
        luxury_sim.input['reputation'] = rep_scale.get()
        luxury_sim.input['margin'] = margin_scale.get()
        luxury_sim.input['season'] = season_scale.get()

        luxury_sim.compute()

        result = luxury_sim.output['discount']
        lbl_result.config(text=f"Chiết Khấu Đề Xuất: {result:.2f} %")
        
    except Exception as e:
        messagebox.showwarning("Lỗi Suy Diễn", "Các thông số chưa kích hoạt luật mờ nào. Hãy thử điều chỉnh lại!")

def load_luxury_watch_case():
    # Tình huống: Đồng hồ xa xỉ thủ công
    p_demand_scale.set(85)   # Nhu cầu: Cao
    comp_scale.set(50)       # Áp lực đối thủ: Trung bình
    rep_scale.set(4.2)       # Uy tín: Trung bình (4.2 sao)
    margin_scale.set(85)     # Biên lợi nhuận: Cao
    season_scale.set(9)      # Nhu cầu theo mùa: Cao (Shopee 11.11)
    calculate_discount()

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Bài 2.13: Định giá mặt hàng đặc biệt")
root.geometry("520x600")
root.configure(padx=20, pady=20)

tk.Label(root, text="MÔ PHỎNG CHIẾT KHẤU MẶT HÀNG NGÁCH", font=("Arial", 13, "bold"), fg="#1E3A8A").pack(pady=10)

frame_inputs = tk.Frame(root)
frame_inputs.pack(fill="both", expand=True)

def create_slider(parent, label_text, from_, to_, resolution, default_val):
    frame = tk.Frame(parent)
    frame.pack(fill="x", pady=5)
    tk.Label(frame, text=label_text, width=32, anchor="w", font=("Arial", 10)).pack(side="left")
    scale = tk.Scale(frame, from_=from_, to=to_, orient="horizontal", resolution=resolution, length=200)
    scale.set(default_val)
    scale.pack(side="right")
    return scale

p_demand_scale = create_slider(frame_inputs, "Nhu cầu sản phẩm (%):", 0, 100, 1, 50)
comp_scale = create_slider(frame_inputs, "Áp lực định giá đối thủ (%):", 0, 100, 1, 50)
rep_scale = create_slider(frame_inputs, "Uy tín cửa hàng (Sao):", 0.0, 5.0, 0.1, 4.2)
margin_scale = create_slider(frame_inputs, "Biên lợi nhuận (%):", 0, 100, 1, 50)
season_scale = create_slider(frame_inputs, "Nhu cầu theo mùa (0=Không, 10=Lớn):", 0, 10, 1, 5)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=20)

btn_test = tk.Button(frame_buttons, text="Chạy TH: Đồng hồ xa xỉ", font=("Arial", 10, "bold"), bg="#FCD34D", command=load_luxury_watch_case)
btn_test.pack(side="left", padx=10)

btn_calc = tk.Button(frame_buttons, text="TÍNH TOÁN", font=("Arial", 10, "bold"), bg="#2563EB", fg="white", command=calculate_discount)
btn_calc.pack(side="left", padx=10)

frame_results = tk.LabelFrame(root, text="Kết Quả Phân Tích", font=("Arial", 11, "bold"), padx=10, pady=20)
frame_results.pack(fill="x")

lbl_result = tk.Label(frame_results, text="Chiết Khấu Đề Xuất: -- %", font=("Arial", 14, "bold"), fg="#2563EB")
lbl_result.pack()

root.mainloop()