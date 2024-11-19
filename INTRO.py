from tkinter import Tk, Label
from PIL import Image, ImageTk, ImageSequence
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

# Global variables for frames and music path
img_frames = []
music_path = "path/to/your/music.mp3"  # Replace with your MP3 file path


def play_gif(index=0):
    """Play the animated GIF by iterating over its frames."""
    global img_frames, lbl
    try:
        # Set the current frame to display
        frame = img_frames[index]
        img_frame = ImageTk.PhotoImage(frame)
        lbl.config(image=img_frame)
        lbl.image = img_frame  # Keep a reference to avoid garbage collection

        # Schedule the next frame
        index = (index + 1) % len(img_frames)  # Loop back to the first frame
        root.after(50, play_gif, index)  # Display the next frame after 50ms
    except Exception as e:
        print(f"Error in GIF playback: {e}")


def load_gif_and_music(gif_path, music_path):
    """Load the GIF frames and start music playback."""
    global img_frames
    try:
        # Load GIF frames
        img = Image.open(gif_path)
        img_frames = [frame.resize((1000, 500)) for frame in ImageSequence.Iterator(img)]

        # Start playing the music
        mixer.music.load(music_path)
        mixer.music.play()

        # Start playing the GIF
        play_gif()
    except FileNotFoundError:
        print("Error: File not found. Please check the file paths.")
        root.destroy()
    except Exception as e:
        print(f"Error: {e}")
        root.destroy()


def on_closing():
    """Stop the music and close the application."""
    mixer.music.stop()
    root.destroy()


# Replace with your GIF and music file paths
gif_path = "path/to/your/gif.gif"  # Replace with your GIF file path

# Bind the close event to the cleanup function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Load the GIF and music and start the application
load_gif_and_music(gif_path, music_path)

# Start the Tkinter event loop
root.mainloop()
