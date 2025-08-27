import streamlit as st
from datetime import datetime
from Interface.asr import transcribe_stream
from Interface.knowledge import summarize_transcript, extract_key_points, extract_action_items
from Interface.storage import upsert_meeting, update_meeting
import os

st.markdown("## 🎙️ Upload or Record New Meeting")

name = st.text_input("Meeting name")
tags = st.text_input("Tags (comma separated)")
dept = st.text_input("Department")
owner = st.text_input("Owner")
status = st.selectbox("Status", ["UNUSED", "SPENT", "DELAYED", "SURPLUS"])
audio = st.file_uploader("Upload audio file", type=["mp3", "wav", "m4a"])
lang = st.selectbox("Language", ["", "en", "fr", "de", "es", "ar"])

if st.button("Start Transcription"):
    if not audio:
        st.warning("Please upload an audio file.")
    else:
        audio_path = os.path.join("data/audio", audio.name)
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)
        with open(audio_path, "wb") as f:
            f.write(audio.read())

        mtg = upsert_meeting(
            name=name or "Untitled",
            occurred_at=datetime.now(),
            tags=tags,
            department=dept,
            owner=owner,
            status=status,
            audio_path=audio_path,
            transcript_text=""
        )

        transcript = ""
        with st.spinner("Transcribing..."):
            for chunk in transcribe_stream(audio_path, lang if lang else None):
                transcript += chunk
                st.text_area("Live Transcript", value=transcript, height=200)

        summary = summarize_transcript(transcript)
        actions = "\n".join(extract_action_items(transcript))
        keys = "\n".join(extract_key_points(transcript))

        update_meeting(mtg.id, transcript_text=transcript, summary=summary, key_points=keys, action_items=actions)

        st.success("✅ Transcription saved.")
