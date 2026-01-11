import streamlit as st
import os
import hashlib
import pickle
from datetime import datetime


# ------------------ CONFIG ------------------
st.set_page_config(page_title="Personal Task Manager", page_icon="📅")
SCOPES = ["https://www.googleapis.com/auth/calendar"]
USERS_FILE = "users.txt"

# ------------------ SECURITY ------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    users = {}
    with open(USERS_FILE, "r") as f:
        for line in f:
            user, pwd = line.strip().split(",")
            users[user] = pwd
    return users

def save_user(username, password):
    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{hash_password(password)}\n")

# ------------------ GOOGLE CALENDAR ------------------
def get_calendar_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("calendar", "v3", credentials=creds)

def add_event_to_calendar(task, due_date):
    service = get_calendar_service()
    event = {
        "summary": task,
        "start": {"date": due_date},
        "end": {"date": due_date},
    }
    service.events().insert(calendarId="primary", body=event).execute()

# ------------------ SESSION ------------------
users = load_users()
if "user" not in st.session_state:
    st.session_state.user = None

# ------------------ LOGIN / REGISTER ------------------
st.title("🔐 Personal Task Manager")

if st.session_state.user is None:
    st.subheader("Login / Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            if username in users and users[username] == hash_password(password):
                st.session_state.user = username
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password")

    with col2:
        if st.button("Register"):
            if username in users:
                st.warning("User already exists")
            elif username and password:
                save_user(username, password)
                st.success("User registered! Please login.")
            else:
                st.warning("Username & password required")

    st.stop()

# ------------------ TASK FILE ------------------
TASK_FILE = f"tasks_{st.session_state.user}.txt"

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        for task in tasks:
            f.write(task + "\n")

if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

# ------------------ DASHBOARD ------------------
st.success(f"Logged in as: {st.session_state.user}")

st.subheader("📝 Your Tasks")
if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks, 1):
        st.write(f"{i}. {task}")
else:
    st.info("No tasks yet")

# ------------------ ADD TASK ------------------
st.subheader("➕ Add Task")

task_name = st.text_input("Task")
due_date = st.date_input("Due Date")
sync_calendar = st.checkbox("📅 Add to Google Calendar")

if st.button("Add Task"):
    if task_name:
        task_entry = f"{task_name} | {due_date}"
        st.session_state.tasks.append(task_entry)
        save_tasks(st.session_state.tasks)

        if sync_calendar:
            add_event_to_calendar(task_name, due_date.strftime("%Y-%m-%d"))
            st.success("Task added to Google Calendar")

        st.rerun()
    else:
        st.warning("Task cannot be empty")

# ------------------ REMOVE TASK ------------------
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

# ------------------ LOGOUT ------------------
if st.button("Logout"):
    st.session_state.clear()
    st.rerun()
