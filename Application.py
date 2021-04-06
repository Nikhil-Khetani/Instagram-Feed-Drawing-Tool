import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageTk
import numpy as np
import os
from copy import deepcopy


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
        return self.dynamic_tiles

    def joinTiles(self):
        for i in range(int(len(self.dynamic_tiles)/3)):
            row_tile = np.concatenate((self.dynamic_tiles[3*i+0],self.dynamic_tiles[3*i+1],self.dynamic_tiles[3*i+2]),axis=1)
            if i==0:
                self.combined_array = row_tile
            else:
                self.combined_array = np.concatenate((self.combined_array,row_tile), axis=0)
        self.combined_pic = Image.fromarray(self.combined_array)
        return

    def saveCombinedPic(self,name):
        try:
            self.combined_pic.save(name)
            print('Image Saved')
        except:
            print('Unable to save image')
        return

    def ShiftTiles(self,current_mode):
        self.dynamic_tiles = deepcopy(self.tiles)
        empty_array = np.zeros_like(self.tiles[0])
        if current_mode==-2:
            self.dynamic_tiles.pop(0)
            self.dynamic_tiles.pop(0)
            self.dynamic_tiles.pop()
        elif current_mode == -1:
            self.dynamic_tiles.pop(0)
            self.dynamic_tiles.pop()
            self.dynamic_tiles.pop()
        elif current_mode == 1:
            self.dynamic_tiles.insert(0,empty_array)
            self.dynamic_tiles.append(empty_array)
            self.dynamic_tiles.append(empty_array)
        elif current_mode == 2:
            self.dynamic_tiles.insert(0,empty_array)
            self.dynamic_tiles.insert(0,empty_array)
            self.dynamic_tiles.append(empty_array)
        return


def clearSplitPics():
    global tile_labels
    for i in tile_labels:
        #i.config(image='')
        i.destroy()

def displaySplitPics():
    global tile_labels

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
    return 

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
    myApp.ShiftTiles(0)
    displaySplitPics()
    

def BUTTON_SAVE_clicked():
    global SAVE_NAME_ENTRY
    myApp.joinTiles()
    myApp.saveCombinedPic(SAVE_NAME_ENTRY.get()+".png")

def ShiftMode():
    myApp.ShiftTiles(mode.get())
    clearSplitPics()
    displaySplitPics()
    print(mode.get())


global myApp
myApp = App()

row_layout = {
            'TITLE_LABEL': 1,
            'SUBTITLE_LABEL': 2,
            'TEXT_LABEL': 3,
            'TEXT_LABEL2': 4,
            'BUTTON_UPLOAD': 5,
            'SHIFT_MODE_TITLE':6,
            'SHIFT_MODE_RADIO': 7, #Note this also has the next 4 rows aswell ie 6,7,8,9,10
            'SAVE_NAME_ENTRY': 12,
            'BUTTON_SAVE': 13
            }

window = tk.Tk()
window.title("Hello World")
window.geometry('900x600')


tile_labels = []

#Title Label
tk.Label(window, text="Instagram Feed Drawing Tool").grid(column=0, row=row_layout['TITLE_LABEL'])

# Subtitle Label
tk.Label(window, text="For designing continuous tiled backgrounds for your instagram profile ").grid(column=0, row=row_layout['SUBTITLE_LABEL'])

#Text Label
tk.Label(window, text="Upload the image you want to use - on first upload we resize automatically for you").grid(column=0, row=row_layout['TEXT_LABEL'])
#Text Label2
tk.Label(window, text="Taking into consideration the maximum instagram image square resolution size of 1080 by 1080").grid(column=0, row=row_layout['TEXT_LABEL2'])

#Button Upload Label
BUTTON_UPLOAD = tk.Button(window, text="Upload Image", command=BUTTON_UPLOAD_clicked)
BUTTON_UPLOAD.grid(column=0, row=row_layout['BUTTON_UPLOAD'])

#Shift mode title

#Shift mode radio
mode = tk.IntVar()
mode.set(0)
modes = [("Shift -2", -2),
        ("Shift -1", -1),
        ("Shift 0", 0),
   	    ("Shift 1", 1),
    	("Shift 2", 2)]
tk.Label(window, 
         text="Choose your favourite programming language:").grid(column=0, row=row_layout['SHIFT_MODE_TITLE'])
for name, val in modes:
    tk.Radiobutton(window, 
                   text=name,
                   variable=mode, 
                   command=ShiftMode,
                   value=val).grid(column=0, row = row_layout['SHIFT_MODE_RADIO']+2+val)


#Save Name Entry
global SAVE_NAME_ENTRY
SAVE_NAME_ENTRY = tk.Entry(window,text='Name the file to be saved (include .png)', width=10)
SAVE_NAME_ENTRY.grid(column=0,row=row_layout['SAVE_NAME_ENTRY'])


#Button Save
BUTTON_SAVE = tk.Button(window, text="Combine and Save", command=BUTTON_SAVE_clicked)
BUTTON_SAVE.grid(column=0, row=row_layout['BUTTON_SAVE'])



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