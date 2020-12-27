import math, os, cv2
from threading import Thread
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from catsnake import *

#experimental thread stuff for seeing if program remains responsive while simultaneously doing other stuff
class TestThread(Thread):
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        while True:
            print("a")

class CaptureThread(Thread):
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.cap = False
        Thread.__init__(self)
    
    def capture(self):
        ret_val, cvimg = self.cam.read()
        cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cvimg)
        app.updatePreview(img)

#this class controls all the windows and such
class UIHandler:
    def __init__(self, root):
        #create notebook for tabs
        self.tab_parent = ttk.Notebook(root)

        self.initThreads()

        #initialize the tabs in the top bar
        self.initTabs()

        #initialize the variables
        self.initVariables()

        #initialize the content for each tab
        self.initCameraTab()

        #complete everything so it displays on screen
        self.tab_parent.pack(expand=1, fill="both")
    
    def initThreads(self):
        self.cap_thread = CaptureThread()
        self.cap_thread.start()

    def initTabs(self):
        #make camera tab
        self.camera_tab = ttk.Frame(self.tab_parent)
        self.tab_parent.add(self.camera_tab, text="Cameras")
        #make capture tab
        self.capture_tab = ttk.Frame(self.tab_parent)
        self.tab_parent.add(self.capture_tab, text="Capture")

    def initVariables(self):
        self.preview_img = Image.new("RGB", (640, 480), "black")
        self.preview = ImageTk.PhotoImage(self.preview_img)

    def initCameraTab(self):
        #Add text to tab
        self.camtab_camera = Label(self.camera_tab, text="Select camera:", padx=10, pady=10)

        #Place text in proper position on grid
        self.camtab_camera.grid(row=0, column=0)

        #add buttons to tab
        self.testbutton = Button(self.camera_tab, text="Test", command=self.capture)

        #align buttons to grid
        self.testbutton.grid(row=0, column=1)

        #preview image
        self.preview_image = Label(self.camera_tab, image=self.preview)
        self.preview_image.grid(row=0, column=2)
    
    def capture(self):
        self.cap_thread.capture()
    
    def updatePreview(self, img):
        self.preview_img = img
        self.preview = ImageTk.PhotoImage(self.preview_img)
        self.preview_image.configure(image=self.preview)

if __name__ == "__main__":
    #create the root and resize to correct size
    root = Tk()
    root.title("AstroCapture V1.0.0")
    root.minsize(1280, 720)
    app = UIHandler(root) #pass root on to the UI Handler
    root.mainloop() #main tkinter loop for interface
    os._exit(0) #quit program including threads