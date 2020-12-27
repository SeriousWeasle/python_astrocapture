#Dependencies
import math, os, cv2 #math for math, os for camera control via v4l2-ctl and cv2 for getting images from the webcam
from tkinter import * #interface library
from tkinter import ttk #idk needed for tabs and such in interface
from PIL import Image, ImageTk #image manipulation library I always use and am familiar with
from catsnake import * #math and such

class captureApp:
    def __init__(self, rt):
        self.cameras = [None]
        self.prev_img = None
        self.preview_image = Image.new("RGB", (640, 480), "black")

        self.tab_parent = ttk.Notebook(rt)

        self.init_settings()

        self.init_tabs()
        self.init_variables()

        self.init_cameratab()

        self.tab_parent.pack(expand=1, fill="both")

        self.preview_window.configure(image=self.prev_img)
    
    def init_settings(self):
        #gather cameras and settings for one of them
        self.detect_cameras()

    def init_tabs(self):
        #initialize tkinter tabs here
        self.camera_tab = ttk.Frame(self.tab_parent)
        self.tab_parent.add(self.camera_tab, text="Camera settings")

    def init_variables(self):
        #initialize tkinter variables with attachted functions here
        self.currentCamera = StringVar()
        self.currentCamera.set(self.cameras[0])

    def init_cameratab(self):
        #tab with camera settings and controls
        Button(self.camera_tab, text="List cameras", command=self.detect_cameras).grid(row=0, column=0)
        OptionMenu(self.camera_tab, self.currentCamera, *self.cameras).grid(row=0, column=1)
        self.testPreview()

    def detect_cameras(self):
        self.cameras = []
        os.system("ls /dev/video* > cameralist") #get all cameras from /dev/video* and write to file named cameralist
        with open("./cameralist", "r") as cl:
            cl_list = cl.readlines() #get the lines from the file just generated from the ls command
            for c in cl_list: #go over raw file lines
                self.cameras.append(c[-2:-1]) #clean up and append to array
    
    def testPreview(self):
        self.prev_img = ImageTk.PhotoImage(self.preview_image)
        self.preview_window = Label(self.camera_tab, image=self.prev_img)
        self.preview_window.grid(row=0, column=3)

#start the app window and such
root = Tk()
root.title("Telescope Webcam Control")
root.minsize(1280, 720)
app = captureApp(root)
root.mainloop()