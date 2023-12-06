import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class GUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GUI")
        # self.root.geometry("500x500")
        # self.root.resizable(False, False)

        self.text = tk.Text(self.root,height=5,width=80)
        self.text.pack()
        self.text.tag_config('red', foreground='red')
        self.text.tag_config('blue', foreground='blue')
        self.text.tag_config('green', foreground='green')


        self.fig = Figure(figsize=(5,3))
        self.window = FigureCanvasTkAgg(self.fig, self.root)
        self.window.get_tk_widget().pack()

        self.label = None
        self.frame = tk.Frame(self.root)
        self.button1 = tk.Button(self.frame, text="goal_1", command=self.button1_clicked)
        self.button2 = tk.Button(self.frame, text="goal_2", command=self.button2_clicked)
        self.button3 = tk.Button(self.frame, text="none", command=self.button3_clicked)
        self.button1.grid(row=1, column=1)
        self.button2.grid(row=1, column=2)
        self.button3.grid(row=1, column=3)
        self.frame.pack()

    def button1_clicked(self):
        self.label = 1
        
    def button2_clicked(self):
        self.label = 2
    
    def button3_clicked(self):
        self.label = 3

    def display_goals(self, goal_1, goal_2):
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, "goal_1: "+goal_1, 'red')
        self.text.insert(tk.END, '\n')
        self.text.insert(tk.END, "goal_2: "+goal_2, 'blue')
        self.text.insert(tk.END, '\n')
        self.label = None
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