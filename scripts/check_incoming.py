from pathlib import Path


# These are the audio and video file types we want to find for now.
MEDIA_EXTENSIONS = {".mp4", ".mkv", ".mov", ".mp3", ".wav", ".m4a"}


def main():
    # The incoming folder is one level above this scripts folder.
    project_root = Path(__file__).resolve().parent.parent
    incoming_folder = project_root / "incoming"

    # Look for files in incoming/ that have one of the allowed extensions.
    sermon_files = [
        file_path
        for file_path in incoming_folder.iterdir()
        if file_path.is_file() and file_path.suffix.lower() in MEDIA_EXTENSIONS
    ]

    if not sermon_files:
        print("No sermon audio or video files found.")
        print("Add sermon files to the incoming/ folder, then run this script again.")
        return

    print("Sermon files found in incoming/:")
    for file_path in sermon_files:
        print(f"- {file_path.name}")


if __name__ == "__main__":
    main()
