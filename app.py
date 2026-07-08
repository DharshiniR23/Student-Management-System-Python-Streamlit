"""
Student Management System
--------------------------
A beginner-friendly web app built with Streamlit + Pandas + CSV storage.

Run with:  streamlit run app.py
"""

import os
import re
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# CONFIG / CONSTANTS
# ---------------------------------------------------------------------------

CSV_FILE = "students.csv"                     # our simple "database"
COLUMNS = ["Student_ID", "Student_Name", "Department", "Email", "Phone", "Marks"]

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide",
)


# ---------------------------------------------------------------------------
# DATA HELPER FUNCTIONS
# ---------------------------------------------------------------------------

def load_data() -> pd.DataFrame:
    """
    Load student records from the CSV file.
    If the file doesn't exist (or is empty/corrupt), create a fresh empty one.
    """
    if not os.path.exists(CSV_FILE):
        # File missing -> create an empty CSV with the correct headers
        empty_df = pd.DataFrame(columns=COLUMNS)
        empty_df.to_csv(CSV_FILE, index=False)
        return empty_df

    try:
        df = pd.read_csv(CSV_FILE, dtype={"Student_ID": str, "Phone": str})
        # Make sure all expected columns exist even if the file was edited manually
        for col in COLUMNS:
            if col not in df.columns:
                df[col] = ""
        return df[COLUMNS]
    except pd.errors.EmptyDataError:
        # File exists but is completely empty
        return pd.DataFrame(columns=COLUMNS)
    except Exception as e:
        st.error(f"⚠️ Could not read {CSV_FILE}: {e}")
        return pd.DataFrame(columns=COLUMNS)


def save_data(df: pd.DataFrame) -> None:
    """Save the given DataFrame back to the CSV file."""
    df.to_csv(CSV_FILE, index=False)


def is_valid_email(email: str) -> bool:
    """Very simple email format check."""
    pattern = r"^[\w\.\-]+@[\w\-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def is_valid_phone(phone: str) -> bool:
    """Phone number should be 7-15 digits (allows leading +)."""
    pattern = r"^\+?\d{7,15}$"
    return re.match(pattern, phone) is not None


# ---------------------------------------------------------------------------
# PAGE 1: HOME
# ---------------------------------------------------------------------------

def show_home():
    st.title("🎓 Student Management System")
    st.markdown(
        """
        Welcome! This simple web app lets you **add, view, search, update,
        delete, and analyze** student records — all stored in a CSV file.

        Use the **sidebar menu** on the left to navigate between modules.
        """
    )

    df = load_data()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", len(df))

    if not df.empty and df["Marks"].astype(str).str.strip().ne("").any():
        marks_numeric = pd.to_numeric(df["Marks"], errors="coerce")
        col2.metric("Average Marks", f"{marks_numeric.mean():.2f}")
        col3.metric("Highest Marks", f"{marks_numeric.max():.0f}")
    else:
        col2.metric("Average Marks", "N/A")
        col3.metric("Highest Marks", "N/A")

    st.divider()
    st.subheader("📋 Quick Preview")
    if df.empty:
        st.info("No student records yet. Go to **Add Student** to create one!")
    else:
        st.dataframe(df.head(5), use_container_width=True)


# ---------------------------------------------------------------------------
# PAGE 2: ADD STUDENT
# ---------------------------------------------------------------------------

def show_add_student():
    st.title("➕ Add Student")
    df = load_data()

    with st.form("add_student_form", clear_on_submit=True):
        student_id = st.text_input("Student ID *")
        student_name = st.text_input("Student Name *")
        department = st.text_input("Department *")
        email = st.text_input("Email Address *")
        phone = st.text_input("Phone Number *")
        marks = st.number_input("Marks *", min_value=0.0, max_value=100.0, step=0.5)

        submitted = st.form_submit_button("Add Student")

    if submitted:
        # ---- Validation ----
        errors = []
        if not student_id.strip():
            errors.append("Student ID cannot be empty.")
        elif student_id.strip() in df["Student_ID"].astype(str).values:
            errors.append("Student ID already exists. Please use a unique ID.")

        if not student_name.strip():
            errors.append("Student Name cannot be empty.")
        if not department.strip():
            errors.append("Department cannot be empty.")
        if not is_valid_email(email.strip()):
            errors.append("Please enter a valid email address.")
        if not is_valid_phone(phone.strip()):
            errors.append("Please enter a valid phone number (7-15 digits).")

        if errors:
            for e in errors:
                st.error(e)
        else:
            # ---- Save new record ----
            new_row = pd.DataFrame([{
                "Student_ID": student_id.strip(),
                "Student_Name": student_name.strip(),
                "Department": department.strip(),
                "Email": email.strip(),
                "Phone": phone.strip(),
                "Marks": marks,
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success(f"✅ Student '{student_name}' added successfully!")


# ---------------------------------------------------------------------------
# PAGE 3: VIEW STUDENTS
# ---------------------------------------------------------------------------

def show_view_students():
    st.title("📋 View Students")
    df = load_data()

    if df.empty:
        st.info("No student records found. Add a student first.")
        return

    st.dataframe(df, use_container_width=True)
    st.caption(f"Total records: {len(df)}")


# ---------------------------------------------------------------------------
# PAGE 4: SEARCH STUDENT
# ---------------------------------------------------------------------------

def show_search_student():
    st.title("🔍 Search Student")
    df = load_data()

    if df.empty:
        st.info("No student records found. Add a student first.")
        return

    search_type = st.radio("Search by:", ["Student ID", "Student Name"], horizontal=True)
    query = st.text_input("Enter search value").strip()

    if st.button("Search") and query:
        if search_type == "Student ID":
            results = df[df["Student_ID"].astype(str).str.lower() == query.lower()]
        else:
            results = df[df["Student_Name"].astype(str).str.lower().str.contains(query.lower())]

        if results.empty:
            st.warning("No matching student found.")
        else:
            st.success(f"Found {len(results)} matching record(s):")
            st.dataframe(results, use_container_width=True)


# ---------------------------------------------------------------------------
# PAGE 5: UPDATE STUDENT
# ---------------------------------------------------------------------------

def show_update_student():
    st.title("✏️ Update Student")
    df = load_data()

    if df.empty:
        st.info("No student records found. Add a student first.")
        return

    student_ids = df["Student_ID"].astype(str).tolist()
    selected_id = st.selectbox("Select Student ID to update", student_ids)

    if selected_id:
        record = df[df["Student_ID"].astype(str) == selected_id].iloc[0]

        st.write(f"**Student Name:** {record['Student_Name']}  (name cannot be changed here)")

        with st.form("update_student_form"):
            department = st.text_input("Department", value=str(record["Department"]))
            email = st.text_input("Email Address", value=str(record["Email"]))
            phone = st.text_input("Phone Number", value=str(record["Phone"]))
            marks = st.number_input(
                "Marks", min_value=0.0, max_value=100.0, step=0.5,
                value=float(record["Marks"]) if str(record["Marks"]).strip() != "" else 0.0
            )
            submitted = st.form_submit_button("Save Changes")

        if submitted:
            errors = []
            if not department.strip():
                errors.append("Department cannot be empty.")
            if not is_valid_email(email.strip()):
                errors.append("Please enter a valid email address.")
            if not is_valid_phone(phone.strip()):
                errors.append("Please enter a valid phone number (7-15 digits).")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                idx = df[df["Student_ID"].astype(str) == selected_id].index[0]
                df.loc[idx, "Department"] = department.strip()
                df.loc[idx, "Email"] = email.strip()
                df.loc[idx, "Phone"] = phone.strip()
                df.loc[idx, "Marks"] = marks
                save_data(df)
                st.success(f"✅ Record for Student ID '{selected_id}' updated successfully!")


# ---------------------------------------------------------------------------
# PAGE 6: DELETE STUDENT
# ---------------------------------------------------------------------------

def show_delete_student():
    st.title("🗑️ Delete Student")
    df = load_data()

    if df.empty:
        st.info("No student records found. Add a student first.")
        return

    student_ids = df["Student_ID"].astype(str).tolist()
    selected_id = st.selectbox("Select Student ID to delete", student_ids)

    if selected_id:
        record = df[df["Student_ID"].astype(str) == selected_id].iloc[0]
        st.warning(
            f"You are about to delete: **{record['Student_Name']}** "
            f"(ID: {selected_id}, Dept: {record['Department']})"
        )

        confirm = st.checkbox("I confirm I want to delete this record.")
        if st.button("Delete Student", type="primary", disabled=not confirm):
            df = df[df["Student_ID"].astype(str) != selected_id]
            save_data(df)
            st.success(f"✅ Student ID '{selected_id}' deleted successfully!")
            st.rerun()


# ---------------------------------------------------------------------------
# PAGE 7: DASHBOARD ANALYTICS + PAGE 8: VISUALIZATION (combined page)
# ---------------------------------------------------------------------------

def show_dashboard():
    st.title("📊 Dashboard & Analytics")
    df = load_data()

    if df.empty:
        st.info("No student records found. Add students to see analytics.")
        return

    marks_numeric = pd.to_numeric(df["Marks"], errors="coerce")

    # ---- Key metrics ----
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", len(df))
    col2.metric("Average Marks", f"{marks_numeric.mean():.2f}" if marks_numeric.notna().any() else "N/A")
    col3.metric("Highest Marks", f"{marks_numeric.max():.0f}" if marks_numeric.notna().any() else "N/A")
    col4.metric("Departments", df["Department"].nunique())

    st.divider()

    # ---- Department-wise student count ----
    st.subheader("🏫 Department-wise Student Count")
    dept_counts = df["Department"].value_counts()
    st.bar_chart(dept_counts)

    # ---- Student marks chart ----
    st.subheader("📈 Student Marks")
    marks_chart_df = df[["Student_Name", "Marks"]].copy()
    marks_chart_df["Marks"] = pd.to_numeric(marks_chart_df["Marks"], errors="coerce")
    marks_chart_df = marks_chart_df.set_index("Student_Name")
    st.bar_chart(marks_chart_df)

    st.divider()
    st.subheader("📋 Department Summary Table")
    st.dataframe(dept_counts.rename_axis("Department").reset_index(name="Student Count"),
                 use_container_width=True)


# ---------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------------------------

def main():
    st.sidebar.title("🎓 Navigation")
    menu = st.sidebar.radio(
        "Go to",
        [
            "Home",
            "Add Student",
            "View Students",
            "Search Student",
            "Update Student",
            "Delete Student",
            "Dashboard & Analytics",
        ],
    )

    st.sidebar.divider()
    st.sidebar.caption("Student Management System · Built with Streamlit & Pandas")

    # ---- Route to the selected page ----
    if menu == "Home":
        show_home()
    elif menu == "Add Student":
        show_add_student()
    elif menu == "View Students":
        show_view_students()
    elif menu == "Search Student":
        show_search_student()
    elif menu == "Update Student":
        show_update_student()
    elif menu == "Delete Student":
        show_delete_student()
    elif menu == "Dashboard & Analytics":
        show_dashboard()


if __name__ == "__main__":
    main()
