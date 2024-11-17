from tkinter import Tk, Label
from PIL import Image, ImageTk, ImageSequence
import pygame
from pygame import mixer

# Initialize the mixer for music playback
mixer.init()

# Create the main Tkinter window
root = Tk()
root.geometry("1000x500")
root.title("GIF Player")

# Label to display the GIF
lbl = Label(root)
lbl.pack()

# Function to play the GIF and music
def play_gif(index=0):
    global img_frames, lbl
    # Set the current frame to display
    frame = img_frames[index]
    img_frame = ImageTk.PhotoImage(frame)
    lbl.config(image=img_frame)
    lbl.image = img_frame  # Keep a reference to avoid garbage collection

    # Schedule the next frame
    index = (index + 1) % len(img_frames)  # Loop back to the first frame
    root.after(50, play_gif, index)  # Display the next frame after 50ms

# Load the GIF and music
try:
    gif_path = "path/to/your/gif.gif"  # Replace with your GIF file path
    music_path = "path/to/your/music.mp3"  # Replace with your MP3 file path

    # Load GIF frames
    img = Image.open(gif_path)
    img_frames = [frame.resize((1000, 500)) for frame in ImageSequence.Iterator(img)]

    # Play the music
    mixer.music.load(music_path)
    mixer.music.play()

    # Start playing the GIF
    play_gif()

    # Stop the music when the window is closed
    def on_closing():
        mixer.music.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

except Exception as e:
    print(f"Error: {e}")
    root.destroy()

# Start the Tkinter event loop
root.mainloop()
