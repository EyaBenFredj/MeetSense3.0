import sounddevice as sd
from scipy.io.wavfile import write

fs = 16000  # Sample rate (16kHz)

def record_voice(output_path="my_voice.wav", duration=30):
    """
    Records audio from the microphone and saves it as a WAV file.

    Args:
        output_path (str): Path to save the recorded audio.
        duration (int): Duration of the recording in seconds.
    """
    print(f"🎤 Recording for {duration} seconds... Speak now!")
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    print("✅ Done recording!")
    write(output_path, fs, myrecording)
    print(f"🎧 Saved as {output_path}")

# Run only if script is executed directly
if __name__ == "__main__":
    record_voice(duration=30)  # record for 60 seconds
