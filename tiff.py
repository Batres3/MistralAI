from tkinter import Canvas, BOTTOM, X, filedialog
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from numpy import array, ndarray, uint16, roll
import tifffile as tf

UINT_16_MAX = 65535

def shift_image(X, dx=0, dy=0):
    X = roll(X, dy, axis=0)
    X = roll(X, dx, axis=1)
    if dy>0:
        X[:dy, :] = 0
    elif dy<0:
        X[dy:, :] = 0
    if dx>0:
        X[:, :dx] = 0
    elif dx<0:
        X[:, dx:] = 0
    return X

def get_tiff_image(src: str) -> ndarray[uint16]:
    return tf.imread(src)

def get_tiff_image_tk(src: str, master, toolbar: bool = True, figsize: tuple[int, int] = (5, 4), whitespace: bool = True) -> tuple[Canvas, NavigationToolbar2Tk] | Canvas:
    fig = Figure(figsize=figsize, dpi=100)
    ax = fig.add_subplot()

    pixels = get_tiff_image("data/126_pos.tiff")
    ax.imshow(pixels, cmap="gray", vmin=0, vmax=UINT_16_MAX)
    ax.axis("off")
    
    if not whitespace:
        fig.tight_layout(pad=0)

    canvas = FigureCanvasTkAgg(fig, master=master)  # A tk.DrawingArea.
    canvas.draw()
    canvas.mpl_connect("key_press_event", key_press_handler)
    
    if not toolbar:
        return canvas.get_tk_widget()

    # pack_toolbar=False will make it easier to use a layout manager later on.
    bar = NavigationToolbar2Tk(canvas, master, pack_toolbar=False)
    bar.update()
    return canvas.get_tk_widget(), bar

class CustomToolbar(NavigationToolbar2Tk):
    def __init__(self, canvas, window=None, *, pack_toolbar=True, custom_save: callable = None):
        super().__init__(canvas, window, pack_toolbar=pack_toolbar)
        self.custom_save = custom_save
    
    def save_figure(self, *args):
        if self.custom_save is not None:
            return self.custom_save()
        return super().save_figure(*args)


class TiffImage:
    def __init__(self, src: str, master, toolbar: bool = True, figsize: tuple[int, int] = (5, 4), whitespace: bool = True, src2 = None) -> None:
        self.fig = Figure(figsize=figsize, dpi=100)
        self.ax = self.fig.add_subplot()
        self.pixels = None

        if src2 is None:
            self.pixels = get_tiff_image(src)
            self.ax.imshow(self.pixels, cmap="gray", vmin=0, vmax=UINT_16_MAX)
            self.ax.axis("off")
        
        if not whitespace:
            self.fig.tight_layout(pad=0)

        self.canvas = FigureCanvasTkAgg(self.fig, master=master)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.mpl_connect("key_press_event", key_press_handler)
        
        if not toolbar:
            return

        # pack_toolbar=False will make it easier to use a layout manager later on.
        self.bar = CustomToolbar(self.canvas, master, pack_toolbar=False, custom_save=self.save)
        self.bar.save_figure()
        self.bar.update()

        if src2 is not None:
            self.subtract(src.pixels, src2.pixels, 0, 0)
        return

    def pack(self) -> None:
        self.canvas.get_tk_widget().pack()
        self.bar.pack(side=BOTTOM, fill=X)

    def grid(self, row, column, padx, pady, columnspan=1):
        self.canvas.get_tk_widget().grid(row=row, column=column, padx=padx, pady=pady, columnspan=columnspan)
        
    def change_src_image(self, src: str) -> None:
        self.ax.clear()
        self.ax.axis("off")
        self.ax.imshow(get_tiff_image(src), cmap="gray", vmin=0, vmax=UINT_16_MAX)
        self.canvas.draw()
        
    def subtract(self, src1=None, src2=None, dx=None, dy=None):
        self.ax.clear()
        if src1 is not None and src2 is not None:
            self.src1 = src1
            self.src2 = src2
        else:
            src1 = self.src1
            src2 = self.src2
            
        if dx is not None:
            self.dx = dx
        else:
            dx = self.dx

        if dy is not None:
            self.dy = dy
        else:
            dy = self.dy

        src1 = shift_image(src1, dx=dx, dy=dy)
        self.pixels = src1 - src2
        self.ax.imshow(self.pixels, cmap="gray", vmin=0, vmax=UINT_16_MAX)
        self.ax.axis("off")
        self.canvas.draw()
        
    def save(self):
        if self.pixels is None:
            return
        tf.imsave("out.tiff",self.pixels)
