import streamlit as st

# ---- Imports from your current structure ----
from Interface.auth import login_user
# Create these modules' render() functions as shown below
from Interface.knowledge import render as render_knowledge
from Interface.storage import render as render_storage
from Interface.asr import render as render_new_meeting
# You can add more pages later (Calendar, Transcripts, Analytics) the same way

# ---- App config ----
st.set_page_config(page_title="MeetSense", layout="wide")
st.title("🤖 MeetSense")

# ---- Authentication (once) ----
if "user" not in st.session_state:
    user = login_user()
    if not user:
        st.stop()
    st.session_state.user = user
    st.success(f"✅ Logged in as {user['username']}")

# ---- Sidebar navigation (single tab, no external links) ----
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3039/3039432.png", width=60)
st.sidebar.title("📋 Navigation")

PAGES = {
    "🏠 Home": "home",
    "📅 Calendar": "calendar",
    "🧠 Knowledge": "knowledge",
    "📄 Transcripts": "transcripts",
    "📊 Analytics": "analytics",
    "🎙️ New Meeting": "new_meeting",
}

choice = st.sidebar.radio("Go to", list(PAGES.keys()))
st.sidebar.markdown("---")
st.sidebar.markdown(f"👤 `{st.session_state.user['username']}`")

page = PAGES[choice]

# ---- Router ----
if page == "home":
    st.header("Home")
    st.write("Welcome to MeetSense.")

elif page == "calendar":
    st.header("Calendar")
    st.info("TODO: implement Calendar page.")

elif page == "knowledge":
    render_knowledge()   # from Interface/knowledge.py

elif page == "transcripts":
    st.header("Transcripts")
    st.info("TODO: implement Transcripts page.")

elif page == "analytics":
    st.header("Analytics")
    st.info("TODO: implement Analytics page.")

elif page == "new_meeting":
    render_new_meeting()  # from Interface/asr.py
