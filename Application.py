import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageTk


class App():
    def __init__(self):
        super().__init__()

    def setInputPic(self, input_pic):
        self.input_pic = input_pic
        
    def resizePic(self):
        pass
    def splitPic(self):
        pass

'''
def BUTTON_UPLOAD_clicked():
    tk.Tk().withdraw()
    file = tk.filedialog.askopenfilename()
    image = Image.open(file)

    test = ImageTk.PhotoImage(image)

    input_pic_label = tk.Label(image=test)
    input_pic_label.image = test
    input_pic_label.grid(column = 2, row=2)
    
    myApp.setInputPic(image)


global myApp
myApp = App()

window = tk.Tk()
window.title("Hello World")
window.geometry('900x600')

lbl = tk.Label(window, text="Maximum square resolution of 1080 by 1080")
lbl.grid(column=0, row=0)

BUTTON_UPLOAD = tk.Button(window, text="Upload Image", command=BUTTON_UPLOAD_clicked)
BUTTON_UPLOAD.grid(column=1, row=1)


txt = tk.Entry(window,width=10)
txt.grid(column=0,row=1)


window.mainloop()
'''