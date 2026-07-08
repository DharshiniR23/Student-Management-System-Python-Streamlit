# 🎓 Student Management System

A simple, beginner-friendly **web application** to manage student records, built with:

- **Python**
- **Streamlit** — web application framework
- **Pandas** — data handling
- **CSV file** — lightweight data storage (`students.csv`)

---

## ✨ Features

| Module | Description |
|---|---|
| 🏠 Home | Dashboard title, description, and total student count |
| ➕ Add Student | Form to add a new student (ID, Name, Department, Email, Phone, Marks) with input validation |
| 📋 View Students | View all student records in a table |
| 🔍 Search Student | Search by Student ID or Student Name |
| ✏️ Update Student | Edit Department, Email, Phone Number, and Marks |
| 🗑️ Delete Student | Remove a student record (with confirmation) |
| 📊 Dashboard & Analytics | Total students, average/highest marks, department-wise counts |
| 📈 Data Visualization | Department-wise bar chart and student marks chart |

---

## 📂 Folder Structure

```
Student-Management-System/
│
├── app.py              # Main Streamlit application
├── students.csv         # CSV data storage (auto-created if missing)
├── requirements.txt     # Python dependencies
├── README.md             # Project documentation
└── screenshots/          # App screenshots
```

---

## 🚀 Getting Started

### 1. Clone / download the project
Make sure all files (`app.py`, `students.csv`, `requirements.txt`) are in the same folder.

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 🗃️ Data Storage

Student records are stored in `students.csv` with the following columns:

| Column | Description |
|---|---|
| Student_ID | Unique identifier for each student |
| Student_Name | Full name of the student |
| Department | Student's department |
| Email | Email address |
| Phone | Phone number |
| Marks | Marks scored (0-100) |

> If `students.csv` is missing, the app automatically creates a new empty one with the correct headers — no manual setup needed.

---

## ✅ Input Validation

- Student ID must be unique and not empty.
- Student Name and Department cannot be empty.
- Email must be in a valid format (e.g., `name@example.com`).
- Phone number must be 7–15 digits (optionally starting with `+`).
- Marks must be between 0 and 100.

---

## 🛠️ Tech Notes

- Built entirely with **Streamlit** widgets — no HTML/CSS/JS needed.
- Uses **Pandas** DataFrames to read, filter, update, and write CSV data.
- Charts are rendered using Streamlit's built-in `st.bar_chart`.
- Sidebar radio menu provides simple navigation between modules.

---

## 📸 Screenshots

Add your application screenshots to the `screenshots/` folder and reference them here, e.g.:

```markdown
![Home Page](screenshots/home.png)
![Add Student](screenshots/add_student.png)
```

---

## 📄 License

This project is free to use for learning purposes.
