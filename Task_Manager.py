import streamlit as st
import os

FILE_NAME = "tasks.txt"

# Load tasks
def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

# Save tasks
def save_tasks(tasks):
    with open(FILE_NAME, "w") as f:
        for task in tasks:
            f.write(task + "\n")

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

st.title("📝 Task Manager")

# Show tasks
st.subheader("Your Tasks")
if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks, 1):
        st.write(f"{i}. {task}")
else:
    st.info("No tasks added yet.")

# Add task
st.subheader("Add a Task")
new_task = st.text_input("Enter task")
if st.button("Add Task"):
    if new_task:
        st.session_state.tasks.append(new_task)
        save_tasks(st.session_state.tasks)
        st.success("Task added!")
        st.rerun()
    else:
        st.warning("Task cannot be empty.")

# Remove task
st.subheader("Remove a Task")
if st.session_state.tasks:
    task_to_remove = st.selectbox(
        "Select task to remove",
        range(1, len(st.session_state.tasks) + 1)
    )

    if st.button("Remove Task"):
        removed = st.session_state.tasks.pop(task_to_remove - 1)
        save_tasks(st.session_state.tasks)
        st.success(f"Removed: {removed}")
        st.rerun()
