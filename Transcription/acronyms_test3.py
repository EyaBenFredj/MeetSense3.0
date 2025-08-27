import re
from pathlib import Path
import whisper
from core.acronyms import expander  # ✅ Uses your singleton AcronymExpander

# --- One-token forms Whisper might collapse (e.g. "سبي" = "SP")
COLLAPSED_TOKEN_MAP = {
    "سبي": "SP",
    "ريم": "RM",
}

# --- Multi-token Arabic spoken letter patterns (very conservative)
PATTERNS = [
    (("دي", "دي"), "DD"),
    (("اس", "بي"), "SP"), (("إس", "بي"), "SP"),
    (("سي", "ار", "ام"), "CRM"), (("سي", "آر", "ام"), "CRM"),
    (("ار", "ام"), "RM"), (("آر", "ام"), "RM"),
    (("ام", "تي"), "MT"), (("ايم", "تي"), "MT"),
    (("كيو", "اي"), "QA"), (("كْيو", "اي"), "QA"),
]

def _strip_punct(tok: str):
    left = right = ""
    m = re.match(r"^[\W_]+", tok)
    if m:
        left = m.group(0)
        tok = tok[len(left):]
    m = re.search(r"[\W_]+$", tok)
    if m:
        right = m.group(0)
        tok = tok[:-len(right)]
    return tok, left, right

def normalize_known_acronyms(text: str) -> str:
    if not text:
        return text

    words = text.split()
    out = []
    i = 0
    n = len(words)

    while i < n:
        raw = words[i]
        core, left_p, right_p = _strip_punct(raw)

        # 1) Collapsed tokens
        if core in COLLAPSED_TOKEN_MAP:
            out.append(left_p + COLLAPSED_TOKEN_MAP[core] + right_p)
            i += 1
            continue

        # 2) Multi-token matches
        matched = False
        for pat, acro in PATTERNS:
            mlen = len(pat)
            if i + mlen <= n:
                window = [_strip_punct(w)[0] for w in words[i:i + mlen]]
                if tuple(window) == pat:
                    out.append(acro)
                    i += mlen
                    matched = True
                    break
        if matched:
            continue

        # 3) Leave as-is
        out.append(words[i])
        i += 1

    return " ".join(out)

def transcribe_audio(audio_path: str) -> str:
    model = whisper.load_model("large-v2")

    # ✅ Force transcription using French — no Arabic spellings of French words
    result = model.transcribe(
        audio_path,
        language="ar",        # Force Latin spelling of French (e.g. société, test)
        task="transcribe",    # Use "translate" if you want pure English
        fp16=False
    )

    return result.get("text", "").strip()

def main():
    audio_path = input(r'📂 Enter the path to your audio file (e.g. MP3/WAV/M4A): ').strip('"').strip()
    if not Path(audio_path).exists():
        print(f"❌ File not found: {audio_path}")
        return

    print("🔊 Transcribing with Whisper (large-v2)…")
    transcript = transcribe_audio(audio_path)

    print("\n📝 Raw Transcript:\n")
    print(transcript or "(empty)")

    # Normalize any Arabic spellings of acronyms
    normalized = normalize_known_acronyms(transcript)

    # Expand acronyms using JSON-based registry
    expanded = expander.expand(normalized)

    print("\n🧠 Normalized & Expanded Transcript:\n")
    print(expanded or "(empty)")

    output_file = "whisper_transcript.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(expanded)

    print(f"\n✅ Saved to '{output_file}'")

if __name__ == "__main__":
    main()
