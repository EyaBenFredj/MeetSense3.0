# Interface/asr.py
from __future__ import annotations

import os
import sys
import time
from typing import Generator, Optional

import streamlit as st

# --- Paths (keep your layout: Transcription/ lives at project root) ---
HERE = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(HERE)
sys.path.append(PROJECT_ROOT)  # allow importing Transcription/*

UPLOAD_DIR = os.path.join(PROJECT_ROOT, "data", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------------- Core ASR helpers ----------------
def simulate_stream(text: str, delay: float = 0.02) -> Generator[str, None, None]:
    """Fake a live transcription stream by yielding words gradually."""
    for word in text.split():
        yield word + " "
        time.sleep(delay)


def _try_local_stream(filepath: str, language: Optional[str]) -> Optional[Generator[str, None, None]]:
    """
    Try custom transcription modules inside Transcription/ directory.

    Expected (optional) modules:
      - Transcription.stream_transcribe.stream_transcribe(filepath, language=None) -> Generator[str, None, None]
      - Transcription.test_whisper.main(filepath) -> str
    """
    # 1) Custom streaming implementation
    try:
        from Transcription.stream_transcribe import stream_transcribe  # type: ignore
        return stream_transcribe(filepath, language=language)
    except Exception:
        pass

    # 2) Simple Whisper test script (returns full text)
    try:
        from Transcription.test_whisper import main as whisper_main  # type: ignore
        text = whisper_main(filepath)
        return simulate_stream(text)
    except Exception:
        return None


def transcribe_stream(filepath: str, language: Optional[str] = None) -> Generator[str, None, None]:
    """
    Transcribe audio via:
    1) Local stream_transcribe (if available)
    2) faster-whisper (if available)
    3) openai/whisper (if available)
    4) last-resort simulated stream (error message)
    """
    # 1) Project-local streaming
    local = _try_local_stream(filepath, language)
    if local:
        yield from local
        return

    # 2) faster-whisper
    try:
        from faster_whisper import WhisperModel  # type: ignore

        model_size = os.getenv("WHISPER_MODEL", "base")
        # compute_type is flexible (int8/int8_float16/float16), int8 is CPU friendly
        model = WhisperModel(model_size, compute_type=os.getenv("WHISPER_COMPUTE", "int8"))
        segments, _ = model.transcribe(
            filepath,
            language=language,
            word_timestamps=True,
            vad_filter=True,
        )
        for seg in segments:
            if getattr(seg, "words", None):
                for w in seg.words:
                    # faster-whisper Word has .word
                    yield getattr(w, "word", "") + " "
            else:
                # fallback if words missing
                for w in (seg.text or "").split():
                    yield w + " "
        return
    except Exception as e:
        print("⚠️ faster-whisper failed:", e)

    # 3) openai/whisper (pip install -U openai-whisper)
    try:
        import whisper  # type: ignore

        model_size = os.getenv("WHISPER_MODEL", "base")
        model = whisper.load_model(model_size)
        result = model.transcribe(filepath, language=language)
        text = result.get("text", "")
        yield from simulate_stream(text)
        return
    except Exception as e:
        print("⚠️ whisper failed:", e)

    # 4) Last resort
    yield from simulate_stream("⚠️ ASR failed. Please install faster-whisper or openai-whisper, or add Transcription/ modules.")


# ---------------- Streamlit Page ----------------
def render():
    st.header("🎙️ New Meeting — Live Transcription")

    st.write("Choose an audio file (upload or local path) and start transcription. "
             "If `Transcription/` helpers are present, they’ll be used; otherwise we'll try `faster-whisper` then `whisper`.")

    # --- Input source ---
    source_tab, settings_tab = st.tabs(["Audio", "Settings"])

    with source_tab:
        up = st.file_uploader(
            "Upload audio file",
            type=["wav", "mp3", "m4a", "mp4", "webm", "ogg"],
            accept_multiple_files=False,
        )
        st.markdown("**OR**")
        local_path = st.text_input("Local audio path (absolute or relative to project root)")

    with settings_tab:
        lang = st.text_input("Language (ISO code, optional)", value="", placeholder="e.g., en, fr, de, ar")
        lang = lang.strip() or None
        model_hint = os.getenv("WHISPER_MODEL", "base")
        st.caption(f"Model hint via `WHISPER_MODEL` env var (current: `{model_hint}`)")

    # --- Resolve file path ---
    audio_path: Optional[str] = None
    if up is not None:
        # Save uploaded file to data/uploads
        safe_name = os.path.basename(up.name)
        dest = os.path.join(UPLOAD_DIR, safe_name)
        with open(dest, "wb") as f:
            f.write(up.getbuffer())
        audio_path = dest
        st.success(f"Uploaded to: `{dest}`")
    elif local_path.strip():
        # Allow relative to project root
        p = local_path.strip()
        audio_path = p if os.path.isabs(p) else os.path.join(PROJECT_ROOT, p)
        if not os.path.exists(audio_path):
            st.error(f"File not found: `{audio_path}`")
            audio_path = None

    # --- Controls ---
    col1, col2 = st.columns([1, 1])
    start = col1.button("▶️ Start Transcription", use_container_width=True, disabled=audio_path is None)
    clear = col2.button("🧹 Clear", use_container_width=True)

    if clear:
        st.rerun()

    # --- Live output ---
    out = st.empty()
    final_box = st.empty()

    if start:
        if not audio_path:
            st.warning("Please provide an audio file (upload or local path).")
            return

        running_text = ""
        with st.spinner("Transcribing…"):
            try:
                for token in transcribe_stream(audio_path, language=lang):
                    running_text += token
                    # Update UI progressively
                    out.markdown(f"**Live Transcript**\n\n{running_text}")
                # Finalize
                final_box.text_area("Final Transcript", running_text.strip(), height=240)
                # Download button
                st.download_button(
                    "💾 Download transcript.txt",
                    data=running_text.strip().encode("utf-8"),
                    file_name="transcript.txt",
                    mime="text/plain",
                )
                st.success("Transcription complete.")
            except Exception as e:
                st.error(f"Transcription error: {e}")
