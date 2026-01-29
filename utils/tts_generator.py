import pyttsx3
import os

print("✅ tts_generator.py started")

# --- project root ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOVELS_DIR = os.path.join(BASE_DIR, "books", "novels")

print("📂 Project root:", BASE_DIR)
print("📂 Novels dir:", NOVELS_DIR)

engine = pyttsx3.init()
engine.setProperty("rate", 165)


def generate_audio(text_path, audio_path):
    print(f"🎧 Generating audio for: {text_path}")

    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()

    engine.save_to_file(text, audio_path)
    engine.runAndWait()

    print(f"✅ Saved audio: {audio_path}")


def generate_all_novels():
    if not os.path.exists(NOVELS_DIR):
        print("❌ Novels folder not found")
        return

    for novel in os.listdir(NOVELS_DIR):
        novel_path = os.path.join(NOVELS_DIR, novel)

        if not os.path.isdir(novel_path):
            continue

        print(f"\n📖 Processing novel: {novel}")

        for file in os.listdir(novel_path):
            if file.endswith(".txt"):
                txt_path = os.path.join(novel_path, file)
                audio_path = os.path.join(
                    novel_path, file.replace(".txt", ".mp3")
                )

                if os.path.exists(audio_path):
                    print(f"⏭ Skipping (already exists): {audio_path}")
                    continue

                generate_audio(txt_path, audio_path)


if __name__ == "__main__":
    generate_all_novels()
