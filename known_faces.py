import cv2
import face_recognition
import numpy as np
import os
import pyttsx3
import tkinter as tk
from tkinter import messagebox
import threading

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# Preload known faces and their names
known_face_encodings = []
known_face_names = []

# Speak a message
def speak(message):
    engine.say(message)
    engine.runAndWait()

# Load known faces from a specified folder
def load_known_faces(folder="known_faces"):
    try:
        for filename in os.listdir(folder):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(folder, filename)
                image = face_recognition.load_image_file(image_path)
                encoding = face_recognition.face_encodings(image)[0]
                known_face_encodings.append(encoding)
                known_face_names.append(os.path.splitext(filename)[0])
        print(f"Loaded {len(known_face_names)} known faces.")
    except Exception as e:
        print(f"Error loading faces: {e}")
        speak("Error loading known faces. Please check the folder.")

# Capture an image from the webcam
def capture_image():
    speak("Opening camera. Please look at the camera.")
    video_capture = cv2.VideoCapture(0)
    
    if not video_capture.isOpened():
        speak("Error accessing camera.")
        return None

    ret, frame = video_capture.read()
    if ret:
        temp_image_path = "captured_image.jpg"
        cv2.imwrite(temp_image_path, frame)
        speak("Image captured successfully.")
        video_capture.release()
        return temp_image_path
    else:
        speak("Failed to capture an image.")
        video_capture.release()
        return None

# Recognize the face in the captured image
def recognize_face_from_image(image_path):
    try:
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        if len(face_encodings) > 0:
            face_encoding = face_encodings[0]
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                speak(f"Hello {name}, welcome back!")
                return name
            else:
                speak("Sorry, I do not recognize this face.")
        else:
            speak("No face detected in the image.")
    except Exception as e:
        print(f"Error during face recognition: {e}")
        speak("An error occurred during face recognition.")
    return None

# Process user commands
def process_command(command):
    if command:
        speak(f"Processing command: {command}")
    else:
        speak("Please enter a valid command.")

# GUI for user interaction
def gui_interface(user_name):
    def on_command_entry():
        command = command_entry.get()
        if command:
            process_command(command)
            command_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a command.")

    # Tkinter GUI setup
    root = tk.Tk()
    root.title(f"Welcome {user_name}")
    tk.Label(root, text=f"Hi {user_name}, enter a command:", font=("Arial", 14)).pack(pady=10)

    command_entry = tk.Entry(root, width=40, font=("Arial", 14))
    command_entry.pack(pady=10)

    submit_button = tk.Button(root, text="Submit", font=("Arial", 12), command=on_command_entry)
    submit_button.pack(pady=5)

    root.mainloop()

# Main program
def main():
    load_known_faces()  # Load known faces
    image_path = capture_image()  # Capture an image
    if image_path:
        user_name = recognize_face_from_image(image_path)
        if user_name:
            gui_interface(user_name)
        else:
            speak("Face recognition failed. Exiting application.")
    else:
        speak("Could not capture an image. Exiting application.")

if __name__ == "__main__":
    threading.Thread(target=main).start()
