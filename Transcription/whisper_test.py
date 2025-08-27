import re
from pathlib import Path
import whisper
from core.acronyms import expander
from langdetect import detect
from translit_me.transliterator import transliterate as tr

_ARABIC_RE = re.compile(r"[\u0600-\u06FF]")

def is_arabic_script(word: str) -> bool:
    return bool(_ARABIC_RE.search(word))

def main():
    audio_path = input("Enter audio path: ").strip('"').strip()
    if not Path(audio_path).exists():
        print("File not found"); return

    model = whisper.load_model("medium")
    print("Detecting language...")
    lang = model.transcribe(audio_path, language=None, fp16=False)["language"]

    print(f"Transcribing as detected language: {lang}")
    result = model.transcribe(audio_path, language=lang, fp16=False)
    transcript = result["text"]
    words = transcript.split()

    processed = []
    seen_acros = set()
    for w in words:
        if is_arabic_script(w):
            det = detect(w)
            if det["lang"] in ("fr","en"):
                w = tr([w], "ar", "en")[0]  # transliterate to Latin
        else:
            key = w.upper()
            if key in expander.reg:
                if key not in seen_acros:
                    w = f"{expander.reg[key]} ({key})"
                    seen_acros.add(key)
                else:
                    w = expander.reg[key]
        processed.append(w)

    final = " ".join(processed)
    print("\nFinal Transcript:\n", final)
    Path("whisper_transcript.txt").write_text(final, encoding="utf-8")
    print("Saved to whisper_transcript.txt")
if __name__ == "__main__":
    main()
