import subprocess
from pathlib import Path


# For this step, we only extract audio from video files.
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov"}


def clean_audio_name(video_path):
    # Some downloaded files can end up named like sermon_1_video.mp4.mp4.
    # Remove video extensions until only the clean sermon name remains.
    clean_path = video_path
    while clean_path.suffix.lower() in VIDEO_EXTENSIONS:
        clean_path = clean_path.with_suffix("")

    return f"{clean_path.name}.mp3"


def main():
    project_root = Path(__file__).resolve().parent.parent
    incoming_folder = project_root / "incoming"
    audio_folder = project_root / "extracted_audio"

    print("Looking for one sermon video in incoming/...")

    video_files = sorted(
        file_path
        for file_path in incoming_folder.iterdir()
        if file_path.is_file() and file_path.suffix.lower() in VIDEO_EXTENSIONS
    )

    if not video_files:
        print("No supported video files found in incoming/.")
        print("Add a .mp4, .mkv, or .mov sermon file, then run this script again.")
        return

    input_video = video_files[0]
    output_audio = audio_folder / clean_audio_name(input_video)

    audio_folder.mkdir(exist_ok=True)

    print(f"Selected video: {input_video.name}")
    print(f"Creating audio file: {output_audio.name}")
    print("Extracting 16 kHz mono MP3 audio...")

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_video),
        "-vn",
        "-acodec",
        "libmp3lame",
        "-ar",
        "16000",
        "-ac",
        "1",
        str(output_audio),
    ]

    result = subprocess.run(command)

    if result.returncode != 0:
        print("Audio extraction failed.")
        print("The original video was not deleted or modified.")
        return

    print("Audio extraction complete.")
    print(f"Output saved to: {output_audio}")
    print("The original video was not deleted or modified.")


if __name__ == "__main__":
    main()
