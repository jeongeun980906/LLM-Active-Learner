import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk
import numpy as np

class GUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GUI")
        # self.root.geometry("500x500")
        # self.root.resizable(False, False)

        self.text = tk.Text(self.root,height=10,width=80)
        self.text.pack()
        self.text.tag_config('red', foreground='red')
        self.text.tag_config('blue', foreground='blue')
        self.text.tag_config('green', foreground='green')

        self.video_frame = tk.Frame(self.root)
        img = np.zeros((200,200,3),dtype=np.uint8)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        self.panel_1 = tk.Label(self.video_frame, image=img)
        self.panel_1.image = img
        self.panel_1.grid(row=1, column=1)
        self.panel_2 = tk.Label(self.video_frame, image=img)
        self.panel_2.image = img
        self.panel_2.grid(row=1, column=2)
        self.video_frame.pack()
        # self.fig = Figure(figsize=(5,3))
        # self.window = FigureCanvasTkAgg(self.fig, self.root)
        # self.window.get_tk_widget().pack()

        self.label = None
        self.frame = tk.Frame(self.root)
        self.button1 = tk.Button(self.frame, text="goal_1", command=self.button1_clicked)
        self.button2 = tk.Button(self.frame, text="goal_2", command=self.button2_clicked)
        self.button3 = tk.Button(self.frame, text="none", command=self.button3_clicked)
        self.button4 = tk.Button(self.frame, text="new env", command=self.button4_clicked)
        self.button1.grid(row=1, column=1)
        self.button2.grid(row=1, column=2)
        self.button3.grid(row=1, column=3)
        self.button4.grid(row=1, column=4)
        self.frame.pack()

    def button4_clicked(self):
        self.label = 4

    def button1_clicked(self):
        self.label = 1
        
    def button2_clicked(self):
        self.label = 2
    
    def button3_clicked(self):
        self.label = 3

    def display_goals(self, goal_1, goal_2, preference):
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, "preference: "+preference, 'green')
        self.text.insert(tk.END, '\n')
        self.text.insert(tk.END, "goal_1: "+goal_1, 'red')
        self.text.insert(tk.END, '\n')
        self.text.insert(tk.END, "goal_2: "+goal_2, 'blue')
        self.text.insert(tk.END, '\n')
        self.label = None
        self.root.update()


    def display_videos(self, video_1, video_2):
        self.label = None
        self.root.update()
        max_frame = max(len(video_1), len(video_2))
        while True:
            for i in range(max_frame):
                if i < len(video_1):
                    self.panel_1.after(25, self.update_frame(video_1[i], 1))
                # else:
                #     self.root.after(50, self.update_frame(None, 1))
                if i < len(video_2):
                    # print("?")
                    self.panel_2.after(25, self.update_frame(video_2[i], 2))
                # else:
                #     self.root.after(50, self.update_frame(None, 2))
                if self.label is not None:
                    return self.label
                self.root.update()
            

    def update_frame(self, img, idx):
        frame_img = ImageTk.PhotoImage(Image.fromarray(img))
        if idx == 1:
            self.panel_1.config(image=frame_img)
            self.panel_1.image = frame_img
        else:
            self.panel_2.config(image=frame_img)
            self.panel_2.image = frame_img
        self.root.update()

    def display_image(self, img_1, img_2):
        self.fig.clear()
        ax1 = self.fig.add_subplot(121)
        if img_1 is not None:
            ax1.imshow(img_1)
        ax1.axis('off')
        ax2 = self.fig.add_subplot(122)
        if img_2 is not None:
            ax2.imshow(img_2)
        ax2.axis('off')
        self.fig.tight_layout()
        self.window.draw()
        # self.window = FigureCanvasTkAgg(self.fig, self.root)
        # self.window.get_tk_widget().pack()
        self.root.update()