import PIL.Image
import PIL.ImageTk
from tkinter import *
from cmu_112_graphics import * #graphics package taken from class


# root = Tk()

# root.geometry("400x200")

# fp = open("splashTitle.png","rb")
# image = PIL.Image.open(fp)
# photo = PIL.ImageTk.PhotoImage(image)

# label = Label(image=photo)
# label.pack()
# root.mainloop() 

class MyApp(App):
    def appStarted(self):
        self.image1 = self.loadImage("splashTitle.png") 

    def redrawAll(self, canvas):
        canvas.create_image(400, 400, image=ImageTk.PhotoImage(self.image1)) 

MyApp(width=840, height=840)