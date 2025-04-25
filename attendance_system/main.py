import customtkinter as ctk  # Modern Tkinter
import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition
import numpy as np
import os
import sqlite3
from datetime import datetime, date
from PIL import Image, ImageTk  # For displaying live camera feed

# === SETUP ===
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# === DATABASE SETUP ===
conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        timestamp TEXT
    )
''')
conn.commit()

# === LOAD KNOWN FACES ===
known_faces = []
known_names = []
image_folder = "images"

for file in os.listdir(image_folder):
    if file.endswith((".jpg", ".png", ".jpeg")):
        image = face_recognition.load_image_file(os.path.join(image_folder, file))
        encoding = face_recognition.face_encodings(image)
        if encoding:
            known_faces.append(encoding[0])
            known_names.append(os.path.splitext(file)[0])

# === CHECK ATTENDANCE ===
def is_already_marked_today(name):
    today = date.today().isoformat()
    cursor.execute("SELECT * FROM attendance WHERE name=? AND timestamp LIKE ?", (name, today + '%'))
    return cursor.fetchone() is not None

# === CAMERA & FACE RECOGNITION ===
cap = None
def start_recognition():
    global cap
    cap = cv2.VideoCapture(0)

    def update_frame():
        if cap is not None:
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = img.resize((400, 300))
                img = ImageTk.PhotoImage(img)
                camera_label.imgtk = img
                camera_label.configure(image=img)

                # FACE RECOGNITION
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_faces, face_encoding)
                    face_distances = face_recognition.face_distance(known_faces, face_encoding)
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = known_names[best_match_index]

                        if not is_already_marked_today(name):
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            cursor.execute("INSERT INTO attendance (name, timestamp) VALUES (?, ?)", (name, timestamp))
                            conn.commit()
                            messagebox.showinfo("Attendance Marked", f"{name} marked present at {timestamp}")
                            update_attendance_list()

            root.after(10, update_frame)

    update_frame()

# === STOP CAMERA ===
def stop_camera():
    global cap
    if cap is not None:
        cap.release()
        cap = None
        camera_label.configure(image='')

# === DISPLAY ATTENDANCE LOG ===
def update_attendance_list():
    cursor.execute("SELECT name, timestamp FROM attendance WHERE timestamp LIKE ?", (date.today().isoformat() + '%',))
    records = cursor.fetchall()

    attendance_listbox.delete(0, tk.END)
    for record in records:
        name, full_timestamp = record
        date_part, time_part = full_timestamp.split()
        attendance_listbox.insert(tk.END, f"{name} - {time_part}")


# === FRONTEND (Modern UI) ===
ctk.set_appearance_mode("dark")  # Light/Dark Mode
root = ctk.CTk()
root.title("Face Recognition Attendance System")
root.geometry("700x600")

# Title Label
title_label = ctk.CTkLabel(root, text="Face Recognition Attendance", font=("Arial", 24, "bold"))
title_label.pack(pady=20)

# Camera Frame
camera_label = ctk.CTkLabel(root, text="Live Camera Feed", width=400, height=300, fg_color="black")
camera_label.pack()

# Start & Stop Buttons
btn_frame = ctk.CTkFrame(root)
btn_frame.pack(pady=10)

start_btn = ctk.CTkButton(btn_frame, text="Start Camera", command=start_recognition, fg_color="green", width=200)
start_btn.grid(row=0, column=0, padx=10)

stop_btn = ctk.CTkButton(btn_frame, text="Stop Camera", command=stop_camera, fg_color="red", width=200)
stop_btn.grid(row=0, column=1, padx=10)

# Attendance Log
log_label = ctk.CTkLabel(root, text="Today's Attendance", font=("Arial", 18, "bold"))
log_label.pack(pady=5)

attendance_listbox = tk.Listbox(root, height=10, width=50)
attendance_listbox.pack()

update_attendance_list()  # Load current attendance

root.mainloop()
