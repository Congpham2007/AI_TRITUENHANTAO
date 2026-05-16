import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import messagebox

# ==========================================
# 1. KHỞI TẠO HỆ THỐNG MỜ CHO BÀI 2.14 (LOGISTICS)
# ==========================================

# --- Biến đầu vào (Antecedents) --- Thang điểm 0 - 100%
density = ctrl.Antecedent(np.arange(0, 101, 1), 'density')           # Mật độ đơn hàng
urgency = ctrl.Antecedent(np.arange(0, 101, 1), 'urgency')           # Mức độ khẩn cấp
load = ctrl.Antecedent(np.arange(0, 101, 1), 'load')                 # Tải trọng hiện tại
traffic = ctrl.Antecedent(np.arange(0, 101, 1), 'traffic')           # Tình trạng giao thông
profit = ctrl.Antecedent(np.arange(0, 101, 1), 'profit')             # Lợi nhuận mỗi lần giao

# --- Biến đầu ra (Consequents) ---
# Số lượng đơn hàng kết hợp (Từ 0 đến 10 đơn)
combine = ctrl.Consequent(np.arange(0, 11, 1), 'combine')
# Ưu tiên giao hàng (0 - 100%)
priority = ctrl.Consequent(np.arange(0, 101, 1), 'priority')

# --- Xây dựng các hàm liên thuộc (Membership Functions) ---

# Các biến đầu vào đều có 3 mức: Thấp, Trung bình, Cao
for var in [density, urgency, load, traffic, profit]:
    var['thap'] = fuzz.trimf(var.universe, [0, 0, 40])
    var['trung_binh'] = fuzz.trimf(var.universe, [20, 50, 80])
    var['cao'] = fuzz.trimf(var.universe, [60, 100, 100])

# Biến đầu ra 1: Số lượng kết hợp (Ít, Một số/Một vài, Nhiều)
combine['it'] = fuzz.trimf(combine.universe, [0, 0, 3])
combine['mot_so'] = fuzz.trimf(combine.universe, [2, 5, 8])
combine['nhieu'] = fuzz.trimf(combine.universe, [6, 10, 10])

# Biến đầu ra 2: Ưu tiên giao hàng (Thấp, Trung bình, Cao)
priority['thap'] = fuzz.trimf(priority.universe, [0, 0, 40])
priority['trung_binh'] = fuzz.trimf(priority.universe, [20, 50, 80])
priority['cao'] = fuzz.trimf(priority.universe, [60, 100, 100])


# --- 8 Luật Mờ (Fuzzy Rules) từ sách Bài 2.14 ---

# Nhóm luật: Kết hợp đơn hàng
rule1 = ctrl.Rule(density['cao'] & load['thap'] & traffic['thap'], combine['nhieu'])
rule2 = ctrl.Rule(density['trung_binh'] & traffic['cao'] & urgency['trung_binh'], combine['mot_so']) # Một vài = Một số
rule3 = ctrl.Rule(load['cao'] & density['cao'] & profit['trung_binh'], combine['mot_so'])
rule4 = ctrl.Rule(density['thap'] & urgency['cao'] & traffic['trung_binh'], combine['mot_so'])
rule5 = ctrl.Rule(profit['cao'] & urgency['cao'] & traffic['cao'], combine['mot_so'])

# Nhóm luật: Ưu tiên giao hàng
rule6 = ctrl.Rule(urgency['cao'] & profit['cao'], priority['cao'])
rule7 = ctrl.Rule(urgency['trung_binh'] & traffic['trung_binh'], priority['trung_binh'])
rule8 = ctrl.Rule(urgency['thap'] & density['cao'] & profit['thap'], priority['thap'])

# --- Bổ sung luật cho Tình huống ví dụ trong sách ---
# Tình huống: Mật độ Cao, Khẩn cấp TB, Tải trọng Thấp, Giao thông TB, Lợi nhuận TB
# Sách kết luận: Kết hợp nhiều đơn hàng VÀ Ưu tiên trung bình (Khoảng 5 lần giao).
# Vì các luật 1-8 bên trên không phủ kín trường hợp này (Luật 1 yêu cầu Giao thông Thấp, nhưng tình huống là TB),
# Giáo sư thêm 2 luật phụ để logic toán học khớp với suy luận văn bản của tác giả:
rule9_hidden = ctrl.Rule(density['cao'] & load['thap'] & traffic['trung_binh'], combine['nhieu'])
rule10_hidden = ctrl.Rule(urgency['trung_binh'], priority['trung_binh'])

# Khởi tạo mô phỏng
logistics_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9_hidden, rule10_hidden])
logistics_sim = ctrl.ControlSystemSimulation(logistics_ctrl)


# ==========================================
# 2. XÂY DỰNG GIAO DIỆN NGƯỜI DÙNG (GUI)
# ==========================================

def calculate_logistics():
    try:
        logistics_sim.input['density'] = density_scale.get()
        logistics_sim.input['urgency'] = urgency_scale.get()
        logistics_sim.input['load'] = load_scale.get()
        logistics_sim.input['traffic'] = traffic_scale.get()
        logistics_sim.input['profit'] = profit_scale.get()

        logistics_sim.compute()

        res_combine = logistics_sim.output['combine']
        res_priority = logistics_sim.output['priority']
        
        lbl_res_combine.config(text=f"Số đơn hàng kết hợp: ~ {int(round(res_combine))} đơn (Mức {res_combine:.1f}/10)")
        lbl_res_priority.config(text=f"Mức độ ưu tiên: {res_priority:.1f} %")
        
    except Exception as e:
        messagebox.showwarning("Lỗi Suy Diễn", "Các thông số chưa kích hoạt luật mờ nào. Hãy thử điều chỉnh lại!")

def load_book_test_case():
    # Load tình huống ví dụ ở trang 93
    density_scale.set(85)   # Mật độ: Cao
    urgency_scale.set(50)   # Khẩn cấp: Trung bình
    load_scale.set(15)      # Tải trọng: Thấp
    traffic_scale.set(50)   # Giao thông: Trung bình (30km/h)
    profit_scale.set(50)    # Lợi nhuận: Trung bình
    calculate_logistics()

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Bài 2.14: Tối ưu hóa Giao Nhận Logistics")
root.geometry("550x650")
root.configure(padx=20, pady=20)

tk.Label(root, text="MÔ PHỎNG LOGISTICS & GIAO HÀNG", font=("Arial", 14, "bold"), fg="#047857").pack(pady=10)

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

density_scale = create_slider(frame_inputs, "Mật độ đơn hàng (%):", 0, 100, 1, 50)
urgency_scale = create_slider(frame_inputs, "Mức độ khẩn cấp (%):", 0, 100, 1, 50)
load_scale = create_slider(frame_inputs, "Tải trọng hiện tại của tài xế (%):", 0, 100, 1, 50)
traffic_scale = create_slider(frame_inputs, "Tình trạng giao thông (Tắc nghẽn %):", 0, 100, 1, 50)
profit_scale = create_slider(frame_inputs, "Lợi nhuận mỗi lần giao (%):", 0, 100, 1, 50)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=20)

btn_test = tk.Button(frame_buttons, text="Chạy Tình Huống Tr.93", font=("Arial", 10, "bold"), bg="#10B981", fg="white", command=load_book_test_case)
btn_test.pack(side="left", padx=10)

btn_calc = tk.Button(frame_buttons, text="TỐI ƯU HÓA", font=("Arial", 10, "bold"), bg="#047857", fg="white", command=calculate_logistics)
btn_calc.pack(side="left", padx=10)

frame_results = tk.LabelFrame(root, text="Kế Hoạch Tuyến Đường", font=("Arial", 11, "bold"), padx=10, pady=20)
frame_results.pack(fill="x")

lbl_res_combine = tk.Label(frame_results, text="Số đơn hàng kết hợp: --", font=("Arial", 13, "bold"), fg="#D97706")
lbl_res_combine.pack(pady=5)

lbl_res_priority = tk.Label(frame_results, text="Mức độ ưu tiên: -- %", font=("Arial", 13, "bold"), fg="#DC2626")
lbl_res_priority.pack(pady=5)

root.mainloop()