import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

class GUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GUI")
        # self.root.geometry("500x500")
        # self.root.resizable(False, False)

        self.text = tk.Text(self.root,height=7,width=60)
        self.text.pack()
        self.text.tag_config('red', foreground='red')
        self.text.tag_config('blue', foreground='blue')
        self.text.tag_config('green', foreground='green')

        img = np.zeros((200,200,3),dtype=np.uint8)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        self.panel = tk.Label(self.root, image=img)
        self.panel.image = img
        self.panel.pack()

        self.label = None
        self.frame = tk.Frame(self.root)
        self.button1 = tk.Button(self.frame, text="STOP HERE", command=self.button1_clicked)
        self.button2 = tk.Button(self.frame, text="GOOD", command=self.button2_clicked)
        self.button3 = tk.Button(self.frame, text="New Env", command=self.button3_clicked)
        self.button1.grid(row=1, column=1)
        self.button2.grid(row=1, column=2)
        self.button3.grid(row=1, column=3)
        self.frame.pack()

    def display_goal(self, goal, preference):
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, "goal: "+goal, 'red')
        self.text.insert(tk.END, '\n')
        self.text.insert(tk.END, "preference: "+preference, 'blue')
        self.text.insert(tk.END, '\n')
        self.label = None
        self.root.update()

    def button3_clicked(self):
        self.label = 3

    def button1_clicked(self):
        self.label = 1

    def button2_clicked(self):
        self.label = 2
    
    def display_video(self,clip):
        self.label = None
        self.root.update()
        while True:
            for i, frame in enumerate(clip.iter_frames()):
                self.root.after(50, self.update_frame(frame))
                if self.label is not None:
                    if self.label == 1: return i
                    else: return -1
                
    def update_frame(self, img):
        frame_img = ImageTk.PhotoImage(Image.fromarray(img))
        self.panel.config(image=frame_img)
        self.panel.image = frame_img
        self.root.update()