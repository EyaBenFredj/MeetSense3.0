import streamlit as st
from Interface.storage import get_meeting

st.markdown("## 📄 Load Transcript by Meeting ID")

mid = st.number_input("Enter Meeting ID", step=1, format="%d")

if st.button("Load"):
    m = get_meeting(mid)
    if not m:
        st.error("❌ Meeting not found.")
    else:
        st.text_area("Transcript", value=m.transcript_text or "", height=200)
        st.text_area("Summary", value=m.summary or "", height=120)
        st.text_area("Key Points", value=m.key_points or "", height=100)
        st.text_area("Action Items", value=m.action_items or "", height=100)
