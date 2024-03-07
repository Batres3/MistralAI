import tkinter as tk
from tkinter import filedialog
import numpy as np
# Implement the default Matplotlib key bindings.
from PIL import Image
from tiff import TiffImage, shift_image, UINT_16_MAX


root = tk.Tk()
root.wm_title("Editor")

left_frame = tk.Frame(root, width=200, height=400, bg='grey')
left_frame.grid(row=0, column=0, padx=10, pady=5)

right_frame = tk.Frame(root, width=650, height=400, bg='grey')
right_frame.grid(row=0, column=1, padx=10, pady=5)

source_frame = tk.Frame(left_frame, width=200, height=200, bg='grey')
source_frame.grid(row=0, column=0, padx=10, pady=5)

manipulation_frame = tk.Frame(left_frame, width=200, height=200, bg='grey')
manipulation_frame.grid(row=1, column=0, padx=10, pady=5)

# Create frames and labels in left_frame
tk.Label(source_frame, text="Source Images").grid(row=0, column=0, columnspan=2, padx=5, pady=5)

path = filedialog.askopenfilename(defaultextension=".tiff")
source_image_1 = TiffImage(path, master=source_frame, toolbar=False, figsize=(1, 1), whitespace=False)
source_image_1.grid(row=1, column=0, padx=5, pady=5)
label_image_1 = tk.Label(master=source_frame, text=path.split("MistralAI/")[-1])
label_image_1.grid(row=2, column=0, padx=5, pady=5)
path = filedialog.askopenfilename(defaultextension=".tiff")
source_image_2 = TiffImage(path, master=source_frame, toolbar=False, figsize=(1, 1), whitespace=False)
source_image_2.grid(row=1, column=1, padx=5, pady=5)
label_image_2 = tk.Label(master=source_frame, text=path.split("MistralAI/")[-1])
label_image_2.grid(row=2, column=1, padx=5, pady=5)

main_image = TiffImage(src=source_image_1, src2=source_image_2, master=right_frame)

def arrow_pressed_callback(e):
    if e.keysym == "Up":
        main_image.subtract(dy=main_image.dy+1)
    if e.keysym == "Down":
        main_image.subtract(dy=main_image.dy-1)
    if e.keysym == "Left":
        main_image.subtract(dx=main_image.dx+1)
    if e.keysym == "Right":
        main_image.subtract(dx=main_image.dx-1)

root.bind('<Left>', arrow_pressed_callback)
root.bind('<Right>', arrow_pressed_callback)
root.bind('<Up>', arrow_pressed_callback)
root.bind('<Down>', arrow_pressed_callback)

def add_source_image_1(e):
    path = filedialog.askopenfilename(defaultextension=".tiff")
    label_image_1.config(text=path.split("MistralAI/")[-1])
    source_image_1.change_src_image(path)
def add_source_image_2(e):
    path = filedialog.askopenfilename(defaultextension=".tiff")
    label_image_2.config(text=path.split("MistralAI/")[-1])
    source_image_2.change_src_image(path)

label_image_1.bind('<Double-Button-1>', add_source_image_1)
label_image_2.bind('<Double-Button-1>', add_source_image_2)

def slider_x(x):
    main_image.subtract(dx=np.int32(x))
def slider_y(y):
    main_image.subtract(dy=np.int32(y))
max_x, max_y = main_image.pixels.shape
min_x, min_y = -max_x, -max_y
dx_slider = tk.Scale(master=manipulation_frame, from_=min_x, to=max_x, orient=tk.HORIZONTAL, command=slider_x)
dx_slider.grid(row=0, column=1, padx=5, pady=5)
dy_slider = tk.Scale(master=manipulation_frame, from_=min_y, to=max_y, orient=tk.HORIZONTAL, command=slider_y)
dy_slider.grid(row=1, column=1, padx=5, pady=5)
save_button = tk.Button(master=manipulation_frame, text="Save", command=lambda: main_image.save())
save_button.grid(row=2, column=1, padx=5, pady=5)

dx_max = tk.StringVar(value=max_x)
dy_max = tk.StringVar(value=max_y)
dx_min = tk.StringVar(value=min_x)
dy_min = tk.StringVar(value=min_y)
tk.Entry(master=manipulation_frame, textvariable=dx_max, width=5).grid(row=0, column=2, padx=5, pady=5)
tk.Entry(master=manipulation_frame, textvariable=dx_min, width=5).grid(row=0, column=0, padx=5, pady=5)
tk.Entry(master=manipulation_frame, textvariable=dy_max, width=5).grid(row=1, column=2, padx=5, pady=5)
tk.Entry(master=manipulation_frame, textvariable=dy_min, width=5).grid(row=1, column=0, padx=5, pady=5)
def callback_max(sv, master, default):
    if sv.get() == "" or sv.get() == "-":
        num = default
    else:
        num = float(sv.get())
    master.configure(to=num)
def callback_min(sv, master, default):
    if sv.get() == "" or sv.get() == "-":
        num = default
    else:
        num = float(sv.get())
    master.configure(from_=num)
dx_max.trace_add("write",  lambda var, index, mode, sv=dx_max: callback_max(sv, dx_slider, -max_x))
dx_min.trace_add("write",  lambda var, index, mode, sv=dx_min: callback_min(sv, dx_slider, -min_x))
dy_max.trace_add("write",  lambda var, index, mode, sv=dy_max: callback_max(sv, dy_slider, -max_y))
dy_min.trace_add("write",  lambda var, index, mode, sv=dy_min: callback_min(sv, dy_slider, -min_y))
# Packing order is important. Widgets are processed sequentially and if there
# is no space left, because the window is too small, they are not displayed.
# The canvas is rather flexible in its size, so we pack it last which makes
# sure the UI controls are displayed as long as possible.
main_image.pack()

tk.mainloop()