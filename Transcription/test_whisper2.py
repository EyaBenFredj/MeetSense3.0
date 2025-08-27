import re
from pathlib import Path
import whisper
from core.acronyms import expander  # imports expand() with acronym definitions

# --- Regex for classic A-Z acronyms (kept) ---
_ARABIC_BLOCK = "\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF"
ACRONYM_REGEX = rf"(?<![0-9A-Za-z_{_ARABIC_BLOCK}])[A-Z0-9]{{2,8}}(?![0-9A-Za-z_{_ARABIC_BLOCK}])"

# --- Collapsed one-token acronym forms ---
COLLAPSED_TOKEN_MAP = {
    "سبي": "SP",
    "ريم": "RM",
}

# --- Multi-token patterns for Arabic letter names ---
PATTERNS = [
    (("دي", "دي"), "DD"),
    (("اس", "بي"), "SP"), (("إس", "بي"), "SP"),
    (("سي", "ار", "ام"), "CRM"), (("سي", "آر", "ام"), "CRM"),
    (("ار", "ام"), "RM"), (("آر", "ام"), "RM"),
    (("ام", "تي"), "MT"), (("ايم", "تي"), "MT"),
    (("كيو", "اي"), "QA"), (("كْيو", "اي"), "QA"),
]

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
    "اس": "S", "إس": "S", "س": "S",
    "تي": "T",
    "يو": "U",
    "في": "V",
    "اكس": "X", "إكس": "X",
    "واي": "Y",
    "زد": "Z", "زين": "Z", "زي": "Z",
}

PUNCT_RX = re.compile(r"^[\W_]+|[\W_]+$")


def _strip_punct(tok: str):
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
    if not text:
        return text

    words = text.split()
    out = []
    i = 0
    n = len(words)

    while i < n:
        raw = words[i]
        core, left_p, right_p = _strip_punct(raw)

        # collapsed single token
        if core in COLLAPSED_TOKEN_MAP:
            out.append(left_p + COLLAPSED_TOKEN_MAP[core] + right_p)
            i += 1
            continue

        # pattern matching
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

        # generic sequence of letter names
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

        out.append(words[i])
        i += 1

    return " ".join(out)


def find_raw_acronyms(text: str):
    return sorted(set(re.findall(ACRONYM_REGEX, text))) if text else []


def transcribe_audio(audio_path: str) -> str:
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

    normalized = normalize_ar_letter_names_to_acronyms(transcript)
    found = find_raw_acronyms(normalized)

    print("\n🔎 Acronyms spotted:", found if found else "none")

    expanded = expander.expand(normalized)

    print("\n🧩 Transcript (acronyms expanded):\n")
    print(expanded or "(empty)")

    with open("whisper_transcript.txt", "w", encoding="utf-8") as f:
        f.write(expanded)

    print("\n✅ Saved to 'whisper_transcript.txt'")


if __name__ == "__main__":
    main()
