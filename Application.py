import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageTk
import numpy as np
import os



class App():
    def __init__(self):
        super().__init__()
        self.max_pixels = 1080
        self.tiles = []
        self.dynamic_tiles = []


    def setInputPic(self,input_address, input_pic):
        self.input_address = input_address
        self.input_pic = input_pic
        self.input_arr = np.array(self.input_pic)
        
    def resizePic(self):
        if self.input_arr.shape[1]>self.max_pixels*3:
            ratio = self.max_pixels*3/self.input_arr.shape[1]
            self.input_pic = self.input_pic.resize((self.max_pixels*3, int(np.ceil(ratio*self.input_arr.shape[0]))), Image.LANCZOS)
            self.input_arr = np.array(self.input_pic)

        self.square_length = self.input_arr.shape[1]//3
        rows = self.input_arr.shape[0]//self.square_length

        self.input_arr = self.input_arr[:rows*1080,:self.square_length*3,:]
        self.input_pic = Image.fromarray(self.input_arr)
        pass
    
    def splitPic(self):
        total_rows = self.input_arr.shape[0]//self.square_length
        for row in range(total_rows):    
            for col in range(3):
                tile = self.input_arr[row*self.square_length:(row+1)*self.square_length,col*self.square_length:(col+1)*self.square_length,:]
                self.tiles.append(tile)
        pass

    def savePic(self, name):
        try:
            self.input_pic.save(name)
            print('Image Saved')
        except:
            print('Unable to save image')
        return
    
    def saveTiles(self):
        index=0
        for i in self.tiles:
            row, col = self.indexToRowCol(index)
            Image.fromarray(i).save("Tile_row{}_col{}.png".format(row,col))
            index+=1

    def rowcolToIndex(self,row,col):
        index = row*3+col
        return index

    def indexToRowCol(self,index):
        row = index//3
        col = index%3
        return row, col
    
    def getDynamicTiles(self):
        self.dynamic_tiles = self.tiles # temporary
        return self.dynamic_tiles


def displaySplitPics():
    index=0
    row_offset = 4
    col_offset = 4
    tile_labels = []
    for i in myApp.getDynamicTiles():
        tile = ImageTk.PhotoImage(Image.fromarray(i).resize((80,80)))
        tile_labels.append(tk.Label(image=tile))
        tile_labels[index].image = tile
        row, col = myApp.indexToRowCol(index)
        tile_labels[index].grid(column = col_offset+col, row = row_offset + row)
        index+=1

def displayInput(image, col, row):
    width, height = image.size
    ratio = 100/width
    test = ImageTk.PhotoImage(image.resize((400, int(ratio*height))))

    input_pic_label = tk.Label(image=test)
    input_pic_label.image = test
    input_pic_label.grid(column = col, row=row)


def BUTTON_UPLOAD_clicked():
    tk.Tk().withdraw()
    file = tk.filedialog.askopenfilename()
    image = Image.open(file)
    print("Image uploaded")
    
    myApp.setInputPic(file,image)
    myApp.resizePic()
    myApp.splitPic()
    print(len(myApp.tiles))
    displaySplitPics()

def ShowChoice():
    print(mode.get())


global myApp
myApp = App()

window = tk.Tk()
window.title("Hello World")
window.geometry('900x600')

lbl = tk.Label(window, text="Maximum square resolution of 1080 by 1080")
lbl.grid(column=0, row=0)

BUTTON_UPLOAD = tk.Button(window, text="Upload Image", command=BUTTON_UPLOAD_clicked)
BUTTON_UPLOAD.grid(column=0, row=1)

mode = tk.IntVar()
mode.set(0)
modes = [("Mode 0", 0),
   	        ("Mode 1", 1),
    	    ("Mode 2", 2)]
tk.Label(window, 
         text="Choose your favourite programming language:").grid(column=0, row=5)
for name, val in modes:
    tk.Radiobutton(window, 
                   text=name,
                   variable=mode, 
                   command=ShowChoice,
                   value=val).grid(column=0, row =6+val)


#txt = tk.Entry(window,width=10)
#txt.grid(column=0,row=1)


window.mainloop()


'''
myApp = App()
myApp.setInputPic('Test_Image.jpg',Image.open('Test_Image.jpg'))
print(myApp.input_arr.shape)
myApp.resizePic()
myApp.savePic("tmp.png")
print(myApp.input_arr.shape)
myApp.splitPic()
myApp.saveTiles()
print(len(myApp.tiles))
'''