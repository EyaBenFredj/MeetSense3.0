# Interface/knowledge.py
from __future__ import annotations
from typing import List
import re
import streamlit as st


# ---------- NLP helpers ----------
def extract_key_points(transcript: str) -> List[str]:
    """Return structured key points based on bullet/colon/symbol cues."""
    sents = re.split(r"[\n\.!?]+", transcript)
    points = [
        s.strip()
        for s in sents
        if any(sym in s for sym in (":", "-", "•")) and len(s.strip()) > 8
    ]
    return points[:10] or [s.strip() for s in sents if s.strip()][:5]


def extract_action_items(transcript: str) -> List[str]:
    """Identify tasks, responsibilities, and follow-ups (very naive rules)."""
    sents = re.split(r"[\n\.!?]+", transcript)
    cues = (
        "action", "todo", "follow up", "follow-up", "assign",
        "deadline", "next step", "will", "task", "owner"
    )
    actions = [s.strip() for s in sents if any(c in s.lower() for c in cues)]
    return actions[:10]


def summarize_transcript(transcript: str) -> str:
    """Simple summary using the beginning and end of the transcript."""
    sents = [s.strip() for s in re.split(r"[\n\.!?]+", transcript) if s.strip()]
    if not sents:
        return ""
    first = " ".join(sents[:3]).strip()
    last = " ".join(sents[-3:]).strip()
    return (first + "\n\n...\n\n" + last).strip()


# ---------- Page entry point ----------
def render():
    st.header("🧠 Knowledge")
    st.write("Paste a transcript to extract key points, action items, and a quick summary.")

    # Input area
    transcript = st.text_area("Transcript", height=200, placeholder="Paste meeting transcript here...")

    col_run, col_clear = st.columns([1, 1])
    run_clicked = col_run.button("Analyze")
    clear_clicked = col_clear.button("Clear")

    if clear_clicked:
        st.experimental_rerun()

    if run_clicked:
        if not transcript.strip():
            st.warning("Please paste a transcript first.")
            return

        with st.spinner("Analyzing…"):
            points = extract_key_points(transcript)
            actions = extract_action_items(transcript)
            summary = summarize_transcript(transcript)

        # Results
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Key Points")
            if points:
                for p in points:
                    st.markdown(f"- {p}")
            else:
                st.info("No key points detected.")

        with c2:
            st.subheader("Action Items")
            if actions:
                for a in actions:
                    st.markdown(f"- [ ] {a}")
            else:
                st.info("No action items detected.")

        st.subheader("Summary")
        if summary:
            st.write(summary)
        else:
            st.info("Summary is empty.")
