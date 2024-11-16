from tkinter import Tk, Label
from PIL import Image, ImageTk, ImageSequence
import time
import pygame  #pip install pygame
from pygame import mixer
mixer.init()

root = Tk()
root.geometry("1000x500")

def play_gif():
    root.lift()
    root.attributes("-topmost", True)
    global img
    img = Image.open("path/to/your/gif.gif")  # Enter the gif address
    lbl = Label(root)
    lbl.place(x=0, y=0)
    mixer.music.load("path/to/your/music.mp3")  # Enter the music file address
    mixer.music.play()
    
    for frame in ImageSequence.Iterator(img):
        frame = frame.resize((1000, 500))
        img_frame = ImageTk.PhotoImage(frame)
        lbl.config(image=img_frame)
        root.update()
        time.sleep(0.05)
    root.destroy()

root.mainloop()