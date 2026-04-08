# Day 30 python Data Analysis project using A.I

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataAnalyzerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("AI Data Analysis Tool")
        self.root.geometry("900x600")

        self.file_path = None
        self.df = None
        self.report_df = None

        self.create_widgets()

    def create_widgets(self):

        # File selection
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(frame, text="Browse File", command=self.browse_file).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Read File", command=self.read_file).grid(row=0, column=1, padx=5)

        self.file_label = tk.Label(self.root, text="No file selected")
        self.file_label.pack()

        # Info display
        self.info_label = tk.Label(self.root, text="")
        self.info_label.pack(pady=5)

        # Dropdowns
        dropdown_frame = tk.Frame(self.root)
        dropdown_frame.pack(pady=10)

        tk.Label(dropdown_frame, text="Group By").grid(row=0, column=0)
        self.group_col = ttk.Combobox(dropdown_frame)
        self.group_col.grid(row=0, column=1)

        tk.Label(dropdown_frame, text="Aggregation").grid(row=0, column=2)
        self.agg_method = ttk.Combobox(dropdown_frame, values=["sum","mean","max","min","count","median"])
        self.agg_method.grid(row=0, column=3)

        tk.Label(dropdown_frame, text="Value Column").grid(row=0, column=4)
        self.value_col = ttk.Combobox(dropdown_frame)
        self.value_col.grid(row=0, column=5)

        tk.Button(self.root, text="Preview Report", command=self.preview_report).pack(pady=5)

        # Treeview for report
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(expand=True, fill='both')

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Export Report", command=self.export_report).grid(row=0, column=0, padx=5)

        # Chart
        tk.Label(btn_frame, text="Chart Type").grid(row=0, column=1)
        self.chart_type = ttk.Combobox(btn_frame, values=["bar", "line", "pie"])
        self.chart_type.grid(row=0, column=2)

        tk.Button(btn_frame, text="Preview Chart", command=self.preview_chart).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Export Chart", command=self.export_chart).grid(row=0, column=4, padx=5)

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files","*.csv"), ("Excel Files","*.xlsx")])
        if self.file_path:
            self.file_label.config(text=self.file_path)

    def read_file(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please select a file first")
            return

        try:
            if self.file_path.endswith(".csv"):
                self.df = pd.read_csv(self.file_path)
            else:
                self.df = pd.read_excel(self.file_path)

            rows, cols = self.df.shape
            self.info_label.config(text=f"Rows: {rows} | Columns: {cols}\nColumns: {list(self.df.columns)}")

            # Detect columns
            text_cols = self.df.select_dtypes(include='object').columns.tolist()
            num_cols = self.df.select_dtypes(include=['int64','float64']).columns.tolist()

            self.group_col['values'] = text_cols
            self.value_col['values'] = num_cols

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def preview_report(self):
        if self.df is None:
            messagebox.showerror("Error", "Please read file first")
            return

        group = self.group_col.get()
        agg = self.agg_method.get()
        value = self.value_col.get()

        if not group or not agg or not value:
            messagebox.showerror("Error", "Please select all options")
            return

        try:
            self.report_df = self.df.groupby(group)[value].agg(agg).reset_index()
            self.report_df = self.report_df.sort_values(by=value, ascending=False)

            # Clear tree
            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = list(self.report_df.columns)
            self.tree["show"] = "headings"

            for col in self.report_df.columns:
                self.tree.heading(col, text=col)

            for _, row in self.report_df.iterrows():
                self.tree.insert("", "end", values=list(row))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_report(self):
        if self.report_df is None:
            messagebox.showerror("Error", "No report to export")
            return

        try:
            folder = os.path.dirname(self.file_path)
            path = os.path.join(folder, "report.xlsx")
            self.report_df.to_excel(path, index=False)
            messagebox.showinfo("Success", f"Report saved at {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def preview_chart(self):
        if self.report_df is None:
            messagebox.showerror("Error", "Generate report first")
            return

        chart = self.chart_type.get()
        if not chart:
            messagebox.showerror("Error", "Select chart type")
            return

        fig, ax = plt.subplots()

        x = self.report_df.iloc[:,0]
        y = self.report_df.iloc[:,1]

        if chart == "bar":
            ax.bar(x, y)
        elif chart == "line":
            ax.plot(x, y)
        elif chart == "pie":
            ax.pie(y, labels=x, autopct="%1.1f%%")

        # Show in GUI
        chart_window = tk.Toplevel(self.root)
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def export_chart(self):
        if self.report_df is None:
            messagebox.showerror("Error", "Generate report first")
            return

        try:
            folder = os.path.dirname(self.file_path)
            path = os.path.join(folder, "chart.png")

            x = self.report_df.iloc[:,0]
            y = self.report_df.iloc[:,1]

            plt.figure()

            if self.chart_type.get() == "bar":
                plt.bar(x, y)
            elif self.chart_type.get() == "line":
                plt.plot(x, y)
            elif self.chart_type.get() == "pie":
                plt.pie(y, labels=x, autopct="%1.1f%%")

            plt.savefig(path)
            messagebox.showinfo("Success", f"Chart saved at {path}")

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = DataAnalyzerApp(root)
    root.mainloop()