import sys
import os
import sounddevice as sd
import numpy as np
import queue
import datetime

# Add path to whisper_streaming folder
sys.path.append(os.path.join(os.path.dirname(__file__), "whisper_streaming"))

from whisper_streaming.whisper_online import OnlineASRProcessor, FasterWhisperASR

# Init Whisper model (auto language detection, medium model)
asr = FasterWhisperASR(lan="auto", model_size_or_path="medium")
asr.use_vad()  # Enable Voice Activity Detection (recommended)

# Create streaming ASR processor
streaming = OnlineASRProcessor(asr)

# Audio stream settings
samplerate = 16000
blocksize = 4000
audio_queue = queue.Queue()

# Audio callback for mic
def callback(indata, frames, time, status):
    if status:
        print(f"⚠️ {status}")
    audio_queue.put(indata.copy())

# Start streaming
with open("meeting_transcript.txt", "a", encoding="utf-8") as transcript_file:
    with sd.InputStream(samplerate=samplerate, channels=1, dtype="float32", callback=callback, blocksize=blocksize):
        print("🎙️ Listening... Press Ctrl+C to stop.\n")
        try:
            while True:
                # Get audio block from queue
                audio_block = audio_queue.get()
                audio_float32 = audio_block.flatten()
                audio_int16 = (audio_float32 * 32767).astype(np.int16)

                # Feed into streaming processor
                streaming.insert_audio_chunk(audio_int16)
                text = streaming.process_iter()

                if text:
                    timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
                    output_line = f"{timestamp} {text}"
                    print(f"📝 {output_line}")
                    transcript_file.write(output_line + "\n")
                    transcript_file.flush()

        except KeyboardInterrupt:
            print("\n🛑 Transcription stopped by user.")
            final_text = streaming.finish()
            if final_text:
                transcript_file.write(final_text + "\n")
                print(f"📝 Final: {final_text}")
