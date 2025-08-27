# process_transcript.py
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import List
import spacy

try:
    import torch
except Exception:
    torch = None

try:
    import accelerate
    HAS_ACCELERATE = True
except Exception:
    HAS_ACCELERATE = False

from langdetect import detect
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import spacy
from tools.acronym_seed import ACRONYMS

TRANSLATION_MODEL = "facebook/nllb-200-distilled-600M"
SUMMARIZATION_MODEL = "csebuetnlp/mT5_multilingual_XLSum"

ACRONYM_DICT = {item["short"].upper(): item["long"] for item in ACRONYMS}


# === ACRONYM EXPANSION ===

import re

def expand_acronyms(text: str, acronyms: dict) -> str:
    # Match acronyms that might be next to Arabic or punctuation without spaces
    for short, long in acronyms.items():
        # Add Arabic-aware boundaries using positive lookbehind and lookahead
        pattern = re.compile(rf"(?<!\w)({re.escape(short)})(?!\w)", re.IGNORECASE)
        matches = pattern.findall(text)
        for match in matches:
            print(f"[DEBUG] Expanding {match} → {long}")
        text = pattern.sub(long, text)
    return text


# === I/O ===
def read_transcript(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Transcript not found at: {p.resolve()}")
    return p.read_text(encoding="utf-8")


def chunk_text(text: str, max_chars: int = 2000) -> List[str]:
    if not text.strip():
        return []
    sents = re.split(r"(?<=[\.!\?。！？])\s+", text.strip())
    chunks, cur = [], ""
    for s in sents:
        if len(cur) + len(s) + 1 <= max_chars:
            cur = (cur + " " + s).strip()
        else:
            if cur:
                chunks.append(cur)
            cur = s
    if cur:
        chunks.append(cur)
    return chunks


def pick_device_index() -> int:
    if torch is not None and getattr(torch, "cuda", None) and torch.cuda.is_available():
        return 0
    return -1


# === MODELS ===
def make_translator():
    tok = AutoTokenizer.from_pretrained(TRANSLATION_MODEL)
    try:
        tok.tgt_lang = "fra_Latn"
    except Exception:
        pass
    if HAS_ACCELERATE:
        mdl = AutoModelForSeq2SeqLM.from_pretrained(TRANSLATION_MODEL, device_map="auto", torch_dtype="auto")
        return pipeline("translation", model=mdl, tokenizer=tok, src_lang="eng_Latn", tgt_lang="fra_Latn")
    else:
        mdl = AutoModelForSeq2SeqLM.from_pretrained(TRANSLATION_MODEL)
        device_index = pick_device_index()
        if device_index >= 0:
            mdl.to(f"cuda:{device_index}")
        return pipeline("translation", model=mdl, tokenizer=tok, device=device_index, src_lang="eng_Latn", tgt_lang="fra_Latn")


def make_summarizer():
    tok = AutoTokenizer.from_pretrained(SUMMARIZATION_MODEL)
    if HAS_ACCELERATE:
        mdl = AutoModelForSeq2SeqLM.from_pretrained(SUMMARIZATION_MODEL, device_map="auto", torch_dtype="auto")
        return pipeline("summarization", model=mdl, tokenizer=tok)
    else:
        mdl = AutoModelForSeq2SeqLM.from_pretrained(SUMMARIZATION_MODEL)
        device_index = pick_device_index()
        if device_index >= 0:
            mdl.to(f"cuda:{device_index}")
        return pipeline("summarization", model=mdl, tokenizer=tok, device=device_index)


# === TRANSLATION (WORD-BY-WORD) ===
def detect_and_translate_mixed_text(text: str, translator) -> str:
    nlp = spacy.load("xx_ent_wiki_sm")
    doc = nlp(text)
    tokens = []
    for token in doc:
        word = token.text.strip()
        if not word:
            continue
        try:
            lang = detect(word)
        except Exception:
            lang = "unknown"
        tokens.append((word, lang))

    to_translate = [word for word, lang in tokens if lang != "fr"]
    if not to_translate:
        return text

    translations = translator(to_translate, batch_size=8, truncation=True, max_new_tokens=20)
    translated_iter = iter([t["translation_text"] for t in translations])

    result = []
    for word, lang in tokens:
        if lang == "fr":
            result.append(word)
        else:
            result.append(next(translated_iter))
    return " ".join(result)


# === SUMMARIZATION & BULLETS ===
def summarize_text(summarizer, text: str) -> str:
    parts = chunk_text(text, max_chars=2000)
    if not parts:
        return ""
    summaries = []
    for part in parts:
        res = summarizer(part, truncation=True, max_new_tokens=160, min_length=50, do_sample=False)
        summaries.append(res[0]["summary_text"])
    combined = " ".join(summaries)
    if len(parts) > 1:
        res = summarizer(combined, truncation=True, max_new_tokens=180, min_length=60, do_sample=False)
        return res[0]["summary_text"]
    return combined


def extract_bullets_from_summary(summary_fr: str) -> str:
    if not summary_fr.strip():
        return ""
    sents = re.split(r"(?<=[\.!\?。！？])\s+", summary_fr.strip())
    seen, bullets = set(), []
    for s in (s.strip(" \n-") for s in sents if s.strip()):
        if s not in seen:
            seen.add(s)
            if not re.search(r"[\.!\?。！？]$", s):
                s += "."
            bullets.append(f"- {s}")
    return "\n".join(bullets)


# === MAIN ===
def main():
    parser = argparse.ArgumentParser(description="Translate multilingual transcript to French, summarize, and extract bullets.")
    parser.add_argument("--in", dest="in_path", default="whisper_transcript.txt", help="Path to input transcript (UTF-8).")
    args = parser.parse_args()

    # === STEP 1: Read original transcript ===
    transcript = read_transcript(args.in_path)
    print("\n📝 ORIGINAL TRANSCRIPT:\n")
    print(transcript)

    # === STEP 2: Expand acronyms ===
    transcript_expanded = expand_acronyms(transcript, ACRONYM_DICT)
    print("\n🔠 EXPANDED TRANSCRIPT (Acronyms Replaced):\n")
    print(transcript_expanded)

    # === STEP 3: Translate to French ===
    print("\n🌍 Translating mixed-language transcript to French...")
    translator = make_translator()
    french = detect_and_translate_mixed_text(transcript_expanded, translator)
    print("\n🇫🇷 TRANSLATED TO FRENCH:\n")
    print(french)

    # === STEP 4: Summarize ===
    print("\n✂️ Summarizing...")
    summarizer = make_summarizer()
    summary = summarize_text(summarizer, french)
    print("\n🧾 SUMMARY:\n")
    print(summary)

    # === STEP 5: Extract bullet points ===
    print("\n📌 Bullet points extracted from summary:\n")
    bullets = extract_bullets_from_summary(summary)
    print(bullets)

    print("\n✅ Done. Comparison complete.")


if __name__ == "__main__":
    main()
