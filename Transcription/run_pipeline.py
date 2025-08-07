import os
from Transcription.record_voice import *
from Transcription.preprocess_audio import reduce_noise
from transcribe2 import transcribe
from Transcription.punctuate import restore_punctuation

AUDIO_DIR = "../uploads"
RAW_AUDIO = os.path.join(AUDIO_DIR, "my_voice.wav")
CLEAN_AUDIO = os.path.join(AUDIO_DIR, "my_voice_clean.wav")

print("\n🎙️ Step 1: Recording audio...")
record_duration = 10  # seconds
record_voice(RAW_AUDIO, duration=record_duration)

print("\n🔇 Step 2: Reducing noise...")
reduce_noise(RAW_AUDIO, CLEAN_AUDIO)

print("\n🧠 Step 3: Transcribing cleaned audio...")
transcript = transcribe(CLEAN_AUDIO)

print("\n🔡 Step 4: Restoring punctuation...")
punctuated = restore_punctuation(transcript)

print("\n✅ Final Transcript with Punctuation:\n")
print(punctuated)

# Optional: Save transcript to file
output_file = os.path.join(AUDIO_DIR, "transcript.txt")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(punctuated)
print(f"\n📁 Transcript saved to: {output_file}")
