




# 👤 Face Recognition-Based Attendance System (DBMS Project)

A **Face Recognition Attendance System** built using Python, OpenCV, Tkinter, and MySQL. This project automates the attendance process by recognizing faces in real-time and recording attendance into a database, eliminating the need for manual roll calls.

---

## 📌 Features

- 🎥 Real-time face detection & recognition using OpenCV
- 📂 Student registration with photo capture
- 🕵️‍♂️ Face data training with LBPH algorithm
- 🧾 Attendance logging with date and time
- 🗃️ Attendance records stored in MySQL database
- 🖼️ GUI built using Tkinter
- 📋 Export attendance to CSV

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| `Python`   | Core language |
| `OpenCV`   | Face detection and recognition |
| `Tkinter`  | GUI development |
| `MySQL`    | Backend database |
| `PIL`      | Image processing |
| `CSV`      | Export attendance reports |

---

## 🖥️ Screenshots

<!-- > *(You can add screenshots here in Markdown format once available)* -->

---

## 🚀 How to Run

### 1. Clone the Repo

```bash
git clone https://github.com/chetangadhiya4939/Fork_dbms_project_face_attendance.git
cd Fork_dbms_project_face_attendance
````

### 2. Install Dependencies

Make sure you have Python 3.7+ installed.

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is missing, manually install:

```bash
pip install opencv-python pillow mysql-connector-python
```

### 3. Setup MySQL Database

* Open your MySQL client
* Create a database:

```sql
CREATE DATABASE face_recognition;
```

* Update database credentials in `student.py` and `attendance.py` (if hardcoded).

### 4. Run the App

```bash
python main.py
```

---

## 🧠 Modules Overview

| Module                | Description                                  |
| --------------------- | -------------------------------------------- |
| `main.py`             | Entry point GUI                              |
| `student.py`          | Student registration                         |
| `train.py`            | Train face recognizer                        |
| `face_recognition.py` | Real-time recognition and attendance marking |
| `attendance.py`       | Manage and export attendance records         |
| `database.py`         | Connects to MySQL DB                         |

---

## 📁 Project Structure

```
├── dataset/              # Captured face images
├── attendance/           # Attendance CSVs
├── trainer/              # Trained model file
├── icons/                # GUI Icons
├── main.py               # Main GUI file
├── student.py            # Student data input
├── face_recognition.py   # Face recognition module
├── train.py              # Model training
└── database.py           # MySQL connectivity
```

---

## ✅ To-Do / Improvements

* [ ] Add face mask detection
* [ ] Improve GUI design
* [ ] Implement email notification
* [ ] Dockerize the app

---

## 🤝 Contributors

* [Chetan Gadhiya](https://github.com/chetangadhiya4939)
* [Vedesh Pandya](https://github.com/VedeshP)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🌟 Star This Repo

If you found this project helpful or interesting, please consider giving it a ⭐️ to support the work!




