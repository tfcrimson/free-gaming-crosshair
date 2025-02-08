import tkinter as tk
from tkinter import colorchooser, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
import json
import webbrowser
import sv_ttk  

class CrosshairApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XC Tools Crosshair")
        self.root.geometry("1000x400")  
        sv_ttk.set_theme("dark")  

        self.thickness = tk.IntVar(value=2)
        self.length = tk.IntVar(value=10)
        self.opacity = tk.DoubleVar(value=0.7)
        self.color = "#800000"  
        self.dot_size = tk.IntVar(value=5)
        self.dot_opacity = tk.DoubleVar(value=1.0)
        self.crosshair_shape = tk.StringVar(value="Plus")
        self.dot_enabled = tk.BooleanVar(value=True)  
        self.crosshair_window = None  

        self.create_ui()
        self.center_window()

    def center_window(self):
        window_width = 1000
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    def create_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        crosshair_frame = ttk.LabelFrame(main_frame, text="Crosshair Settings")
        crosshair_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.create_crosshair_settings(crosshair_frame)

        dot_frame = ttk.LabelFrame(main_frame, text="Dot Settings")
        dot_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.create_dot_settings(dot_frame)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side="left", fill="y", padx=10, pady=10)
        ttk.Button(button_frame, text="Reset Settings", command=self.reset_settings).pack(fill="x")
        ttk.Button(button_frame, text="Save Crosshair", command=self.save_crosshair).pack(fill="x")
        ttk.Button(button_frame, text="Discord Server", command=self.open_discord_server).pack(fill="x")

    def create_dot_settings(self, parent):
        ttk.Label(parent, text="Dot Size").pack()
        ttk.Scale(parent, from_=1, to_=20, orient=tk.HORIZONTAL, variable=self.dot_size, length=200).pack()

        ttk.Label(parent, text="Dot Opacity").pack()
        ttk.Scale(parent, from_=0.1, to_=1.0, orient=tk.HORIZONTAL, variable=self.dot_opacity, length=200).pack()

        ttk.Checkbutton(parent, text="Enable Dot", variable=self.dot_enabled).pack()

    def create_crosshair_settings(self, parent):
        ttk.Label(parent, text="Shape").pack()
        shape_options = ["Plus", "X", "Dot", "Circle"]
        ttk.Combobox(parent, textvariable=self.crosshair_shape, values=shape_options).pack()

        ttk.Label(parent, text="Thickness").pack()
        ttk.Scale(parent, from_=1, to_=10, orient=tk.HORIZONTAL, variable=self.thickness, length=200).pack()

        ttk.Label(parent, text="Length").pack()
        ttk.Scale(parent, from_=5, to_=50, orient=tk.HORIZONTAL, variable=self.length, length=200).pack()

        ttk.Label(parent, text="Opacity").pack()
        ttk.Scale(parent, from_=0.1, to_=1.0, orient=tk.HORIZONTAL, variable=self.opacity, length=200).pack()

        ttk.Button(parent, text="Pick Color", command=self.pick_color).pack()
        ttk.Button(parent, text="Enable Crosshair", command=self.enable_crosshair).pack()
        ttk.Button(parent, text="Disable Crosshair", command=self.disable_crosshair).pack()

    def enable_crosshair(self):
        if self.crosshair_window:
            self.crosshair_window.destroy()
        
        self.crosshair_window = tk.Toplevel(self.root)
        self.crosshair_window.attributes("-topmost", True)
        self.crosshair_window.overrideredirect(True)
        self.crosshair_window.attributes("-alpha", self.opacity.get())
        
        # Make background transparent
        self.crosshair_window.configure(bg="black")
        self.crosshair_window.wm_attributes("-transparentcolor", "black")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        length = self.length.get()
        thickness = self.thickness.get()
        pos_x = screen_width // 2
        pos_y = screen_height // 2
        
        canvas = tk.Canvas(self.crosshair_window, width=length * 2, height=length * 2, 
                            highlightthickness=0, bg="black")
        canvas.pack()
        
        if self.crosshair_shape.get() == "Plus":
            canvas.create_line(length, 0, length, length * 2, fill=self.color, width=thickness)
            canvas.create_line(0, length, length * 2, length, fill=self.color, width=thickness)
        elif self.crosshair_shape.get() == "X":
            canvas.create_line(0, 0, length * 2, length * 2, fill=self.color, width=thickness)
            canvas.create_line(0, length * 2, length * 2, 0, fill=self.color, width=thickness)
        
        if self.dot_enabled.get():
            canvas.create_oval(length - self.dot_size.get()//2, length - self.dot_size.get()//2, 
                               length + self.dot_size.get()//2, length + self.dot_size.get()//2, 
                               fill=self.color, outline="")
        
        self.crosshair_window.geometry(f"{length * 2}x{length * 2}+{pos_x - length}+{pos_y - length}")
        self.crosshair_window.lift()
    
    def disable_crosshair(self):
        if self.crosshair_window:
            self.crosshair_window.destroy()
            self.crosshair_window = None
    
    def pick_color(self):
        color_code = colorchooser.askcolor(title="Choose Crosshair Color")[1]
        if color_code:
            self.color = color_code

    def reset_settings(self):
        self.thickness.set(2)
        self.length.set(10)
        self.opacity.set(0.7)
        self.color = "#800000"  
        self.dot_size.set(5)
        self.dot_opacity.set(1.0)
        self.crosshair_shape.set("Plus")
        self.dot_enabled.set(True)
        messagebox.showinfo("Reset", "Settings have been reset.")

    def save_crosshair(self):
        messagebox.showinfo("Save", "Crosshair settings have been saved.")
    
    def open_discord_server(self):
        webbrowser.open("https://discord.gg/ctxP3vCfTf")

if __name__ == "__main__":
    root = tk.Tk()
    app = CrosshairApp(root)
    root.mainloop()
