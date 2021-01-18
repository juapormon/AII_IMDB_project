import tkinter
from tkinter import *
from tkinter import messagebox


class Template:
    def __init__(self, title, geometry="500x350+10+20"):
        self.window = tkinter.Tk()
        self.frame = Frame(self.window)
        self.frame.pack()
        self.window.title = title
        self.window.geometry = geometry

    def add_button(self, command, text="button", active_background="#FFFFFF", side=LEFT):
        button = Button(self.frame, text=text, activebackground=active_background, command=command)
        button.pack(side=side)

    def print(self):
        print("IS WORKING")

    def start(self):
        self.frame.mainloop()
        

def create_list(values):
    top_level = Toplevel()
    sc = Scrollbar(top_level)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(top_level, width=150, yscrollcommand=sc.set)
    for value in values:
        lb.insert(END, "\n")
        lb.insert(END, value)
        lb.insert(END, "--------------------------------")
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)

def buttonAction():
    create_list(["VALUE1, VALUE2, VALUE3"])


if __name__ == '__main__':
    window = tkinter.Tk()
    frame = Frame(window)
    frame.pack()
    button = Button(frame, text="text", command=buttonAction)
    button.pack(side=LEFT)
    frame.mainloop()
