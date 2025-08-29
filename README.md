# 🧠 MeetSense : AI Meeting Assistant
**Multilingual AI-powered tool for meeting transcription and knowledge retrieval (Tunisian dialect, French, English).**

This project provides:
- 🎙️ **Accurate meeting transcription** using OpenAI Whisper & Faster-Whisper  
- 🌍 **Multilingual processing** (Tunisian dialect, Arabic script, French, English)  
- 🔤 **Smart acronym expansion** & transliteration of Arabic-script words  
- 📚 **Knowledge base search** over saved transcripts  
- 👤 **User management system** (login, signup, transcript storage)  
- 💻 **Web interfaces** with Streamlit & Gradio  

---

## 🚀 Features
- Upload audio in multiple formats (`.mp3`, `.wav`, `.m4a`, `.mp4`)
- Automatic **language detection**
- Handles **Tunisian dialect**, Arabic, French, and English seamlessly
- Expands **acronyms** automatically (via `core.acronyms.expander`)
- **Transliterates Arabic-script words** into Latin script where necessary
- **Noise reduction** & audio preprocessing for clearer transcription
- Secure **user accounts** with personal transcript history
- Integrated **search engine** for knowledge retrieval across meetings

---
## 📂 Project Structure
```
MeetSense3.0/
│
├── .venv/                         # Virtual environment
├── .env                           # Environment variables (API keys, configs)
├── .gitignore                     # Git ignored files
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
│
├── app.py                         # Main Streamlit application
├── pipeline.py                    # Central transcription pipeline orchestration
├── whisper_transcript.txt         # Example transcript output
├── temp_Enregistrement.m4a        # Sample audio recording
├── users.db                       # SQLite database for users & transcripts
│
├── whisper_streaming/              # Whisper streaming tests & modules
│
├── Transcription/                  # Speech-to-text & processing modules
│   ├── record_voice.py             # Record audio from microphone
│   ├── preprocess_audio.py         # Preprocess & denoise audio
│   ├── transcribe_audio.py         # Core Whisper/Faster-Whisper transcription
│   ├── process_transcript.py       # Acronym expansion & transliteration
│   ├── punctuate.py                # Restores punctuation in transcripts
│   ├── stream_transcribe.py        # Streaming transcription logic
│   ├── run_pipeline.py             # Runs full transcription pipeline
│   ├── run_pipeline2.py            # Alternative pipeline runner
│   ├── test_whisper.py             # Test script for Whisper
│   ├── test_whisper2.py
│   ├── test_whisper3.py
│   ├── bullet_points.txt           # Example bullet point summary
│   ├── expanded_transcript.txt     # Transcript with acronyms expanded
│   ├── original_transcript.txt     # Raw transcript output
│   ├── transcript.txt              # Processed transcript
│   ├── translated_french.txt       # Transcript translated into French
│   ├── summary.txt                 # Example transcript summary
│   ├── whisper_transcript.txt      # Whisper-generated transcript
│   └── my_voice.wav                # Example input audio file
│
├── Knowledge Extraction & Retrieval/ # Semantic + keyword transcript search
│   └── (Modules for retrieval & knowledge indexing)
│
├── PostProcessing & Summarization/ # Transcript summarization modules
│   └── summarize.py                # Generates abstractive meeting summaries
│
├── scripts/
│   └── build_acronym_registry.py   # Builds acronym registry for expansion
│
├── tools/
│   └── acronym_seed.py             # Initial acronym seeds for registry
│
├── acronym_index/                  # Vector store for acronyms
│   ├── index_builder.py            # Builds acronym vector index
│   ├── default_vector_store.json   # Default embedding store
│   ├── docstore.json               # Document storage
│   ├── graph_store.json            # Graph relationships between acronyms
│   ├── image_vector_store.json     # (Future) embeddings for images
│   └── index_store.json            # Finalized index structure
│
├── core/
│   └── acronyms.py                 # Acronym expansion logic
│
├── app/
│   └── chat_chain.py               # Conversational pipeline for Q&A
│
├── data/                           # User data & transcripts
│   ├── audio/                      # Uploaded audio files
│   ├── transcripts/                # Saved transcripts per user
│   ├── uploads/                    # Temporary upload files
│   ├── acronyms.json               # Acronym dictionary
│   ├── meetings.db                 # Meeting metadata database
│   └── users.json                  # User authentication data
│
├── Interface/
│   ├── Pages/                      # Streamlit modular pages
│   │   ├── __init__.py
│   │   ├── asr.py                  # Automatic Speech Recognition page
│   │   ├── auth.py                 # Login & signup page
│   │   ├── knowledge.py            # Knowledge base search page
│   │   └── storage.py              # Transcript storage & management
```
Perfect ✅ — thanks for the clarification. What you want is a **complete documentation pack**:

1. **Main README.md** (for the whole project: description, installation, structure, workflows, models, problems, roadmap, etc.).
2. **Sub-README files** (inside key folders like `Transcription/`, `PostProcessing & Summarization/`, `Knowledge Extraction & Retrieval/`, etc.) to explain those modules individually.

I’ll generate them for you in **ready-to-paste Markdown**.

---

# 📜 Main Project README (`README.md`)

```markdown
# 🧠 MeetSense 3.0
**Multilingual AI Assistant for Meeting Transcription, Knowledge Extraction, and Summarization**

MeetSense 3.0 is an end-to-end AI-powered tool that:
- 🎙️ Transcribes **multilingual meeting audio** (Tunisian dialect, French, English)
- 🔤 Handles **script mixing** with **acronym expansion** and **transliteration**
- 📚 Builds a **knowledge base** from transcripts with search & retrieval
- 📝 Summarizes meetings into concise notes
- 🌐 Provides **CLI tools**, **Streamlit UI**, and **API endpoints**

---

## 🚀 Features
- Upload audio in **mp3, wav, m4a, mp4**
- **Automatic language detection** (Arabic / Tunisian dialect / French / English)
- **Noise reduction** & audio preprocessing
- **Whisper + Faster-Whisper** for transcription
- **Transliteration** of mixed-script Arabic words
- **Acronym expansion** on first use
- **Knowledge retrieval** with hybrid (keyword + semantic embedding) search
- **Summarization** into bullet points or paragraphs
- **User management** with account system (JSON/SQLite)
- **Web UI (Streamlit)** and **command-line interface**

---

## 📂 Project Structure

```

MeetSense3.0/
│
├── .venv/                         # Virtual environment
├── .env                           # Environment variables (API keys, configs)
├── .gitignore                     # Git ignored files
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
│
├── app.py                         # Main Streamlit application
├── app\_int.py                     # CLI/Intermediate application
├── pipeline.py                    # Central transcription pipeline orchestration
├── whisper\_transcript.txt         # Example transcript output
├── temp\_Enregistrement.m4a        # Sample audio recording
├── users.db                       # SQLite database for users & transcripts
│
├── whisper\_streaming/              # Whisper streaming tests & modules
│
├── Transcription/                  # Speech-to-text & processing modules
│   ├── record\_voice.py             # Record audio from microphone
│   ├── preprocess\_audio.py         # Preprocess & denoise audio
│   ├── transcribe\_audio.py         # Core Whisper/Faster-Whisper transcription
│   ├── process\_transcript.py       # Acronym expansion & transliteration
│   ├── punctuate.py                # Restores punctuation in transcripts
│   ├── stream\_transcribe.py        # Streaming transcription logic
│   ├── run\_pipeline.py             # Runs full transcription pipeline
│   ├── run\_pipeline2.py            # Alternative pipeline runner
│   ├── test\_whisper.py             # Test script for Whisper
│   ├── test\_whisper2.py
│   ├── test\_whisper3.py
│   ├── bullet\_points.txt           # Example bullet point summary
│   ├── expanded\_transcript.txt     # Transcript with acronyms expanded
│   ├── original\_transcript.txt     # Raw transcript output
│   ├── transcript.txt              # Processed transcript
│   ├── translated\_french.txt       # Transcript translated into French
│   ├── summary.txt                 # Example transcript summary
│   ├── whisper\_transcript.txt      # Whisper-generated transcript
│   └── my\_voice.wav                # Example input audio file
│
├── Knowledge Extraction & Retrieval/ # Semantic + keyword transcript search
│   └── (Modules for retrieval & knowledge indexing)
│
├── PostProcessing & Summarization/ # Transcript summarization modules
│   └── summarize.py                # Generates abstractive meeting summaries
│
├── scripts/
│   └── build\_acronym\_registry.py   # Builds acronym registry for expansion
│
├── tools/
│   └── acronym\_seed.py             # Initial acronym seeds for registry
│
├── acronym\_index/                  # Vector store for acronyms
│   ├── index\_builder.py            # Builds acronym vector index
│   ├── default\_vector\_store.json   # Default embedding store
│   ├── docstore.json               # Document storage
│   ├── graph\_store.json            # Graph relationships between acronyms
│   ├── image\_vector\_store.json     # (Future) embeddings for images
│   └── index\_store.json            # Finalized index structure
│
├── core/
│   └── acronyms.py                 # Acronym expansion logic
│
├── app/
│   └── chat\_chain.py               # Conversational pipeline for Q\&A
│
├── data/                           # User data & transcripts
│   ├── audio/                      # Uploaded audio files
│   ├── transcripts/                # Saved transcripts per user
│   ├── uploads/                    # Temporary upload files
│   ├── acronyms.json               # Acronym dictionary
│   ├── meetings.db                 # Meeting metadata database
│   └── users.json                  # User authentication data
│
├── Interface/
│   ├── Pages/                      # Streamlit modular pages
│   │   ├── **init**.py
│   │   ├── asr.py                  # Automatic Speech Recognition page
│   │   ├── auth.py                 # Login & signup page
│   │   ├── knowledge.py            # Knowledge base search page
│   │   └── storage.py              # Transcript storage & management

````

---

## 📦 Installation

1. Clone the repo:
```bash
git clone https://github.com/your-repo/MeetSense3.0.git
cd MeetSense3.0
````

2. Create virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🧩 Dependencies

* **flask** – API endpoints (future expansion)
* **vosk** – optional offline transcription
* **sounddevice, scipy, numpy, pydub, librosa, soundfile, noisereduce** – audio preprocessing
* **whisper, faster-whisper** – multilingual transcription
* **torch, torchaudio** – deep learning backend
* **transformers, spacy** – NLP pipeline
* **langdetect, translit-me** – language detection & transliteration
* **llama-index** – semantic knowledge retrieval
* **sqlalchemy** – structured storage
* **gradio, streamlit** – interfaces (demo + full app)

---

## ⚙️ Workflow

1. **Audio Input**
   User records/upload audio → stored in `/data/audio/`

2. **Preprocessing**

   * Noise reduction (`noisereduce`, `pydub`)
   * Resampling & normalization (`librosa`, `soundfile`)

3. **Transcription**

   * Whisper/Faster-Whisper transcribes
   * Language auto-detected (Arabic, French, English)

4. **Post-Processing**

   * Acronym expansion (`core/acronyms.py`)
   * Script detection & transliteration (`translit-me`)
   * Punctuation restoration

5. **Knowledge Management**

   * Transcript saved to `/data/transcripts/<user>/`
   * Indexed into `Knowledge Extraction & Retrieval`

6. **Search & Summarization**

   * Keyword + semantic search (LLaMA-Index)
   * Summarization (`summarize.py`, `bullet_points.py`)

7. **User Management**

   * Users stored in `users.json` or `users.db`
   * Each has personal transcripts

---

## 🧠 Models & LLMs

* **Whisper/Faster-Whisper**: Transcription (Tunisian dialect + French + English)
* **SpaCy/Transformers**: Text tokenization, NER
* **Langdetect + Translit-me**: Language detection + transliteration
* **LLaMA-Index**: Semantic knowledge base
* **Custom Acronym Index**: Consistent acronym handling

---

## 🏗️ Challenges Faced

* **Dialect mixing**: Tunisian Arabic often mixed with French/English → solved with transliteration + hybrid language detection
* **Noisy audio**: solved with preprocessing & `noisereduce`
* **Acronym expansion**: built custom registry with first-use expansion
* **User data**: managed with JSON/SQLite, scalable to SQLAlchemy
* **Search**: balanced between keyword speed & semantic embeddings

---

## ▶️ Running the App

### CLI

```bash
python app_int.py
```

### Streamlit Web App

```bash
streamlit run app.py
```

Go to: `http://localhost:8501`

---

## 📌 Roadmap

* [ ] Multi-speaker diarization
* [ ] OAuth-based authentication
* [ ] Dockerized deployment
* [ ] Full SQLAlchemy migration
* [ ] Fine-tuned summarization models

---

## 📜 License

MIT License

````

---

# 📜 Sub-README files

---

## `Transcription/README.md`

```markdown
# 🎙️ Transcription Module

This folder contains scripts for audio preprocessing, transcription, and post-processing.

## Files
- `record_voice.py` → record audio from mic
- `preprocess_audio.py` → noise reduction, normalization
- `transcribe_audio.py` → run Whisper/Faster-Whisper
- `process_transcript.py` → acronym expansion & transliteration
- `punctuate.py` → restore punctuation
- `stream_transcribe.py` → real-time streaming transcription
- `run_pipeline.py` → run full pipeline
- `run_pipeline2.py` → alternate pipeline runner
- `test_whisper*.py` → test scripts
- Outputs: `original_transcript.txt`, `expanded_transcript.txt`, `translated_french.txt`, `summary.txt`

## Workflow
1. Record or upload audio
2. Preprocess (denoise, normalize)
3. Transcribe (Whisper/Faster-Whisper)
4. Process transcript (punctuation, acronyms, transliteration)
5. Save and use in knowledge base
````

---

## `PostProcessing & Summarization/README.md`

```markdown
# 📝 PostProcessing & Summarization

Handles transcript cleanup and summarization.

## Files
- `summarize.py` → abstractive meeting summarization
- `bullet_points.py` (output) → action items

## Workflow
1. Input transcript
2. Clean text
3. Generate bullet points or summaries
```

---

## `Knowledge Extraction & Retrieval/README.md`

```markdown
# 📚 Knowledge Extraction & Retrieval

Implements knowledge base search.

## Features
- Index transcripts with LLaMA-Index
- Keyword search fallback
- Hybrid retrieval (semantic + keyword)

## Workflow
1. User query
2. Search transcripts (keyword + embeddings)
3. Return matching segments
```

---

## `core/README.md`

```markdown
# 🔤 Core Module

Core utilities for acronyms.

- `acronyms.py` → acronym registry & expansion logic

Workflow:
- On first mention → expand with full form (e.g. *Artificial Intelligence (AI)*)
- Later mentions → shortened (*AI*)
```

---

## `acronym_index/README.md`

```markdown
# 🗂️ Acronym Index

Vector-based storage of acronyms.

- `index_builder.py` → builds vector index
- `default_vector_store.json` → embeddings store
- `docstore.json`, `graph_store.json`, `image_vector_store.json`, `index_store.json` → index persistence
```

---

