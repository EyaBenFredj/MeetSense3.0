# Interface/storage.py
from __future__ import annotations

import os
import re
import sqlite3
from datetime import datetime
from typing import Optional, List

import streamlit as st
from sqlalchemy import create_engine, select, String, DateTime, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


# ---------- Setup ----------
HERE = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(HERE)
DB_PATH = os.getenv("MEETSENSE_DB", os.path.join(PROJECT_ROOT, "data", "meetings.db"))
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


# ---------- Models ----------
class Base(DeclarativeBase):
    pass


class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    tags: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    audio_path: Mapped[Optional[str]] = mapped_column(String(1024))
    transcript_path: Mapped[Optional[str]] = mapped_column(String(1024))
    transcript_text: Mapped[Optional[str]] = mapped_column(Text)
    summary: Mapped[Optional[str]] = mapped_column(Text)
    key_points: Mapped[Optional[str]] = mapped_column(Text)
    action_items: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[Optional[str]] = mapped_column(String(50), default="UNUSED", index=True)
    department: Mapped[Optional[str]] = mapped_column(String(120), index=True)
    owner: Mapped[Optional[str]] = mapped_column(String(120), index=True)


# ---------- DB Init ----------
engine = create_engine(f"sqlite:///{DB_PATH}", future=True)
Base.metadata.create_all(engine)


def _ensure_columns() -> None:
    """
    Add new columns without migrations (dev-friendly). Idempotent.
    """
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("PRAGMA table_info(meetings)")
        existing = {row[1] for row in cur.fetchall()}

        wanted = [
            ("status", "TEXT", "'UNUSED'"),
            ("department", "TEXT", "NULL"),
            ("owner", "TEXT", "NULL"),
        ]
        for name, typ, default in wanted:
            if name not in existing:
                cur.execute(f"ALTER TABLE meetings ADD COLUMN {name} {typ} DEFAULT {default}")
        con.commit()


_ensure_columns()


# ---------- Functions ----------
def upsert_meeting(**fields) -> Meeting:
    # Ensure a datetime object for occurred_at if a string is passed
    if "occurred_at" in fields and isinstance(fields["occurred_at"], str):
        # Accepts "YYYY-MM-DD HH:MM" or "YYYY-MM-DD"
        s = fields["occurred_at"].strip()
        try:
            fields["occurred_at"] = datetime.fromisoformat(s)
        except ValueError:
            # Try tolerant parse: keep only digits, dashes, colons and spaces
            s2 = re.sub(r"[^\d\-\:\sT]", "", s).replace("T", " ")
            fields["occurred_at"] = datetime.fromisoformat(s2)

    with Session(engine) as s:
        m = Meeting(**fields)
        s.add(m)
        s.commit()
        s.refresh(m)
        return m


def update_meeting(meeting_id: int, **fields) -> Meeting:
    if "occurred_at" in fields and isinstance(fields["occurred_at"], str):
        fields["occurred_at"] = datetime.fromisoformat(fields["occurred_at"])

    with Session(engine) as s:
        m = s.get(Meeting, meeting_id)
        if not m:
            raise ValueError(f"Meeting {meeting_id} not found")

        for k, v in fields.items():
            if hasattr(m, k):
                setattr(m, k, v)

        s.commit()
        s.refresh(m)
        return m


def list_meetings(
    name_query: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    tag_query: Optional[str] = None,
    department: Optional[str] = None,
    status: Optional[str] = None,
    owner: Optional[str] = None,
) -> List[Meeting]:
    with Session(engine) as s:
        meetings = s.execute(select(Meeting)).scalars().all()

    def match(m: Meeting) -> bool:
        return all(
            [
                (name_query.lower() in m.name.lower()) if name_query else True,
                (tag_query.lower() in (m.tags or "").lower()) if tag_query else True,
                (department.lower() in (m.department or "").lower()) if department else True,
                (status.lower() == (m.status or "").lower()) if status else True,
                (owner.lower() in (m.owner or "").lower()) if owner else True,
                (m.occurred_at >= date_from) if date_from else True,
                (m.occurred_at <= date_to) if date_to else True,
            ]
        )

    return [m for m in meetings if match(m)]


def get_meeting(meeting_id: int) -> Optional[Meeting]:
    with Session(engine) as s:
        return s.get(Meeting, meeting_id)


# ---------- Streamlit Page ----------
def render():
    st.header("📦 Storage / Meetings")

    # --- Filters ---
    with st.expander("Filters", expanded=True):
        c1, c2, c3 = st.columns(3)
        name_query = c1.text_input("Name contains")
        tag_query = c2.text_input("Tags contain")
        owner = c3.text_input("Owner contains")

        c4, c5, c6 = st.columns(3)
        department = c4.text_input("Department contains")
        status = c5.selectbox("Status", ["", "UNUSED", "DRAFT", "READY", "ARCHIVED"])
        date_from = c6.date_input("From date", value=None)

        c7, _, _ = st.columns(3)
        date_to = c7.date_input("To date", value=None)

        def to_dt(d):
            return datetime.combine(d, datetime.min.time()) if d else None

        results = list_meetings(
            name_query=name_query or None,
            tag_query=tag_query or None,
            owner=owner or None,
            department=department or None,
            status=(status or None),
            date_from=to_dt(date_from),
            date_to=to_dt(date_to),
        )

    # --- Table ---
    if results:
        import pandas as pd

        df = pd.DataFrame(
            [
                {
                    "ID": m.id,
                    "Name": m.name,
                    "Tags": m.tags,
                    "Occurred At": m.occurred_at,
                    "Owner": m.owner,
                    "Department": m.department,
                    "Status": m.status,
                    "Audio": m.audio_path,
                    "Transcript": m.transcript_path,
                }
                for m in results
            ]
        ).sort_values("Occurred At", ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No meetings found. Add one below.")

    st.markdown("---")

    # --- Add new meeting ---
    st.subheader("➕ Add Meeting")
    with st.form("add_meeting"):
        n1, n2 = st.columns([2, 1])
        name = n1.text_input("Name")
        occurred_at = n2.text_input("Occurred at (YYYY-MM-DD HH:MM)", value=datetime.now().strftime("%Y-%m-%d %H:%M"))
        tags = st.text_input("Tags (comma-separated)")
        owner = st.text_input("Owner")
        department = st.text_input("Department")
        audio_path = st.text_input("Audio path")
        transcript_path = st.text_input("Transcript path")
        transcript_text = st.text_area("Transcript text", height=120)
        submitted = st.form_submit_button("Save")

    if submitted:
        if not name.strip():
            st.warning("Name is required.")
        else:
            m = upsert_meeting(
                name=name.strip(),
                tags=tags.strip() or None,
                occurred_at=occurred_at.strip(),
                audio_path=audio_path.strip() or None,
                transcript_path=transcript_path.strip() or None,
                transcript_text=transcript_text.strip() or None,
                # optional fields default to None
                owner=owner.strip() or None,
                department=department.strip() or None,
                status="DRAFT",
            )
            st.success(f"Saved meeting #{m.id}: {m.name}")
            st.rerun()
