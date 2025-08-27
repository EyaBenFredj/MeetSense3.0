import streamlit as st
import sqlite3
import hashlib

DB_PATH = "users.db"

def _get_conn():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            is_admin BOOLEAN DEFAULT 0
        )
    """)
    con.commit()
    return con

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def register_user(username: str, password: str, is_admin=False) -> bool:
    con = _get_conn()
    try:
        con.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                    (username, hash_pw(password), is_admin))
        con.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate(username: str, password: str):
    con = _get_conn()
    cur = con.cursor()
    cur.execute("SELECT id, is_admin FROM users WHERE username=? AND password=?",
                (username, hash_pw(password)))
    row = cur.fetchone()
    if row:
        return {"user_id": row[0], "username": username, "is_admin": bool(row[1])}
    return None

def login_user():
    st.subheader("🔐 Login / Sign Up")
    mode = st.radio("Choose mode:", ["Login", "Sign Up"], horizontal=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    go = st.button("Submit")

    if go:
        if not username or not password:
            st.warning("Please enter all fields.")
            return None

        if mode == "Login":
            user = authenticate(username, password)
            if user:
                return user
            else:
                st.error("❌ Invalid credentials.")
        else:
            success = register_user(username, password)
            if success:
                st.success("✅ Registered! Please log in.")
            else:
                st.error("Username already exists.")
    return None
