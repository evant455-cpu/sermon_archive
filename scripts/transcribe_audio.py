import os
from pathlib import Path

MAX_UPLOAD_SIZE_MB = 25
MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024


def main():
    project_root = Path(__file__).resolve().parent.parent
    env_file = project_root / ".env"

    from dotenv import load_dotenv

    load_dotenv(env_file)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY is missing. Set it before running transcription.")
        return

    from openai import OpenAI, OpenAIError

    audio_folder = project_root / "extracted_audio"
    transcripts_folder = project_root / "transcripts"

    print("Looking for one extracted MP3 audio file...")

    audio_files = sorted(
        file_path
        for file_path in audio_folder.iterdir()
        if file_path.is_file() and file_path.suffix.lower() == ".mp3"
    )

    if not audio_files:
        print("No .mp3 audio files found in extracted_audio/.")
        print("Run scripts/extract_audio.py first, then run this script again.")
        return

    input_audio = audio_files[0]
    output_transcript = transcripts_folder / f"{input_audio.stem}_raw_transcript.txt"
    audio_size = input_audio.stat().st_size

    transcripts_folder.mkdir(exist_ok=True)

    print(f"Selected audio: {input_audio.name}")
    print(f"Audio file size: {audio_size / (1024 * 1024):.1f} MB")

    if audio_size > MAX_UPLOAD_SIZE_BYTES:
        print(f"Audio file is over {MAX_UPLOAD_SIZE_MB} MB.")
        print("Please use a smaller audio file before running transcription.")
        print("The original audio file was not deleted or modified.")
        return

    print("Sending audio to OpenAI for transcription...")

    client = OpenAI(api_key=api_key)

    try:
        with input_audio.open("rb") as audio_file:
            transcript_text = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file,
                response_format="text",
            )
    except OpenAIError as error:
        print("Transcription failed while calling the OpenAI API.")
        print(f"Error: {error}")
        print("The original audio file was not deleted or modified.")
        return

    output_transcript.write_text(transcript_text, encoding="utf-8")

    print("Transcription complete.")
    print(f"Transcript saved to: {output_transcript}")
    print("The original audio file was not deleted or modified.")


if __name__ == "__main__":
    main()
