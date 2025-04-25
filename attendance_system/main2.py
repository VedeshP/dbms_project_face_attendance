# code for implimentation for time, deny duplicacy and added some more features.





import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition
import numpy as np
import os
import sqlite3
from datetime import datetime, date

# Set working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# === Database Setup ===
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

# === Load Known Faces ===
known_faces = []
known_names = []

image_folder = "images"
for file in os.listdir(image_folder):
    if file.endswith((".jpg", ".png", ".jpeg")):
        image = face_recognition.load_image_file(os.path.join(image_folder, file))
        encoding = face_recognition.face_encodings(image)
        if encoding:  # Check if a face is found
            known_faces.append(encoding[0])
            known_names.append(os.path.splitext(file)[0])  # e.g., John_Doe

# === Attendance Logic ===
def is_already_marked_today(name):
    today = date.today().isoformat()
    cursor.execute("SELECT * FROM attendance WHERE name=? AND timestamp LIKE ?", (name, today + '%'))
    return cursor.fetchone() is not None

# === Start Webcam Recognition ===
def start_recognition():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

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

        cv2.imshow('Face Recognition Attendance', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# === GUI ===
root = tk.Tk()
root.title("PDPU Face Attendance System")

tk.Label(root, text="Face Recognition Attendance", font=("Helvetica", 18)).pack(pady=10)
tk.Button(root, text="Start Attendance", command=start_recognition, font=("Helvetica", 14)).pack(pady=20)
tk.Label(root, text="Press 'q' to stop the camera", font=("Helvetica", 10)).pack()

root.mainloop()
