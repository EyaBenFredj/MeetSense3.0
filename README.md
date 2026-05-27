```
Cognix/
├── api/
│   ├── __init__.py
│   ├── agent_routes.py
│   ├── onboarding_agent.py
│   ├── project_agent.py
│   └── routes.py
├── config/
│   └── settings.py
├── core/
│   ├── __init__.py
│   ├── knowledge_engine.py
│   ├── language_detector.py
│   ├── model_router.py
│   ├── rag_pipeline.py
│   ├── terminology_engine.py
│   └── transcription_engine.py
├── db/
│   ├── __init__.py
│   ├── database.py
│   └── repositories.py
├── services/
│   ├── __init__.py
│   ├── assistant_service.py
│   ├── ingestion_service.py
│   ├── knowledge_service.py
│   ├── meeting_service.py
│   ├── onboarding_agent.py
│   ├── project_agent.py
│   ├── tutorial_service.py
│   └── validation_service.py
└── tests/
    ├── test_api.py
    ├── test_ingestion.py
    ├── test_knowledge.py
    ├── test_language_detector.py
    ├── test_terminology.py
    ├── test_transcription.py
    └── test_validation.py
```


# 🧠 MeetSense : AI Meeting Assistant
**Multilingual AI-powered tool for meeting transcription and knowledge retrieval (Tunisian dialect, French, English).**

This project provides:
- 🎙️ **Accurate meeting transcription** using OpenAI Whisper & Faster-Whisper  
- 🌍 **Multilingual processing** (Tunisian dialect, Arabic script, French, English)  
- 🔤 **Smart acronym expansion** & transliteration of Arabic-script words  
- 📚 **Knowledge base search** over saved transcripts  
- 👤 **User management system** (login, signup, transcript storage)  
- 💻 **Web interfaces** with Streamlit 
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


## 🔹 Demo Previews

Below are some demo screenshots that showcase **MeetSense in action**:

### 1. Streamlit Interface
MeetSense provides an **interactive Streamlit interface** for quickly uploading and processing meeting recordings.  
This interface is lightweight and ideal for prototyping and internal usage.

<img width="1918" height="896" alt="streamlit" src="https://github.com/user-attachments/assets/0c34fc3e-37a6-4431-96ce-60ac2b9bfb56" />

---

### 2. React Extension Prototype
We also built a **React-based interface**, designed to evolve into a **browser extension or standalone web app**.  
This architecture makes it easier to integrate MeetSense into existing workflows (e.g., Google Meet, Zoom, MS Teams)  
and ensures scalability beyond the Streamlit prototype.

<img width="1897" height="986" alt="react interface" src="https://github.com/user-attachments/assets/7ea14b7b-5742-41b0-986c-256872576c04" />

---

### 3. Execution Example – French Transcription
MeetSense can **transcribe meetings directly in French** (or any other supported language).  
Here, an audio snippet is automatically detected as French and converted into clean text, then saved into a transcript file.

<img width="1491" height="807" alt="dem2" src="https://github.com/user-attachments/assets/6f8710f5-190f-4697-a5d0-bae1c28de995" />

---

### 4. Execution Example – Transcription + Acronym Detection
Beyond transcription, MeetSense also performs **acronym detection and expansion**.  
In this example:
- The raw transcript is first generated in mixed languages.  
- Acronyms such as `DD`, `MT`, `QA`, `RM`, and `SP` are automatically spotted.  
- A second, enriched transcript is created where acronyms are expanded for clarity (e.g., *SP → Sofrecom Products*).  

This feature ensures meeting transcripts are **readable and knowledge-rich**, even when shorthand or domain-specific terms are used.

<img width="1492" height="842" alt="dem1" src="https://github.com/user-attachments/assets/ed1f0b96-e78a-4655-bb8a-caeb5744bb27" />

## 📂 Project Structure

```bash 


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


## 📦 Installation

1. Clone the repo:
```bash
git clone https://github.com/EyaBenFredj/MeetSense3.0
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
* ** streamlit** – interfaces (demo + full app)

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



# 📝 PostProcessing & Summarization

Handles transcript cleanup and summarization.

## Files
- `summarize.py` → abstractive meeting summarization
- `bullet_points.py` (output) → action items

## Workflow
1. Input transcript
2. Clean text
3. Generate bullet points or summaries



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





