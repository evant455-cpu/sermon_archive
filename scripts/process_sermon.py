import os
import subprocess
import sys
from pathlib import Path

from extract_audio import (
    VIDEO_EXTENSIONS,
    clean_audio_name,
    expected_video_name,
    output_audio_name,
)
from format_transcript import readable_transcript_name
from transcribe_audio_speechmatics import input_audio_name, raw_transcript_name


def find_expected_video(incoming_folder, sermon_id):
    expected_name = expected_video_name(sermon_id)
    video_files = sorted(
        file_path
        for file_path in incoming_folder.iterdir()
        if file_path.is_file() and file_path.suffix.lower() in VIDEO_EXTENSIONS
    )

    for video_path in video_files:
        if clean_audio_name(video_path) == expected_name:
            return video_path

    return None


def run_step(project_root, sermon_id, script_name):
    env = os.environ.copy()
    env["SERMON_ID"] = sermon_id
    command = [sys.executable, str(project_root / "scripts" / script_name)]
    return subprocess.run(command, cwd=project_root, env=env).returncode == 0


def write_prompt_package(prompt_path, workflow_path, transcript_path, sermon_id):
    workflow_prompt = workflow_path.read_text(encoding="utf-8")
    readable_transcript = transcript_path.read_text(encoding="utf-8")

    prompt_text = "\n".join(
        [
            workflow_prompt.rstrip(),
            "",
            f"source_file: {sermon_id}",
            "",
            "TRANSCRIPT START",
            readable_transcript.rstrip(),
            "TRANSCRIPT END",
            "",
        ]
    )

    prompt_path.write_text(prompt_text, encoding="utf-8")


def main():
    sermon_id = os.environ.get("SERMON_ID")
    if not sermon_id:
        print("SERMON_ID is missing. Set it before running this script.")
        print('Example: $env:SERMON_ID="sermon_004"')
        sys.exit(1)

    project_root = Path(__file__).resolve().parent.parent
    incoming_folder = project_root / "incoming"
    audio_folder = project_root / "extracted_audio"
    transcripts_folder = project_root / "transcripts"
    working_folder = project_root / "working"

    input_video = find_expected_video(incoming_folder, sermon_id)
    if not input_video:
        print(f"Target SERMON_ID: {sermon_id}")
        print("Expected input video was not found.")
        print(f"Expected video match: {expected_video_name(sermon_id)}")
        print("No files were changed.")
        sys.exit(1)

    output_audio = audio_folder / output_audio_name(sermon_id)
    raw_transcript = transcripts_folder / raw_transcript_name(sermon_id)
    readable_transcript = transcripts_folder / readable_transcript_name(sermon_id)
    prompt_path = working_folder / f"claude_prompt_{sermon_id}.txt"
    workflow_path = project_root / "docs" / "manual_claude_analysis_workflow.md"

    print(f"Target SERMON_ID: {sermon_id}")
    print(f"Input video: {input_video}")

    if output_audio.exists():
        print(f"Skipping audio extraction; output already exists: {output_audio}")
    else:
        print("Running audio extraction...")
        if not run_step(project_root, sermon_id, "extract_audio.py"):
            print("Audio extraction failed. Stopping pipeline.")
            sys.exit(1)

    if raw_transcript.exists():
        print(f"Skipping transcription; output already exists: {raw_transcript}")
    else:
        print("Running transcription...")
        if not run_step(project_root, sermon_id, "transcribe_audio_speechmatics.py"):
            print("Transcription failed. Stopping pipeline.")
            sys.exit(1)

    if readable_transcript.exists():
        print(f"Skipping transcript formatting; output already exists: {readable_transcript}")
    else:
        print("Running transcript formatting...")
        if not run_step(project_root, sermon_id, "format_transcript.py"):
            print("Transcript formatting failed. Stopping pipeline.")
            sys.exit(1)

    if not readable_transcript.exists():
        print("Readable transcript was not found. Prompt package was not created.")
        sys.exit(1)

    working_folder.mkdir(exist_ok=True)
    write_prompt_package(prompt_path, workflow_path, readable_transcript, sermon_id)
    print(f"Manual AI prompt package saved to: {prompt_path}")
    print("No summary or metadata files were created.")


if __name__ == "__main__":
    main()
