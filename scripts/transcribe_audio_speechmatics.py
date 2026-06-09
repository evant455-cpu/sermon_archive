import asyncio
import os
from pathlib import Path


def hide_secret(message, secret):
    if not secret:
        return message
    return message.replace(secret, "[hidden]")


async def transcribe_audio(input_audio, output_transcript, api_key):
    try:
        from speechmatics.batch import AsyncClient, TranscriptionConfig
    except ModuleNotFoundError:
        print("The Speechmatics Python package is not installed for this Python.")
        print("Install project dependencies with: python -m pip install -r requirements.txt")
        print("No audio files were modified or deleted.")
        return False

    client = AsyncClient(api_key=api_key)
    try:
        config = TranscriptionConfig(language="en")
        result = await client.transcribe(
            audio_file=str(input_audio),
            transcription_config=config,
        )
    finally:
        await client.close()

    output_transcript.write_text(result.transcript_text, encoding="utf-8")
    return True


def main():
    project_root = Path(__file__).resolve().parent.parent
    env_file = project_root / ".env"

    try:
        from dotenv import load_dotenv
    except ModuleNotFoundError:
        print("python-dotenv is not installed for this Python.")
        print("Install project dependencies with: python -m pip install -r requirements.txt")
        print("No audio files were modified or deleted.")
        return

    load_dotenv(env_file)

    api_key = os.environ.get("SPEECHMATICS_API_KEY")
    if not api_key:
        print("SPEECHMATICS_API_KEY is missing.")
        print("Add it to .env or your environment, then run this script again.")
        print("No audio files were modified or deleted.")
        return

    audio_folder = project_root / "extracted_audio"
    transcripts_folder = project_root / "transcripts"
    requested_sermon_id = os.environ.get("SERMON_ID", "sermon_1_video")

    print("Looking for the first MP3 file in extracted_audio/...")

    audio_files = sorted(
        file_path
        for file_path in audio_folder.iterdir()
        if file_path.is_file() and file_path.suffix.lower() == ".mp3"
    )

    if not audio_files:
        print("No .mp3 audio files found in extracted_audio/.")
        print("No audio files were modified or deleted.")
        return

    matching_audio = [
        file_path for file_path in audio_files if file_path.stem == requested_sermon_id
    ]

    if not matching_audio:
        print(f"No audio found for SERMON_ID={requested_sermon_id}.")
        print("No audio files were modified or deleted.")
        return

    input_audio = matching_audio[0]

    output_transcript = transcripts_folder / f"{input_audio.stem}_raw_transcript.txt"

    transcripts_folder.mkdir(exist_ok=True)

    print(f"Selected audio: {input_audio.name}")
    print("Sending audio to Speechmatics for batch transcription...")

    try:
        transcribed = asyncio.run(
            transcribe_audio(input_audio, output_transcript, api_key)
        )
    except Exception as error:
        print("Transcription failed while calling the Speechmatics API.")
        print(f"Error: {hide_secret(str(error), api_key)}")
        print("The original audio file was not deleted or modified.")
        return

    if not transcribed:
        return

    print("Transcription complete.")
    print(f"Transcript saved to: {output_transcript}")
    print("The original audio file was not deleted or modified.")


if __name__ == "__main__":
    main()
