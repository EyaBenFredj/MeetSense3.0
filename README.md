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
## 📂 Project Structure

MeetSense3.0/
│
├── .venv/                         # Virtual environment
├── .env                           # Environment variables (API keys, configs)
├── .gitignore                     # Git ignored files
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
│
├── app.py                         # Main Streamlit application
├── app_int.py                     # CLI/Intermediate application
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
