import os
import whisper

def get_audio_path():
    raw_input_path = input("🎙️ Enter the path to your audio file (e.g. MP3, WAV): ").strip()
    cleaned_path = raw_input_path.strip('"').strip("'")  # Remove quotes if pasted from Explorer
    return os.path.normpath(cleaned_path)

def main():
    audio_path = get_audio_path()

    if not os.path.isfile(audio_path):
        print(f"❌ File not found: {audio_path}")
        return

    print("🧠 Loading Whisper model (small)...")
    model = whisper.load_model("medium")  # You can change to 'base', 'small', etc.

    print("🎧 Transcribing audio (language auto-detect)...")
    result = model.transcribe(audio_path, language=None)

    transcript = result["text"]
    print("\n📝 Transcript:\n")
    print(transcript)

    # Save to file
    with open("whisper_transcript.txt", "w", encoding="utf-8") as f:
        f.write(transcript)

    print("\n✅ Saved to 'whisper_transcript.txt'")

if __name__ == "__main__":
    main()
