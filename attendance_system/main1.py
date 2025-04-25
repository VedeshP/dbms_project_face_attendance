# basic code for face recognition attendance system..







import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition
import numpy as np
import os
import sqlite3
from datetime import datetime
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Database setup
conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    time TEXT
)''')
conn.commit()

# Load known faces
known_faces = []
known_names = []

for file in os.listdir("images"):
    image = face_recognition.load_image_file(f"images/{file}")
    encoding = face_recognition.face_encodings(image)[0]
    known_faces.append(encoding)
    known_names.append(os.path.splitext(file)[0])  # student name from file name

# Attendance tracking
marked = []

# GUI
def start_recognition():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
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

                if name not in marked:
                    marked.append(name)
                    time_now = datetime.now().strftime("%H:%M:%S")
                    cursor.execute("INSERT INTO attendance (name, time) VALUES (?, ?)", (name, time_now))
                    conn.commit()
                    messagebox.showinfo("Attendance Marked", f"{name} marked present at {time_now}")

        cv2.imshow('Attendance System', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Build simple GUI
root = tk.Tk()
root.title("PDPU Attendance System")

tk.Label(root, text="Face Recognition Attendance", font=("Helvetica", 18)).pack(pady=10)
tk.Button(root, text="Start Attendance", command=start_recognition, font=("Helvetica", 14)).pack(pady=20)
tk.Label(root, text="Press 'q' to stop camera", font=("Helvetica", 10)).pack()

root.mainloop()
