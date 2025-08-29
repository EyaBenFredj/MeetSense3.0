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

MeetSense3.0/
│── .venv/ # Virtual environment
│── .env # Environment variables
│── .gitignore
│── requirements.txt # Python dependencies
│── README.md # Project documentation
│
│── app.py # Main Streamlit application
│── app_int.py # Intermediate/CLI app
│── pipeline.py # Central transcription pipeline
│── whisper_transcript.txt # Example transcript output
│── temp_Enregistrement.m4a # Example audio file
│── users.db # SQLite database (users & transcripts)
│
├── whisper_streaming/ # Streaming transcription tests
│
├── Transcription/ # Core speech-to-text modules
│ ├── record_voice.py # Record audio from mic
│ ├── preprocess_audio.py # Audio preprocessing (noise reduction)
│ ├── transcribe_audio.py # Whisper/Faster-Whisper transcription
│ ├── process_transcript.py # Acronym expansion & transliteration
│ ├── punctuate.py # Adds punctuation
│ ├── stream_transcribe.py # Streaming transcription
│ ├── run_pipeline.py # Full transcription pipeline
│ ├── run_pipeline2.py # Alternate pipeline runner
│ ├── test_whisper.py # Whisper test scripts
│ ├── test_whisper2.py
│ ├── test_whisper3.py
│ ├── bullet_points.txt # Example bullet point summary
│ ├── expanded_transcript.txt # Transcript with acronyms expanded
│ ├── original_transcript.txt # Raw transcript output
│ ├── transcript.txt # Processed transcript
│ ├── translated_french.txt # Translated transcript (French)
│ ├── summary.txt # Example transcript summary
│ ├── whisper_transcript.txt # Whisper transcript output
│ └── my_voice.wav # Example input audio
│
├── Knowledge Extraction & Retrieval/
│ └── (Modules for semantic + keyword search on transcripts)
│
├── PostProcessing & Summarization/
│ └── summarize.py # Transcript summarization
│
├── scripts/
│ └── build_acronym_registry.py # Script to build acronym registry
│
├── tools/
│ └── acronym_seed.py # Initial acronym seeds
│
├── acronym_index/ # Vector index for acronyms
│ ├── index_builder.py
│ ├── default_vector_store.json
│ ├── docstore.json
│ ├── graph_store.json
│ ├── image_vector_store.json
│ └── index_store.json
│
├── core/
│ └── acronyms.py # Acronym expansion logic
│
├── app/
│ └── chat_chain.py # Conversational pipeline (LLM integration)
│
├── data/ # User & transcript storage
│ ├── audio/ # Uploaded audio
│ ├── transcripts/ # User transcripts
│ ├── uploads/ # Temporary uploads
│ ├── acronyms.json # Acronym dictionary
│ ├── meetings.db # Meeting database
│ └── users.json # User accounts
│
├── Interface/
│ ├── Pages/
│ │ ├── init.py
│ │ ├── asr.py # Speech-to-text page
│ │ ├── auth.py # User authentication
│ │ ├── knowledge.py # Knowledge base search
│ │ └── storage.py # Transcript management
