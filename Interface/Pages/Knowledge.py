import streamlit as st
from Interface.storage import list_meetings
import pandas as pd

st.markdown("## 🧠 Extracted Meeting Knowledge")

view = st.radio("View format:", ["Cards", "Table", "Board"])

meetings = list_meetings()

if view == "Cards":
    for m in meetings:
        st.markdown(f"""
        ### 📝 {m.name}
        - 🏢 Department: {m.department or '-'}
        - 👤 Owner: {m.owner or '-'}
        - 📅 Date: {m.occurred_at.date().isoformat()}
        - 🔖 Tags: {m.tags or '-'}
        - 🧩 Status: {m.status or 'UNUSED'}
        """)
elif view == "Table":
    df = pd.DataFrame([{
        "ID": m.id,
        "Name": m.name,
        "Owner": m.owner,
        "Department": m.department,
        "Tags": m.tags,
        "Status": m.status,
        "Date": m.occurred_at.date().isoformat()
    } for m in meetings])
    st.dataframe(df)
else:
    statuses = ["UNUSED", "SPENT", "DELAYED", "SURPLUS"]
    for s in statuses:
        st.markdown(f"### 📌 {s}")
        for m in [x for x in meetings if (x.status or "").upper() == s]:
            st.markdown(f"- {m.name} | {m.owner or '-'}")
