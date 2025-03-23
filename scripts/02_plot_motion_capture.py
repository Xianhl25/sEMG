import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataPlotter:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Data Plotter")
        self.root.geometry("1280x720")

        # 左侧按钮区域
        self.control_frame = tk.Frame(root, width=200)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.load_button = tk.Button(self.control_frame, text="Load CSV", command=self.load_csv)
        self.load_button.pack(pady=10, fill=tk.X)

        self.add_curve_button = tk.Button(self.control_frame, text="Add Curve", command=self.add_curve, state=tk.DISABLED)
        self.add_curve_button.pack(pady=10, fill=tk.X)

        self.remove_curve_button = tk.Button(self.control_frame, text="Remove Curve", command=self.remove_curve, state=tk.DISABLED)
        self.remove_curve_button.pack(pady=10, fill=tk.X)

        # 曲线类别选择器
        self.category_label = tk.Label(self.control_frame, text="Filter Category:")
        self.category_label.pack(pady=5)

        self.category_selector = ttk.Combobox(self.control_frame, values=["All", "Power", "Moment", "Angle", "EMG", "GRF"])
        self.category_selector.pack(pady=5, fill=tk.X)
        self.category_selector.current(0)  # 默认选中 "All"
        self.category_selector.bind("<<ComboboxSelected>>", self.update_plot_visibility)

        # 右侧绘图区域
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.ax.set_xlabel("Time(s)")
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.data = None
        self.headers = None
        self.x_data = None
        self.lines = {}  # 存储曲线 {列名: (曲线对象, 可见性)}

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        df = pd.read_csv(file_path, header=[0, 1])
        df.columns = [f"{col[0]}-{col[1]}" if col[0] and col[1] else col[0] for col in df.columns]
        self.data = df.iloc[1:].astype(float)
        self.headers = df.columns
        self.x_data = self.data.iloc[:, 0]

        self.add_curve_button["state"] = tk.NORMAL
        print("✅ CSV loaded successfully.")

    def add_curve(self):
        choice = self.ask_choice("Select Data Type", ["Motion Capture", "EMG", "GRF"])
        if not choice:
            return

        if choice == "EMG":
            num = self.ask_choice("Select EMG Number", ["1", "2", "3", "4", "6", "7", "9", "10", "11"])
            if not num:
                return
            column_name = f"EMG{num}"
            matching_cols = [col for col in self.headers if col.startswith(column_name)]
        else:
            side = self.ask_choice("Select Side", ["Left", "Right"] if choice == "Motion Capture" else ["LT", "RT"])
            if not side:
                return

            if choice == "Motion Capture":
                joint = self.ask_choice("Select Joint", ["Hip", "Knee", "Ankle"])
                if not joint:
                    return
                measure = self.ask_choice("Select Measure", ["Angle", "Moment", "Power"])
                if not measure:
                    return
                main_category = f"{side} {joint} {measure}"
            else:
                main_category = f"{side}_GRF"

            matching_cols = [col for col in self.headers if col.startswith(main_category)]
            if matching_cols:
                axis = self.ask_choice("Select Axis", ["X", "Y", "Z"])
                if not axis:
                    return
                matching_cols = [col for col in matching_cols if col.endswith(axis)]

        if not matching_cols:
            print("⚠️ No matching columns found.")
            return

        column_name = self.ask_choice("Confirm Column", matching_cols)
        if not column_name:
            return

        line, = self.ax.plot(self.x_data, self.data[column_name], label=column_name)
        self.lines[column_name] = (line, True)  # 记录曲线，默认可见
        self.ax.legend()
        self.update_plot_visibility()  # 确保新添加的曲线符合筛选
        self.update_y_axis()  # 更新Y轴范围和单位

        # 启用 Remove Curve 按钮
        self.remove_curve_button["state"] = tk.NORMAL

    def remove_curve(self):
        if not self.lines:
            return

        column_name = self.ask_choice("Select Curve to Remove", list(self.lines.keys()))
        if not column_name:
            return

        line, _ = self.lines.pop(column_name)
        line.remove()
        self.ax.legend()
        self.update_plot_visibility()  # 更新曲线可见性
        self.update_y_axis()  # 更新Y轴范围和单位

        # 如果没有曲线了，禁用 Remove Curve 按钮
        if not self.lines:
            self.remove_curve_button["state"] = tk.DISABLED

    def update_plot_visibility(self, event=None):
        """更新曲线的可见性"""
        selected_category = self.category_selector.get()

        for column_name, (line, _) in self.lines.items():
            category = self.get_category(column_name)
            if selected_category == "All" or category == selected_category:
                line.set_visible(True)
            else:
                line.set_visible(False)

        self.ax.legend()
        self.canvas.draw()
        self.update_y_axis()  # 更新Y轴范围和单位

    def update_y_axis(self):
        """更新Y轴范围和单位"""
        selected_category = self.category_selector.get()
        visible_lines = [line for column_name, (line, _) in self.lines.items() if line.get_visible()]

        if visible_lines:
            # 获取所有可见曲线的Y值范围
            y_min = min([line.get_ydata().min() for line in visible_lines])
            y_max = max([line.get_ydata().max() for line in visible_lines])
            self.ax.set_ylim(y_min, y_max)

            # 根据类别设置Y轴单位
            if selected_category == "Power":
                self.ax.set_ylabel("Power/W")
            elif selected_category == "Moment":
                self.ax.set_ylabel("Moment/Nm")
            elif selected_category == "Angle":
                self.ax.set_ylabel("Angle/°")
            elif selected_category == "GRF":
                self.ax.set_ylabel("GRF/N")
            elif selected_category == "EMG":
                self.ax.set_ylabel("EMG/XX")
            else:
                self.ax.set_ylabel("")
        else:
            # 如果没有可见曲线，重置Y轴
            self.ax.set_ylim(0, 1)
            self.ax.set_ylabel("")

        self.canvas.draw()

    def get_category(self, column_name):
        """根据列名解析类别"""
        if "Power" in column_name:
            return "Power"
        elif "Moment" in column_name:
            return "Moment"
        elif "Angle" in column_name:
            return "Angle"
        elif "EMG" in column_name:
            return "EMG"
        elif "GRF" in column_name:
            return "GRF"
        return "Other"

    def ask_choice(self, title, options):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("300x200")
        choice_var = tk.StringVar()
        choice_var.set("")

        for option in options:
            btn = tk.Button(dialog, text=option, command=lambda opt=option: self.set_choice(choice_var, opt, dialog))
            btn.pack(pady=5, fill=tk.X)

        dialog.wait_window()
        return choice_var.get()

    def set_choice(self, choice_var, value, dialog):
        choice_var.set(value)
        dialog.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DataPlotter(root)
    root.mainloop()