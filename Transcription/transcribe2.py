import json
import wave
import os
from vosk import Model, KaldiRecognizer

# 🌍 Multilingual context vocabulary (Tunisian Arabic + French + English)
CONTEXT_PHRASES = {
    "work_meeting": [
        "projet", "meeting", "réunion", "client", "تخطيط", "planning", "objectif", "ميزانية",
        "startup", "تسيير", "gestion", "timeline", "deadlines", "مسؤول", "responsable", "strategy"
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


def load_audio(audio_path):
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    wf = wave.open(audio_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        raise ValueError("Audio file must be mono channel, 16-bit PCM WAV")
    return wf


def transcribe(audio_path, model_path):
    context = select_context()
    phrases = CONTEXT_PHRASES.get(context, [])
    print(f"\n🎯 Using context: {context.replace('_', ' ').title()}\n")

    if not os.path.isdir(model_path):
        raise FileNotFoundError(f"Model folder not found: {model_path}")

    model = Model(model_path)
    wf = load_audio(audio_path)
    rec = KaldiRecognizer(model, wf.getframerate(), json.dumps(phrases))

    results = []
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


if __name__ == "__main__":
    AUDIO_PATH = "my_voice.wav"  # Or "live_recording.wav", etc.
    MODEL_PATH = os.path.join(os.getcwd(), "vosk-model")  # Absolute path for safety

    transcribe(AUDIO_PATH, MODEL_PATH)
