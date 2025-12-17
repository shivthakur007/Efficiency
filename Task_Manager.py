import streamlit as st
import os

st.title("🔐 Personal Task Manager")

# ---------- LOGIN ----------
if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    username = st.text_input("Enter your username")
    if st.button("Login"):
        if username.strip():
            st.session_state.user = username.strip().lower()
            st.rerun()
        else:
            st.warning("Username cannot be empty")
    st.stop()

# ---------- USER FILE ----------
FILE_NAME = f"tasks_{st.session_state.user}.txt"

def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

def save_tasks(tasks):
    with open(FILE_NAME, "w") as f:
        for task in tasks:
            f.write(task + "\n")

if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

st.success(f"Logged in as: {st.session_state.user}")

# ---------- SHOW TASKS ----------
st.subheader("📝 Your Tasks")

if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks, 1):
        st.write(f"{i}. {task}")
else:
    st.info("No tasks yet")

# ---------- ADD TASK ----------
st.subheader("➕ Add Task")
new_task = st.text_input("Task")

if st.button("Add Task"):
    if new_task:
        st.session_state.tasks.append(new_task)
        save_tasks(st.session_state.tasks)
        st.rerun()
    else:
        st.warning("Task cannot be empty")

# ---------- REMOVE TASK ----------
if st.session_state.tasks:
    st.subheader("❌ Remove Task")
    index = st.selectbox(
        "Select task number",
        range(1, len(st.session_state.tasks) + 1)
    )

    if st.button("Remove Task"):
        removed = st.session_state.tasks.pop(index - 1)
        save_tasks(st.session_state.tasks)
        st.success(f"Removed: {removed}")
        st.rerun()

# ---------- LOGOUT ----------
if st.button("Logout"):
    st.session_state.clear()
    st.rerun()
