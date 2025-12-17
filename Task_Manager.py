st.title("🔐 Personal Task Manager")

USERS_FILE = "users.txt"

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

users = load_users()

if "user" not in st.session_state:
    st.session_state.user = None

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
                st.success("User registered! You can now log in.")
            else:
                st.warning("Username & password required")

    st.stop()