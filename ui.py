from matplotlib.pyplot import imread
import tkinter as tk
from PIL import ImageTk, Image

pairs = []
with open("pairs.txt", "r") as file:
    for line in file.readlines():
        a, b = line.split(", ")
        b = b.replace("\n", "")
        pairs.append((a, b))

WIDTH, HEIGHT = 640, 480

#im = Image.open("data/126_pos.tiff")
#test = np.array(im)
#print(np.max(test), type(test[0][0]))
#plt.imshow(im, cmap="gray", vmin=0, vmax=65535)
#plt.show()

window = tk.Tk()
im = Image.open("data/126_pos.tiff")
image = ImageTk.PhotoImage(im)
panel = tk.Label(image=image)
panel.pack()
tk.mainloop()
