import whisperx
import torch
import re
from pathlib import Path
from core.acronyms import expander

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def transcribe_with_whisperx(audio_path: str):
    model = whisperx.load_model("large-v2", DEVICE)
    print("🔊 Transcribing with WhisperX...")

    result = model.transcribe(audio_path)
    print("📦 Alignment model loading...")
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=DEVICE)
    aligned = whisperx.align(result["segments"], model_a, metadata, audio_path, device=DEVICE)

    return aligned["word_segments"]


def join_words_by_script(words):
    out = []
    for word in words:
        text = word["text"]
        lang = detect_script(text)
        out.append((text, lang))
    return out


def detect_script(word: str) -> str:
    # Very rough heuristic
    if re.search(r"[\u0600-\u06FF]", word):
        return "ar"
    if re.search(r"[A-Za-z]", word):
        return "lat"
    return "other"


def expand_acronyms_in_words(words_with_lang):
    expanded = []
    seen = set()
    for word, lang in words_with_lang:
        if lang == "lat" and word.upper() in expander.reg:
            short = word.upper()
            long = expander.reg[short]
            if short in seen:
                expanded.append(long)
            else:
                expanded.append(f"{long} ({short})")
                seen.add(short)
        else:
            expanded.append(word)
    return " ".join(expanded)


def main():
    audio_path = input("📂 Enter path to audio file: ").strip('"').strip()
    if not Path(audio_path).exists():
        print(f"❌ File not found: {audio_path}")
        return

    words = transcribe_with_whisperx(audio_path)
    words_lang = join_words_by_script(words)

    print("\n🌐 Language-aware words:\n")
    print(" ".join(w for w, _ in words_lang))

    expanded = expand_acronyms_in_words(words_lang)

    print("\n🧩 Final Output with Acronym Expansion:\n")
    print(expanded)

    Path("whisperx_transcript.txt").write_text(expanded, encoding="utf-8")
    print("\n✅ Saved to whisperx_transcript.txt")


if __name__ == "__main__":
    main()
