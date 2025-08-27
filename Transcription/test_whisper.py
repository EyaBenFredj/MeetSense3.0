# Transcription/test_whisper.py
import re
from pathlib import Path
import whisper

from core.acronyms import expander  # once-and-for-all expansion

# --- Regex for classic A-Z acronyms (kept) ---
_ARABIC_BLOCK = "\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF"
ACRONYM_REGEX = rf"(?<![0-9A-Za-z_{_ARABIC_BLOCK}])[A-Z0-9]{{2,8}}(?![0-9A-Za-z_{_ARABIC_BLOCK}])"


# ---------------------------
# Arabic letter-name handling
# ---------------------------

# Single-token collapsed forms Whisper often produces
# e.g. "سبي" ~= "إس بي" (SP), "ريم" ~= "آر إم" (RM)
COLLAPSED_TOKEN_MAP = {
    "سبي": "SP",
    "ريم": "RM",
}

# Multi-token patterns → acronym
# (Keep it small & precise to avoid false positives in Tunisian Arabic)
PATTERNS = [
    (("دي", "دي"), "DD"),
    (("اس", "بي"), "SP"), (("إس", "بي"), "SP"),
    (("سي", "ار", "ام"), "CRM"), (("سي", "آر", "ام"), "CRM"),
    (("ار", "ام"), "RM"), (("آر", "ام"), "RM"),
    (("ام", "تي"), "MT"), (("ايم", "تي"), "MT"),
    (("كيو", "اي"), "QA"), (("كْيو", "اي"), "QA"),  # QA (Quality Assurance)
]

# Arabic spellings of Latin letter names (very conservative list)
LETTER_NAME_MAP = {
    "اي": "A", "آي": "I", "إي": "E",
    "بي": "B",
    "سي": "C",
    "دي": "D",
    "اف": "F", "إف": "F",
    "جي": "G",
    "اتش": "H", "إتش": "H",
    "كي": "K",
    "ام": "M", "ايم": "M",
    "ان": "N", "إن": "N", "اين": "N",
    "او": "O", "أو": "O",
    "كيو": "Q",
    "ار": "R", "آر": "R",
    "اس": "S", "إس": "S", "س": "S",   # sometimes Whisper drops the alif
    "تي": "T",
    "يو": "U",
    "في": "V",
    "اكس": "X", "إكس": "X",
    "واي": "Y",
    "زد": "Z", "زين": "Z", "زي": "Z",
}

PUNCT_RX = re.compile(r"^[\W_]+|[\W_]+$")


def _strip_punct(tok: str):
    """Return (core, left_punct, right_punct)."""
    left = ""
    right = ""
    m = re.match(r"^[\W_]+", tok)
    if m:
        left = m.group(0)
        tok = tok[len(left):]
    m = re.search(r"[\W_]+$", tok)
    if m:
        right = m.group(0)
        tok = tok[:-len(right)]
    return tok, left, right


def normalize_ar_letter_names_to_acronyms(text: str) -> str:
    """
    Convert sequences like:
      'دي دي سبي' → 'DD SP'
      'ايم تي'   → 'MT'
      'كيو اي'   → 'QA'
      'سي ريم'   → 'CRM' (via 'سي' + 'ريم'→'RM')
    and also map any run of Arabic letter names (length>=2) to an acronym.
    """
    if not text:
        return text

    words = text.split()
    out = []
    i = 0
    n = len(words)

    while i < n:
        raw = words[i]
        core, left_p, right_p = _strip_punct(raw)

        # 1) collapsed one-token (e.g., "سبي", "ريم")
        if core in COLLAPSED_TOKEN_MAP:
            out.append(left_p + COLLAPSED_TOKEN_MAP[core] + right_p)
            i += 1
            continue

        # 2) multi-token patterns (try longest first)
        matched = False
        for pat, acro in PATTERNS:
            mlen = len(pat)
            if i + mlen <= n:
                window = [ _strip_punct(w)[0] for w in words[i:i+mlen] ]
                if tuple(window) == pat:
                    out.append(acro)
                    i += mlen
                    matched = True
                    break
        if matched:
            continue

        # 3) generic run of Arabic letter names → acronym (length >= 2)
        j = i
        letters = []
        while j < n:
            w_core = _strip_punct(words[j])[0]
            if w_core in LETTER_NAME_MAP:
                letters.append(LETTER_NAME_MAP[w_core])
                j += 1
            else:
                break
        if len(letters) >= 2:
            out.append("".join(letters))
            i = j
            continue

        # 4) default: keep as-is
        out.append(words[i])
        i += 1

    return " ".join(out)


# ---------------------------
# Classic helpers
# ---------------------------

def find_raw_acronyms(text: str):
    return sorted(set(re.findall(ACRONYM_REGEX, text))) if text else []


def transcribe_audio(audio_path: str) -> str:
    """
    Use Whisper; large-v2 handles mixed Arabic/French/English better.
    If you prefer your older model, change 'large-v2' to what you used.
    """
    model = whisper.load_model("large-v2")
    result = model.transcribe(audio_path, language=None, fp16=False)
    return result.get("text", "").strip()


def main():
    audio_path = input(r'Enter the path to your audio file (e.g. MP3/WAV/M4A): ').strip('"').strip()
    if not Path(audio_path).exists():
        print(f"❌ File not found: {audio_path}")
        return

    print("🔊 Transcribing audio with Whisper (large-v2, multilingual)…")
    transcript = transcribe_audio(audio_path)

    print("\n📝 Transcript (raw):\n")
    print(transcript or "(empty)")

    # --- Normalize Arabic letter-names to real acronyms ---
    normalized = normalize_ar_letter_names_to_acronyms(transcript)

    # --- Detect acronyms after normalization ---
    found = find_raw_acronyms(normalized)
    print("\n🔎 Acronyms spotted:", found if found else "none")

    # --- Expand acronyms once-and-for-all ---
    expanded = expander.expand(normalized)
    print("\n🧩 Transcript (acronyms expanded):\n")
    print(expanded or "(empty)")

    # Save if you want
    with open("whisper_transcript.txt", "w", encoding="utf-8") as f:
        f.write(expanded)

    print("\n✅ Saved to 'whisper_transcript.txt'")


if __name__ == "__main__":
    main()
