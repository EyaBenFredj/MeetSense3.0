import os
import wave
import json
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment

# 🌍 Multilingual context vocabulary (Tunisian Arabic + French + English)
CONTEXT_PHRASES = {
    "angular_tuto": [
    "component", "template", "service", "directive", "module", "pipe", "routing", "formulaire",
    "API", "observable", "rxjs", "async", "subscribe", "interface", "ngOnInit", "binding",
    "two-way", "props", "event", "input", "output", "class", "structure", "ngModel",
    "data", "DOM", "node_modules", "build", "serve", "compilation", "transpiler", "CLI",
    "angular.json", "tsconfig", "html", "css", "typescript", "ts", "javascript", "assets",
    "واجهة", "تطبيق", "مشروع", "كومبونون", "مكون", "formulaire", "événement",
    "تحديث", "module dynamique", "installation", "npm", "package", "أوامر", "commande",
    "تشغيل", "تطوير", "بيئة", "dev", "production", "import", "export", "service injectable",
    "httpClient", "auth", "تسجيل", "واجهة دخول", "تسجيل خروج", "guard", "route",
    "navigation", "lazy loading", "interceptor", "form reactive", "validation", "erreurs",
    "message d'erreur", "directive personnalisée", "component imbriqué", "animation"
],

    "networks_fiber": [
        "fiber", "fibre optique", "backbone", "5G", "déploiement", "شبكة", "تغطية", "connexion",
        "haut débit", "FTTx", "latency", "النطاق العريض", "capacité", "architecture réseau"
    ],
    "it_security": [
        "cybersecurity", "sécurité", "اختراق", "firewall", "تحقق", "authentification", "مراقبة",
        "antivirus", "intrusion", "compliance", "SOC", "privileges", "كلمة سر", "protection", "data leak"
    ],
    "data_ai": [
        "الذكاء الاصطناعي", "machine learning", "model", "données", "data", "analyse prédictive",
        "predictive maintenance", "معالجة", "خوارزمية", "algorithm", "نموذج", "training", "AI", "optimisation"
    ],
    "consulting_transform": [
        "digital transformation", "تحول رقمي", "governance", "agile", "scrum", "تطوير", "workflow",
        "pilotage", "impact", "périmètre", "efficacité", "sustainability", "تغيير", "change management"
    ]
}


def select_context():
    print("🔧 Select meeting context:")
    options = list(CONTEXT_PHRASES.keys())
    for i, key in enumerate(options, 1):
        print(f"{i}. {key.replace('_', ' ').title()}")
    choice = input("Enter number: ").strip()
    return options[int(choice) - 1] if choice.isdigit() and 1 <= int(choice) <= len(options) else "work_meeting"


def convert_mp3_to_wav(mp3_path, wav_path):
    if not os.path.exists(mp3_path):
        raise FileNotFoundError(f"MP3 file not found: {mp3_path}")
    print("🔄 Converting MP3 to WAV (mono, 16-bit PCM)...")
    audio = AudioSegment.from_mp3(mp3_path)
    audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    audio.export(wav_path, format="wav")
    print("✅ Conversion complete.")
    return wav_path


def load_audio(wav_path):
    if not os.path.exists(wav_path):
        raise FileNotFoundError(f"WAV file not found: {wav_path}")
    wf = wave.open(wav_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        raise ValueError("Audio must be mono channel, 16-bit PCM WAV")
    return wf


def transcribe(mp3_path, model_path):
    context = select_context()
    phrases = CONTEXT_PHRASES.get(context, [])
    print(f"\n🎯 Using context: {context.replace('_', ' ').title()}\n")

    if not os.path.isdir(model_path):
        raise FileNotFoundError(f"Model folder not found: {model_path}")

    # Temporary WAV file path
    wav_path = "converted_temp.wav"
    convert_mp3_to_wav(mp3_path, wav_path)

    model = Model(model_path)
    wf = load_audio(wav_path)
    rec = KaldiRecognizer(model, wf.getframerate(), json.dumps(phrases))

    results = []
    print("🧠 Transcribing...")
    while True:
        data = wf.readframes(4000)
        if not data:
            break
        if rec.AcceptWaveform(data):
            results.append(json.loads(rec.Result()))
    results.append(json.loads(rec.FinalResult()))

    transcript = " ".join([res.get("text", "") for res in results])
    print("📝 Transcript:\n")
    print(transcript)

    with open("transcript.txt", "w", encoding="utf-8") as f:
        f.write(transcript)
    print("\n✅ Saved to transcript.txt")

    wf.close()
    os.remove(wav_path)  # Clean up temporary file


if __name__ == "__main__":
    raw_input_path = input("🎙️ Enter path to your MP3 file : ").strip()

    # Clean pasted Windows path: remove quotes, normalize slashes
    cleaned_path = raw_input_path.strip('"').strip("'")
    MP3_PATH = os.path.normpath(cleaned_path)

    MODEL_PATH = os.path.join(os.getcwd(), "vosk-model")  # Adjust if needed

    try:
        transcribe(MP3_PATH, MODEL_PATH)
    except Exception as e:
        print(f"❌ Error: {e}")

