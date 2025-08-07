from pydub import AudioSegment
import noisereduce as nr
import numpy as np
import scipy.io.wavfile as wavfile
import os

def reduce_noise(input_path, output_path):
    # Load audio
    audio = AudioSegment.from_wav(input_path)
    samples = np.array(audio.get_array_of_samples())

    # Reduce noise
    reduced = nr.reduce_noise(y=samples.astype('float32'), sr=audio.frame_rate)

    # Export cleaned audio
    wavfile.write(output_path, audio.frame_rate, reduced.astype(np.int16))
    print(f"✅ Noise-reduced audio saved: {output_path}")

if __name__ == "__main__":
    reduce_noise("../uploads/my_voice.wav", "uploads/my_voice_clean.wav")
