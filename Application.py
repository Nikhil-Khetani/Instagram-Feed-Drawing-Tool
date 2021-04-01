import tkinter as tk
import tkinter.filedialog
from PIL import Image

def clicked():
    tk.Tk().withdraw()
    file = tk.filedialog.askopenfilename()
    image = Image.open(file)
    var = input()

window = tk.Tk()
window.title("Hello World")
window.geometry('320x200')

lbl = tk.Label(window, text="Hello")
lbl.grid(column=0, row=0)

btn = tk.Button(window, text="Upload Image", command=clicked)
btn.grid(column=2, row=0)

txt = tk.Entry(window,width=10)
txt.grid(column=1,row=0)




window.mainloop()
